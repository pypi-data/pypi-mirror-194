from __future__ import annotations

import collections.abc
import time
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, List, Mapping, Optional, Sequence, Type, TypeVar, Union, cast
from urllib.parse import urljoin

import pandas as pd
import requests
from pydantic import BaseModel, ValidationError
from requests import HTTPError
from requests import JSONDecodeError as RequestsJSONDecodeError

from chalk._version import __version__ as chalkpy_version
from chalk.client import ChalkClient, Dataset, OnlineQueryResult
from chalk.client.dataset import DatasetVersion, load_dataset
from chalk.client.exc import (
    ChalkAuthException,
    ChalkBaseException,
    ChalkComputeResolverException,
    ChalkDatasetDownloadException,
    ChalkOfflineQueryException,
    ChalkOnlineQueryException,
    ChalkResolverRunException,
    ChalkWhoAmIException,
)
from chalk.client.models import (
    ChalkError,
    ComputeResolverOutputRequest,
    ComputeResolverOutputResponse,
    CreateOfflineQueryJobRequest,
    CreateOfflineQueryJobResponse,
    ErrorCode,
    FeatureResult,
    GetOfflineQueryJobResponse,
    OfflineQueryContext,
    OfflineQueryInput,
    OnlineQueryContext,
    OnlineQueryRequest,
    OnlineQueryResponse,
    ResolverRunResponse,
    WhoAmIResponse,
    _ExchangeCredentialsRequest,
    _ExchangeCredentialsResponse,
    _TriggerResolverRunRequest,
)
from chalk.config.auth_config import load_token
from chalk.features import DataFrame, Feature, FeatureNotFoundException, ensure_feature
from chalk.features.pseudofeatures import CHALK_TS_FEATURE
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import polars as pl

_logger = get_logger(__name__)

T = TypeVar("T")


class _ChalkClientConfig(BaseModel):
    name: str
    client_id: str
    client_secret: str
    api_server: str
    active_environment: Optional[str]


def _normalize_input_times(input_times: Union[datetime, Sequence[datetime], None], input_len: int):
    if input_times is None:
        input_times = datetime.now(timezone.utc)
    if isinstance(input_times, datetime):
        input_times = [input_times for _ in range(input_len)]
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo

    input_times = [x.replace(tzinfo=local_tz) if x.tzinfo is None else x for x in input_times]
    input_times = [x.astimezone(timezone.utc) for x in input_times]
    return input_times


class DatasetImpl(Dataset):
    def __init__(self, data: pl.LazyFrame, errors: Optional[List[ChalkError]] = None):
        self._data = DataFrame(data)
        self._errors = errors

    @property
    def data(self) -> DataFrame:
        return self._data

    @property
    def errors(self) -> Optional[List[ChalkError]]:
        return self._errors

    def _df_repr(self):
        if self._errors:
            return pd.DataFrame([vars(x) for x in self._errors])
        return self._data

    def __repr__(self) -> str:
        return repr(self._df_repr())


class OnlineQueryResponseImpl(OnlineQueryResult):
    data: List[FeatureResult]
    errors: List[ChalkError]
    warnings: List[str]

    def __init__(self, data: List[FeatureResult], errors: List[ChalkError], warnings: List[str]):
        self.data = data
        self.errors = errors
        self.warnings = warnings
        for d in self.data:
            if d.value is not None:
                try:
                    f = Feature.from_root_fqn(d.field)
                except FeatureNotFoundException:
                    self.warnings.append(
                        f"Return data {d.field}:{d.value} cannot be decoded. Attempting to JSON decode"
                    )
                else:
                    d.value = f.converter.from_json_to_rich(d.value)

        self._values = {d.field: d for d in self.data}

    def _df_repr(self):
        if self.errors:
            info = [vars(x) for x in self.errors]
        else:
            info = [{"field": x.field, "value": x.value, "error": x.error, "ts": x.ts} for x in self.data]
        return pd.DataFrame(info)

    def __repr__(self) -> str:
        return repr(self._df_repr())

    def _repr_html_(self) -> Union[str, None]:
        return self._df_repr()._repr_html_()

    def get_feature(self, feature: Any) -> Optional[FeatureResult]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        return self._values.get(str(feature))

    def get_feature_value(self, feature: Any) -> Optional[Any]:
        # Typing `feature` as Any, as the Features will be typed as the underlying datatypes, not as Feature
        v = self.get_feature(feature)
        return v and v.value


class ChalkAPIClientImpl(ChalkClient):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(ChalkAPIClientImpl)
        obj.__init__(*args, **kwargs)
        obj.__name__ = "ChalkClient"
        obj.__qualname__ = "chalk.client.ChalkClient"
        return obj

    def __repr__(self):
        return f"chalk.client.ChalkClient<{self._config.name}>"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        environment: Optional[str] = None,
        api_server: Optional[str] = None,
        _skip_cache: bool = False,
    ):
        token = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment,
            api_server=api_server,
            skip_cache=_skip_cache,
        )
        if token is None:
            raise ChalkAuthException()

        self._config = _ChalkClientConfig(
            name=token.name or "",
            client_id=token.clientId,
            client_secret=token.clientSecret,
            api_server=token.apiServer or "https://api.chalk.ai",
            active_environment=token.activeEnvironment,
        )

        self._default_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"chalkpy-{chalkpy_version}",
            "X-Chalk-Client-Id": self._config.client_id,
            "X-Chalk-Features-Versioned": "true",
        }
        self._exchanged_credentials = False
        self._primary_environment = None

    def _exchange_credentials(self):
        _logger.debug("Performing a credentials exchange")
        resp = requests.post(
            url=urljoin(self._config.api_server, f"v1/oauth/token"),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=_ExchangeCredentialsRequest(
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                grant_type="client_credentials",
            ).dict(),
            timeout=10,
        )
        resp.raise_for_status()
        response_json = resp.json()
        try:
            creds = _ExchangeCredentialsResponse(**response_json)
        except ValidationError:
            raise HTTPError(response=resp)
        self._default_headers["Authorization"] = f"Bearer {creds.access_token}"
        self._primary_environment = creds.primary_environment
        self._exchanged_credentials = True

    def _get_headers(self, environment_override: Optional[str], preview_deployment_id: Optional[str]):
        x_chalk_env_id = environment_override or self._config.active_environment or self._primary_environment
        headers = dict(self._default_headers)  # shallow copy
        if x_chalk_env_id is not None:
            headers["X-Chalk-Env-Id"] = x_chalk_env_id
        if preview_deployment_id is not None:
            headers["X-Chalk-Preview-Deployment"] = preview_deployment_id
        return headers

    @staticmethod
    def _raise_if_200_with_errors(response: BaseModel, exception_cls: Type[ChalkBaseException]):
        errors = getattr(response, "errors", None)
        if errors and isinstance(errors, list) and all(isinstance(e, ChalkError) for e in errors):
            errors = cast(List[ChalkError], errors)
            raise exception_cls(errors=errors)

    @staticmethod
    def _raise_http_error(http_error: HTTPError, exception_cls: Type[ChalkBaseException], **exception_kwargs):
        detail = None
        try:
            response_json = http_error.response.json()
            if isinstance(response_json, Mapping):
                detail = response_json.get("detail")
        except RequestsJSONDecodeError:
            pass

        status_code = http_error.response.status_code
        known_error_code = None
        if status_code == 401:
            known_error_code = ErrorCode.UNAUTHENTICATED
        elif status_code == 403:
            known_error_code = ErrorCode.UNAUTHORIZED

        chalk_error = ChalkError(
            code=known_error_code or ErrorCode.INTERNAL_SERVER_ERROR,
            message=detail or f"Unexpected Chalk server error with status code {status_code}",
        )
        raise exception_cls(errors=[chalk_error], **exception_kwargs)

    def _request(
        self,
        method: str,
        uri: str,
        response: Type[T],
        json: Optional[BaseModel],
        use_engine: bool,
        environment_override: Optional[str],
        exception_cls: Type[ChalkBaseException],
        preview_deployment_id: Optional[str],
        **exception_kwargs,
    ) -> T:
        # Track whether we already exchanged credentials for this request
        exchanged_credentials = False
        if not self._exchanged_credentials:
            exchanged_credentials = True
            try:
                self._exchange_credentials()
            except HTTPError as e:
                self._raise_http_error(http_error=e, exception_cls=exception_cls, **exception_kwargs)
        headers = self._get_headers(
            environment_override=environment_override,
            preview_deployment_id=preview_deployment_id,
        )
        url = urljoin(self._config.api_server, uri)
        json_body = json and json.dict()
        r = requests.request(method=method, headers=headers, url=url, json=json_body)
        if r.status_code in (401, 403) and not exchanged_credentials:
            # It is possible that credentials expired, or that we changed permissions since we last
            # got a token. Exchange them and try again
            self._exchange_credentials()
            r = requests.request(method=method, headers=headers, url=url, json=json_body)

        try:
            r.raise_for_status()
        except HTTPError as e:
            self._raise_http_error(http_error=e, exception_cls=exception_cls, **exception_kwargs)

        return response(**r.json())

    def whoami(self) -> WhoAmIResponse:
        return self._request(
            method="GET",
            uri=f"/v1/who-am-i",
            response=WhoAmIResponse,
            json=None,
            use_engine=False,
            environment_override=None,
            exception_cls=ChalkWhoAmIException,
            preview_deployment_id=None,
        )

    def upload_features(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> Optional[List[ChalkError]]:
        return self.query(
            input=input,
            output=list(input.keys()),
            staleness=None,
            context=context,
            preview_deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        ).errors

    def query(
        self,
        input: Mapping[Union[str, Feature, Any], Any],
        output: Sequence[Union[str, Feature, Any]],
        staleness: Optional[Mapping[Union[str, Feature, Any], str]] = None,
        context: Optional[OnlineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        meta: Optional[Mapping[str, str]] = None,
    ) -> OnlineQueryResponseImpl:
        warnings: List[str] = []
        encoded_inputs = {}
        for feature, value in input.items():
            try:
                feature = ensure_feature(feature)
            except FeatureNotFoundException:
                warnings.append(f"Input {feature} not recognized. JSON encoding {feature} and requesting anyways")
                encoded_inputs[feature] = value
            else:
                encoded_inputs[feature.fqn] = feature.converter.from_rich_to_json(
                    value,
                    missing_value_strategy="error",
                )

        outputs: List[str] = [str(feature) for feature in output]

        request = OnlineQueryRequest(
            inputs=encoded_inputs,
            outputs=outputs,
            staleness={} if staleness is None else {ensure_feature(k).root_fqn: v for k, v in staleness.items()},
            context=context,
            deployment_id=preview_deployment_id,
            correlation_id=correlation_id,
            query_name=query_name,
            meta=meta,
        )

        resp = self._request(
            method="POST",
            uri="/v1/query/online",
            json=request,
            response=OnlineQueryResponse,
            use_engine=preview_deployment_id is None,
            environment_override=context.environment if context else None,
            exception_cls=ChalkOnlineQueryException,
            preview_deployment_id=preview_deployment_id,
        )
        return OnlineQueryResponseImpl(data=resp.data, errors=resp.errors or [], warnings=warnings)

    def offline_query(
        self,
        input: Optional[Union[Mapping[Union[str, Feature, Any], Any], pd.DataFrame, pl.DataFrame, DataFrame]] = None,
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_ts: bool = False,
        output_id: bool = False,
        context: Optional[OfflineQueryContext] = None,
        dataset_name: Optional[str] = None,
        branch: Optional[str] = None,
        max_samples: Optional[int] = None,
        disallow_stale_results: bool = False,
    ):
        if context is None:
            context = OfflineQueryContext()

        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if not input:
            # ChalkClient().sample(...)
            response = self._create_and_await_offline_query_job(
                query_input=None,
                optional_output=optional_output_root_fqns,
                required_output=required_output_root_fqns,
                max_samples=max_samples,
                context=context,
                output_id=output_id,
                output_ts=output_ts,
                dataset_name=dataset_name,
                branch=branch,
                disallow_stale_results=disallow_stale_results,
                preview_deployment_id=None,
                lazy=True,
            )
            return DatasetImpl(data=response.lazy())

        # ChalkClient().get_training_dataframe(...)
        if isinstance(input, (DataFrame, pl.DataFrame)):
            input = input.to_pandas()
        if isinstance(input, collections.abc.Mapping):
            input = {str(k): v for (k, v) in input.items()}
        if not isinstance(input, pd.DataFrame):
            input = pd.DataFrame(input)

        columns = input.columns
        matrix: List[List[Any]] = input.T.values.tolist()

        columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]

        if input_times is None:
            input_times = datetime.now(timezone.utc)
        if isinstance(input_times, datetime):
            input_times = [input_times for _ in range(len(input))]

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                try:
                    f = Feature.from_root_fqn(columns_fqn[col_index])
                except FeatureNotFoundException:
                    # The feature is not in the graph, so passing the value as-is and hoping it's possible
                    # to json-serialize it
                    encoded_feature = value
                else:
                    encoded_feature = f.converter.from_rich_to_json(
                        value,
                        missing_value_strategy="error",
                    )

                matrix[col_index][row_index] = encoded_feature

        query_input = OfflineQueryInput(
            columns=columns_fqn,
            values=matrix,
        )

        response = self._create_and_await_offline_query_job(
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            query_input=query_input,
            output_id=False,
            output_ts=output_ts,
            dataset_name=dataset_name,
            branch=branch,
            context=context,
            max_samples=max_samples,
            disallow_stale_results=disallow_stale_results,
            preview_deployment_id=None,
            lazy=True,
        )
        return DatasetImpl(data=response.lazy())

    def get_training_dataframe(
        self,
        input: Union[Mapping[Union[str, Feature, Any], Any], pd.DataFrame, pl.DataFrame, DataFrame],
        input_times: Union[Sequence[datetime], datetime, None] = None,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_ts: bool = False,
        context: Optional[OfflineQueryContext] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        max_samples: Optional[int] = None,
        disallow_stale_results: bool = False,
    ) -> pd.DataFrame:
        if context is None:
            context = OfflineQueryContext()
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if isinstance(input, (DataFrame, pl.DataFrame)):
            input = input.to_pandas()

        if isinstance(input, collections.abc.Mapping):
            input = {str(k): v for (k, v) in input.items()}

        if not isinstance(input, pd.DataFrame):
            input = pd.DataFrame(input)

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        return self._get_training_dataframe(
            input=input,
            input_times=input_times,
            optional_output=[str(x) for x in output],
            required_output=[str(x) for x in required_output],
            output_id=False,
            output_ts=output_ts,
            context=context,
            dataset=dataset,
            branch=branch,
            max_samples=max_samples,
            disallow_stale_results=disallow_stale_results,
        )

    def _get_training_dataframe(
        self,
        input: pd.DataFrame,
        input_times: Union[Sequence[datetime], datetime, None],
        optional_output: List[str],
        required_output: List[str],
        output_id: bool,
        output_ts: bool,
        max_samples: Optional[int],
        context: OfflineQueryContext,
        dataset: Optional[str],
        branch: Optional[str],
        disallow_stale_results: bool,
    ) -> pd.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")

        columns = input.columns
        matrix: List[List[Any]] = input.T.values.tolist()

        columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]

        input_times = _normalize_input_times(input_times, len(input))

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                try:
                    f = Feature.from_root_fqn(columns_fqn[col_index])
                except FeatureNotFoundException:
                    # The feature is not in the graph, so passing the value as-is and hoping it's possible
                    # to json-serialize it
                    encoded_feature = value
                else:
                    encoded_feature = f.converter.from_rich_to_json(
                        value,
                        missing_value_strategy="error",
                    )

                matrix[col_index][row_index] = encoded_feature

        query_input = OfflineQueryInput(
            columns=columns_fqn,
            values=matrix,
        )

        response = self._create_and_await_offline_query_job(
            optional_output=optional_output,
            required_output=required_output,
            query_input=query_input,
            output_id=output_id,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=branch,
            context=context,
            max_samples=max_samples,
            disallow_stale_results=disallow_stale_results,
            preview_deployment_id=None,
            lazy=False,
        )
        if isinstance(response, pl.LazyFrame):
            response = response.collect()
        return response.to_pandas()

    def sample(
        self,
        output: Sequence[Union[str, Feature, Any]] = (),
        required_output: Sequence[Union[str, Feature, Any]] = (),
        output_id: bool = False,
        output_ts: bool = False,
        max_samples: Optional[int] = None,
        dataset: Optional[str] = None,
        branch: Optional[str] = None,
        context: Optional[OfflineQueryContext] = None,
        disallow_stale_results: bool = False,
    ) -> pd.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if context is None:
            context = OfflineQueryContext()
        optional_output_root_fqns = [str(f) for f in output]
        required_output_root_fqns = [str(f) for f in required_output]

        if len(output) == 0 and len(required_output) == 0:
            raise ValueError("Either 'output' or 'required_output' must be specified.")

        response = self._create_and_await_offline_query_job(
            query_input=None,
            optional_output=optional_output_root_fqns,
            required_output=required_output_root_fqns,
            max_samples=max_samples,
            context=context,
            output_id=output_id,
            output_ts=output_ts,
            dataset_name=dataset,
            branch=branch,
            disallow_stale_results=disallow_stale_results,
            preview_deployment_id=None,
            lazy=False,
        )
        if isinstance(response, pl.LazyFrame):
            response = response.collect()

        return response.to_pandas()

    def get_dataset(
        self,
        dataset_name: str,
        context: Optional[OfflineQueryContext] = None,
        output_ts: bool = False,
        output_id: bool = False,
    ) -> DatasetImpl:
        if context is None:
            context = OfflineQueryContext()
        response: GetOfflineQueryJobResponse = self._get_dataset_urls(
            dataset_name=dataset_name,
            context=context,
            preview_deployment_id=None,
        )
        if response.errors:
            raise ChalkDatasetDownloadException(dataset_name=dataset_name, errors=response.errors)
        result = load_dataset(
            uris=response.urls,
            output_id=output_id,
            output_ts=output_ts,
            version=DatasetVersion(response.version),
            lazy=True,
            columns=response.columns,
        )
        return DatasetImpl(data=result.lazy())

    def trigger_resolver_run(
        self,
        resolver_fqn: str,
        context: Optional[OfflineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
    ) -> ResolverRunResponse:
        _logger.debug(f"Triggering resolver {resolver_fqn} to run")
        if context is None:
            context = OfflineQueryContext()

        request = _TriggerResolverRunRequest(resolver_fqn=resolver_fqn)
        response = self._request(
            method="POST",
            uri="/v1/runs/trigger",
            json=request,
            response=ResolverRunResponse,
            use_engine=False,
            environment_override=context.environment,
            exception_cls=ChalkResolverRunException,
            preview_deployment_id=preview_deployment_id,
        )

        return response

    def get_run_status(
        self,
        run_id: str,
        preview_deployment_id: Optional[str] = None,
        context: Optional[OfflineQueryContext] = None,
    ) -> ResolverRunResponse:
        if context is None:
            context = OfflineQueryContext()

        response = self._request(
            method="GET",
            uri=f"/v1/runs/{run_id}",
            response=ResolverRunResponse,
            json=None,
            use_engine=False,
            environment_override=context.environment,
            exception_cls=ChalkResolverRunException,
            preview_deployment_id=preview_deployment_id,
        )

        return response

    def _create_and_await_offline_query_job(
        self,
        optional_output: List[str],
        required_output: List[str],
        query_input: Optional[OfflineQueryInput],
        max_samples: Optional[int],
        dataset_name: Optional[str],
        branch: Optional[str],
        context: OfflineQueryContext,
        output_id: bool,
        output_ts: bool,
        disallow_stale_results: bool,
        preview_deployment_id: Optional[str],
        lazy: bool = True,
    ) -> Union[pl.DataFrame, pl.LazyFrame]:
        req = CreateOfflineQueryJobRequest(
            output=optional_output,
            required_output=required_output,
            destination_format="PARQUET",
            input=query_input,
            max_samples=max_samples,
            dataset_name=dataset_name,
            branch=branch,
            max_cache_age_secs=0 if disallow_stale_results else None,
        )
        response = self._create_offline_query_job(
            request=req,
            context=context,
            preview_deployment_id=None,
        )
        self._raise_if_200_with_errors(response=response, exception_cls=ChalkOfflineQueryException)

        while True:
            status = self._get_job_status(
                job_id=response.job_id,
                context=context,
                preview_deployment_id=preview_deployment_id,
            )
            if status.is_finished:
                break
            time.sleep(0.5)
        return load_dataset(
            uris=status.urls,
            output_features=[*optional_output, *required_output],
            version=DatasetVersion(response.version),
            output_id=output_id,
            output_ts=output_ts,
            columns=status.columns,
            lazy=lazy,
        )

    def compute_resolver_output(
        self,
        input: Union[Mapping[Union[str, Feature], Any], pl.DataFrame, pd.DataFrame, DataFrame],
        input_times: List[datetime],
        resolver: str,
        context: Optional[OfflineQueryContext] = None,
        preview_deployment_id: Optional[str] = None,
    ) -> pl.DataFrame:
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        if context is None:
            context = OfflineQueryContext()
        if not isinstance(input, DataFrame):
            input = DataFrame(input)
        input = input.to_pandas()

        columns = input.columns
        matrix = input.T.values.tolist()

        columns_fqn = [str(c) for c in (*columns, CHALK_TS_FEATURE)]

        input_times = _normalize_input_times(input_times, len(input))

        matrix.append([a for a in input_times])

        for col_index, column in enumerate(matrix):
            for row_index, value in enumerate(column):
                try:
                    f = Feature.from_root_fqn(columns_fqn[col_index])
                except FeatureNotFoundException:
                    # The feature is not in the graph, so passing the value as-is and hoping it's possible
                    # to json-serialize it
                    encoded_feature = value
                else:
                    encoded_feature = f.converter.from_rich_to_json(value, missing_value_strategy="error")
                matrix[col_index][row_index] = encoded_feature

        query_input = OfflineQueryInput(
            columns=columns_fqn,
            values=matrix,
        )
        request = ComputeResolverOutputRequest(input=query_input, resolver_fqn=resolver)
        response = self._request(
            method="POST",
            uri="/v1/compute_resolver_output",
            json=request,
            response=ComputeResolverOutputResponse,
            environment_override=context.environment,
            use_engine=False,
            exception_cls=ChalkComputeResolverException,
            preview_deployment_id=preview_deployment_id,
        )
        self._raise_if_200_with_errors(response=response, exception_cls=ChalkComputeResolverException)

        while True:
            status = self._get_compute_job_status(
                job_id=response.job_id,
                context=context,
                preview_deployment_id=preview_deployment_id,
            )
            if status.is_finished:
                break
            time.sleep(0.5)

        df = load_dataset(
            uris=status.urls,
            version=status.version,
            executor=None,
            columns=status.columns,
        )
        if isinstance(df, pl.LazyFrame):
            df = df.collect()
        return df

    def _get_compute_job_status(
        self,
        job_id: str,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v1/compute_resolver_output/{job_id}",
            response=GetOfflineQueryJobResponse,
            json=None,
            use_engine=False,
            environment_override=context.environment,
            exception_cls=ChalkComputeResolverException,
            preview_deployment_id=preview_deployment_id,
        )

    def _create_offline_query_job(
        self,
        request: CreateOfflineQueryJobRequest,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
    ):
        response = self._request(
            method="POST",
            uri="/v2/offline_query",
            json=request,
            response=CreateOfflineQueryJobResponse,
            environment_override=context.environment,
            use_engine=False,
            exception_cls=ChalkOfflineQueryException,
            preview_deployment_id=preview_deployment_id,
        )
        return response

    def _get_job_status(
        self,
        job_id: uuid.UUID,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v2/offline_query/{job_id}",
            response=GetOfflineQueryJobResponse,
            environment_override=context.environment,
            use_engine=False,
            json=None,
            exception_cls=ChalkOfflineQueryException,
            preview_deployment_id=preview_deployment_id,
        )

    def _get_dataset_urls(
        self,
        dataset_name: str,
        context: OfflineQueryContext,
        preview_deployment_id: Optional[str],
    ) -> GetOfflineQueryJobResponse:
        return self._request(
            method="GET",
            uri=f"/v2/lazy_dataset/{dataset_name}",
            response=GetOfflineQueryJobResponse,
            environment_override=context.environment,
            use_engine=False,
            json=None,
            exception_cls=ChalkDatasetDownloadException,
            dataset_name=dataset_name,
            preview_deployment_id=preview_deployment_id,
        )
