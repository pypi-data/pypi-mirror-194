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
    """Operations for aggregations in `DataFrame`.

    The class methods on this class are used to create aggregations
    for use in `DataFrame.group_by`.
    """

    @classmethod
    def sum(cls, col, *cols) -> Aggregation:
        """Add together the values of `col` and `*cols` in a `DataFrame`.

        Parameters
        ----------
        col
            There must be at least one column to aggregate.
        cols
            Subsequent columns to aggregate.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.sum(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ├─────────┼──────────┤
        │ i64     │ f64      │
        ╞═════════╪══════════╡
        │  1      │ 4.5      │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        cols = [col, *[t for t in cols]]
        if len(cols) == 1:
            return Aggregation(pl.col(str(cols[0])), lambda x: x.sum())
        c = pl.col([str(c) for c in cols])
        return Aggregation(c, lambda x: pl.sum(c))

    @classmethod
    def product(cls, col) -> Aggregation:
        """Multiply together the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column to aggregate. Used in `DataFrame.group_by`.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...         User.active: [True, True, False],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={
        ...         User.val: op.product(User.val),
        ...         User.active: op.product(User.active),
        ...      }
        ... )
        ╭─────────┬──────────┬─────────────╮
        │ User.id │ User.val │ User.active │
        ├─────────┼──────────┼─────────────┤
        │ i64     │ f64      │ i64         │
        ╞═════════╪══════════╪═════════════╡
        │  1      │ 2        │ 1           │
        ├─────────┼──────────┼─────────────┤
        │  3      │ 10       │ 0           │
        ╰─────────┴──────────┴─────────────╯
        """
        return Aggregation(pl.col(str(col)), lambda x: x.product())

    @classmethod
    def max(cls, col) -> Aggregation:
        """Find the maximum of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the maximum value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.max(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ├─────────┼──────────┤
        │ i64     │ f64      │
        ╞═════════╪══════════╡
        │  1      │ 4        │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
        return Aggregation(pl.col(str(col)), lambda x: x.max())

    @classmethod
    def min(cls, col) -> Aggregation:
        """Find the minimum of the values of `col` in a `DataFrame`.

        Parameters
        ----------
        col
            The column along which to find the minimum value.

        Examples
        --------
        >>> from chalk.features import DataFrame
        >>> df = DataFrame(
        ...     {
        ...         User.id: [1, 1, 3],
        ...         User.val: [0.5, 4, 10],
        ...     }
        ... ).group_by(
        ...      group={User.id: User.id}
        ...      agg={User.val: op.min(User.val)}
        ... )
        ╭─────────┬──────────╮
        │ User.id │ User.val │
        ├─────────┼──────────┤
        │ i64     │ f64      │
        ╞═════════╪══════════╡
        │  1      │ 0.5      │
        ├─────────┼──────────┤
        │  3      │ 10       │
        ╰─────────┴──────────╯
        """
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
    def concat(cls, col, col2, sep: str = "") -> Aggregation:
        c = pl.col([str(col), str(col2)])
        return Aggregation(c, lambda x: pl.concat_str(c, sep=sep))

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
