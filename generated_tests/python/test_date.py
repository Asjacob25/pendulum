import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from datetime import date, timedelta
from pendulum.date import Date
from pendulum.exceptions import PendulumException
import calendar
import pendulum

# Fixtures for common dates
@pytest.fixture(scope="module")
def leap_year_date():
    return Date(2020, 2, 29)

@pytest.fixture(scope="module")
def non_leap_year_date():
    return Date(2021, 3, 1)

@pytest.fixture(scope="module")
def new_year_date():
    return Date(2023, 1, 1)

@pytest.fixture(scope="module")
def end_of_year_date():
    return Date(2023, 12, 31)

# Test Cases
def test_day_of_week(leap_year_date):
    assert leap_year_date.day_of_week == pendulum.SATURDAY

def test_day_of_year_non_leap_year(non_leap_year_date):
    assert non_leap_year_date.day_of_year == 60

def test_day_of_year_leap_year(leap_year_date):
    assert leap_year_date.day_of_year == 60

def test_week_of_year_new_year(new_year_date):
    assert new_year_date.week_of_year == 1

def test_days_in_month_february_leap_year(leap_year_date):
    assert leap_year_date.days_in_month == 29

def test_days_in_month_february_non_leap_year(non_leap_year_date):
    assert non_leap_year_date.days_in_month == 28

def test_week_of_month_first_day(new_year_date):
    assert new_year_date.week_of_month == 1

def test_age_on_birthday():
    birthdate = Date(2000, 1, 1)
    with pendulum.test(Date(2020, 1, 1)):
        assert birthdate.age == 20

def test_is_future_with_future_date():
    future_date = Date.today().add(days=1)
    assert future_date.is_future()

def test_is_past_with_past_date():
    past_date = Date.today().subtract(days=1)
    assert past_date.is_past()

def test_set_year(new_year_date):
    modified_date = new_year_date.set(year=2022)
    assert modified_date.year == 2022

def test_add_years(new_year_date):
    future_date = new_year_date.add(years=2)
    assert future_date.year == 2025

def test_subtract_days(new_year_date):
    past_date = new_year_date.subtract(days=1)
    assert past_date == Date(2022, 12, 31)

def test_to_date_string(new_year_date):
    assert new_year_date.to_date_string() == "2023-01-01"

def test_to_formatted_date_string(new_year_date):
    assert new_year_date.to_formatted_date_string() == "Jan 01, 2023"

def test_closest_future_date():
    base_date = Date(2023, 1, 1)
    future_date1 = Date(2023, 1, 10)
    future_date2 = Date(2023, 2, 1)
    assert base_date.closest(future_date1, future_date2) == future_date1

def test_farther_future_date():
    base_date = Date(2023, 1, 1)
    future_date1 = Date(2023, 1, 10)
    future_date2 = Date(2023, 2, 1)
    assert base_date.farthest(future_date1, future_date2) == future_date2

def test_diff_for_humans_with_future_date():
    base_date = Date.today()
    future_date = base_date.add(days=5)
    assert "5 days" in future_date.diff_for_humans(base_date)

def test_is_leap_year_with_leap_year(leap_year_date):
    assert leap_year_date.is_leap_year()

def test_is_not_leap_year_with_non_leap_year(non_leap_year_date):
    assert not non_leap_year_date.is_leap_year()

def test_invalid_unit_for_start_of_raises_error(new_year_date):
    with pytest.raises(ValueError):
        new_year_date.start_of("hour")

def test_invalid_unit_for_end_of_raises_error(new_year_date):
    with pytest.raises(ValueError):
        new_year_date.end_of("minute")

def test_addition_with_timedelta(new_year_date):
    result_date = new_year_date + timedelta(days=30)
    assert result_date == Date(2023, 1, 31)

def test_subtraction_with_timedelta(new_year_date):
    result_date = new_year_date - timedelta(days=1)
    assert result_date == Date(2022, 12, 31)

def test_diff_returns_interval(new_year_date, end_of_year_date):
    interval = new_year_date.diff(end_of_year_date)
    assert interval.in_days() == 364  # Considering non-leap year for simplicity

def test_today_returns_current_date(mocker):
    mocker.patch('pendulum.date.Date.today', return_value=Date(2023, 1, 1))
    assert Date.today() == Date(2023, 1, 1)