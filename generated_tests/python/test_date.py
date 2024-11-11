import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from datetime import date, timedelta
from pendulum import Date, PendulumException

# Mocking external dependencies
from unittest.mock import patch

# Fixtures for common dates used in multiple tests
@pytest.fixture
def leap_year_date():
    return Date(2020, 2, 29)


@pytest.fixture
def non_leap_year_date():
    return Date(2019, 2, 28)


@pytest.fixture
def start_of_year():
    return Date(2023, 1, 1)


@pytest.fixture
def end_of_year():
    return Date(2023, 12, 31)


# Test cases
def test_set_method_changes_date_components():
    dt = Date(2023, 1, 1)
    changed_dt = dt.set(year=2024, month=12, day=31)
    assert changed_dt.year == 2024
    assert changed_dt.month == 12
    assert changed_dt.day == 31


def test_day_of_week_returns_correct_weekday(leap_year_date):
    # 2020-02-29 is a Saturday
    assert leap_year_date.day_of_week == Date.WeekDay.SATURDAY


def test_day_of_year_for_leap_and_non_leap_year(leap_year_date, non_leap_year_date):
    # Day of year for leap year date (2020-02-29)
    assert leap_year_date.day_of_year == 60
    # Day of year for non-leap year date (2019-02-28)
    assert non_leap_year_date.day_of_year == 59


def test_week_of_year_returns_correct_iso_week(start_of_year):
    # 2023-01-01 is in the first week of the year
    assert start_of_year.week_of_year == 52  # Depending on the year, this might need to be adjusted


def test_days_in_month_for_february_leap_and_non_leap_year(leap_year_date, non_leap_year_date):
    # Leap year February
    assert leap_year_date.days_in_month == 29
    # Non-leap year February
    assert non_leap_year_date.days_in_month == 28


def test_is_future_checks_if_date_is_in_future():
    with patch("pendulum.Date.today", return_value=Date(2023, 1, 1)):
        future_date = Date(2023, 1, 2)
        assert future_date.is_future()


def test_is_past_checks_if_date_is_in_past():
    with patch("pendulum.Date.today", return_value=Date(2023, 1, 2)):
        past_date = Date(2023, 1, 1)
        assert past_date.is_past()


def test_is_leap_year_identifies_leap_years(leap_year_date, non_leap_year_date):
    assert leap_year_date.is_leap_year()
    assert not non_leap_year_date.is_leap_year()


def test_add_and_subtract_method_changes_date_correctly():
    dt = Date(2023, 1, 1)
    dt_added = dt.add(years=1, months=1, days=1)
    assert dt_added == Date(2024, 2, 2)

    dt_subtracted = dt.subtract(years=1, months=1, days=1)
    assert dt_subtracted == Date(2021, 11, 30)


def test_diff_for_humans_localized_output():
    base_date = Date(2023, 1, 1)
    comparison_date = Date(2023, 1, 2)
    # Assuming default locale is English
    assert base_date.diff_for_humans(comparison_date) == "1 day before"


def test_start_of_and_end_of_methods():
    dt = Date(2023, 6, 15)
    start_of_month = dt.start_of("month")
    assert start_of_month == Date(2023, 6, 1)

    end_of_month = dt.end_of("month")
    assert end_of_month == Date(2023, 6, 30)


def test_invalid_unit_for_start_of_raises_error():
    dt = Date(2023, 1, 1)
    with pytest.raises(ValueError):
        dt.start_of("invalid_unit")


def test_average_method_gives_middle_date():
    dt1 = Date(2023, 1, 1)
    dt2 = Date(2023, 1, 3)
    assert dt1.average(dt2) == Date(2023, 1, 2)


def test_today_classmethod_returns_current_date():
    with patch("pendulum.date.today", return_value=date(2023, 1, 1)):
        assert Date.today() == Date(2023, 1, 1)


def test_fromtimestamp_classmethod_creates_date_instance():
    timestamp = 1672531200  # Corresponds to 2023-01-01
    assert Date.fromtimestamp(timestamp) == Date(2023, 1, 1)


def test_replace_method_replaces_specified_date_components():
    dt = Date(2023, 1, 1)
    replaced_dt = dt.replace(year=2024)
    assert replaced_dt.year == 2024
    assert replaced_dt.month == 1  # Month remains unchanged
    assert replaced_dt.day == 1  # Day remains unchanged


def test_is_anniversary_checks_if_date_matches_today():
    with patch("pendulum.Date.today", return_value=Date(2023, 1, 1)):
        anniversary_date = Date(2022, 1, 1)
        assert anniversary_date.is_anniversary()