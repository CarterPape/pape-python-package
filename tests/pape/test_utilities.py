"""Tests for pape.utilities."""

from __future__ import annotations

import datetime

import pytest

from pape import utilities


class _Sample:
    """A throwaway class for exercising the qualified-name helpers."""


# A reference date in each month, all in 2025, to exercise every formatting branch.
_REF = datetime.date(2025, 6, 1)


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        # Spelled-out months (March through July): full name, no period.
        (datetime.date(2025, 3, 5), "March 5"),
        (datetime.date(2025, 4, 5), "April 5"),
        (datetime.date(2025, 5, 5), "May 5"),
        (datetime.date(2025, 6, 5), "June 5"),
        (datetime.date(2025, 7, 5), "July 5"),
        # Abbreviated months: three letters + period.
        (datetime.date(2025, 1, 5), "Jan. 5"),
        (datetime.date(2025, 2, 5), "Feb. 5"),
        (datetime.date(2025, 8, 5), "Aug. 5"),
        (datetime.date(2025, 10, 5), "Oct. 5"),
        (datetime.date(2025, 11, 5), "Nov. 5"),
        (datetime.date(2025, 12, 5), "Dec. 5"),
        # September is the special four-letter "Sept." abbreviation.
        (datetime.date(2025, 9, 5), "Sept. 5"),
        # Day is not zero-padded.
        (datetime.date(2025, 1, 15), "Jan. 15"),
    ],
)
def test_ap_style_date_string_same_year(date: datetime.date, expected: str) -> None:
    # relative_to shares the year, so the year is omitted per AP style.
    assert utilities.ap_style_date_string(date, relative_to=_REF) == expected


@pytest.mark.parametrize(
    ("use_period", "expected"),
    [
        (True, "Jan. 5"),
        (False, "Jan 5"),
    ],
)
def test_ap_style_date_string_use_period(use_period: bool, expected: str) -> None:  # noqa: FBT001
    date = datetime.date(2025, 1, 5)
    assert utilities.ap_style_date_string(date, relative_to=_REF, use_period=use_period) == expected


@pytest.mark.parametrize(
    ("use_period", "expected"),
    [
        (True, "Sept. 5"),
        (False, "Sept 5"),
    ],
)
def test_ap_style_date_string_september_period(use_period: bool, expected: str) -> None:  # noqa: FBT001
    date = datetime.date(2025, 9, 5)
    assert utilities.ap_style_date_string(date, relative_to=_REF, use_period=use_period) == expected


def test_ap_style_date_string_different_year_includes_year() -> None:
    date = datetime.date(2025, 1, 5)
    relative_to = datetime.date(2024, 1, 1)
    assert utilities.ap_style_date_string(date, relative_to=relative_to) == "Jan. 5, 2025"


def test_ap_style_date_string_false_forces_year() -> None:
    # relative_to=False treats the date as absolute: the year is always shown.
    date = datetime.date(2025, 1, 5)
    assert utilities.ap_style_date_string(date, relative_to=False) == "Jan. 5, 2025"


def test_ap_style_date_string_none_defaults_to_today() -> None:
    # A date in a year that is never "this year" exercises the relative_to=None
    # (default-to-now) branch deterministically: the year is always included.
    date = datetime.date(1999, 1, 5)
    assert utilities.ap_style_date_string(date) == "Jan. 5, 1999"


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (5, "5th"),
        (0, "0th"),
        # Teen band: 11th through 13th are all "th" despite their last digit.
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        # Past the teens, the last digit governs again.
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (100, "100th"),
        (101, "101st"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        # Negatives follow the same rules off their absolute value.
        (-1, "-1st"),
        (-11, "-11th"),
    ],
)
def test_ordinal(number: int, expected: str) -> None:
    assert utilities.ordinal(number) == expected


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        # count == 1 -> singular; AP spells "one".
        ({"singular_form": "apple", "count": 1}, "one apple"),
        # count != 1 -> default "+s" plural; AP spells the digit.
        ({"singular_form": "apple", "count": 2}, "two apples"),
        ({"singular_form": "apple", "count": 0}, "zero apples"),
        ({"singular_form": "apple", "count": 9}, "nine apples"),
        # Above 9, AP uses numerals (with thousands separators).
        ({"singular_form": "apple", "count": 10}, "10 apples"),
        ({"singular_form": "apple", "count": 1000}, "1,000 apples"),
        # Explicit irregular plural.
        ({"singular_form": "mouse", "count": 3, "plural_form": "mice"}, "three mice"),
        # AP style off -> numerals even for small counts.
        ({"singular_form": "apple", "count": 2, "use_ap_style": False}, "2 apples"),
        # Non-integer counts never get AP word substitution.
        ({"singular_form": "apple", "count": 2.5}, "2.5 apples"),
        # include_count=False drops the number entirely.
        ({"singular_form": "apple", "count": 3, "include_count": False}, "apples"),
        ({"singular_form": "apple", "count": 1, "include_count": False}, "apple"),
    ],
)
def test_pluralize(kwargs: dict[str, object], expected: str) -> None:
    assert utilities.pluralize(**kwargs) == expected  # type: ignore[arg-type]


def test_full_class_name_builtin_has_no_module_prefix() -> None:
    assert utilities.full_class_name(of_object="hello") == "str"


def test_full_class_name_custom_is_module_qualified() -> None:
    expected = f"{_Sample.__module__}._Sample"
    assert utilities.full_class_name(of_object=_Sample()) == expected


def test_full_name_builtin_has_no_module_prefix() -> None:
    assert utilities.full_name(of_type=str) == "str"


def test_full_name_custom_is_module_qualified() -> None:
    expected = f"{_Sample.__module__}._Sample"
    assert utilities.full_name(of_type=_Sample) == expected
