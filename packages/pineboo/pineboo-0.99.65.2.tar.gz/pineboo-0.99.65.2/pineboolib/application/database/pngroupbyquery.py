# -*- coding: utf-8 -*-
"""Manage a group by from a Query instance."""


class PNGroupByQuery(object):
    """Class that manages each group by of a query."""

    level_: int
    field_: str

    def __init__(self, label: int, field: str) -> None:
        """Specify the level and field."""

        self.level_ = label
        self.field_ = field

    def level(self) -> int:
        """Return the level GroupBy."""

        return self.level_

    def field(self) -> str:
        """Return the field GroupBy."""
        return self.field_
