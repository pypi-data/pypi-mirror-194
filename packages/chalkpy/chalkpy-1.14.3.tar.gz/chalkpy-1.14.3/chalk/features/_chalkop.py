from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List

try:
    import polars as pl
except:
    pl = None


if TYPE_CHECKING:
    from polars import internals as pli

    from chalk.features import Filter


class Aggregation:
    def __init__(self, col, fn):
        self.col = col
        self.fn: Callable[[pli.Expr], pli.Expr] = fn
        self.filters: List[Filter] = []

    def where(self, *f):
        # TODO: Make this support using `and` and `or` between filters.
        #       Right now, the iterable of filters is taken to mean `and`.
        self.filters.extend(f)
        return self

    def __add__(self, other):
        return self

    def __radd__(self, other):
        return self


class op:
    @classmethod
    def sum(cls, col, *cols) -> Aggregation:
        cols = [col, *[t for t in cols]]
        if len(cols) == 1:
            return Aggregation(pl.col(str(cols[0])), lambda x: x.sum())
        c = pl.col([str(c) for c in cols])
        return Aggregation(c, lambda x: pl.sum(c))

    @classmethod
    def max(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.max())

    @classmethod
    def min(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.min())

    @classmethod
    def mode(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.mode())

    @classmethod
    def quantile(cls, col, q: float) -> Aggregation:
        assert q >= 0 <= 1, f"Quantile must be between 0 and 1, but given {q}"
        return Aggregation(pl.col(str(col)), lambda x: x.quantile(q))

    @classmethod
    def median(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.median())

    @classmethod
    def mean(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.mean())

    @classmethod
    def std(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.std())

    @classmethod
    def variance(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.var())

    @classmethod
    def count(cls, col) -> Aggregation:
        return Aggregation(pl.col(str(col)), lambda x: x.count())

    @classmethod
    def concat_str(cls, col, col2, sep: str = "") -> Aggregation:
        c = pl.col([str(col), str(col2)])
        return Aggregation(c, lambda x: pl.concat_str(c, sep=sep))

    # TODO: Add these back with `.sort(...)` on `DataFrame`.
    # @classmethod
    # def last(cls, col) -> Aggregation:
    #     return Aggregation(col, lambda x: x.last())
    #
    # @classmethod
    # def first(cls, col) -> Aggregation:
    #     return Aggregation(col, lambda x: x.first())
