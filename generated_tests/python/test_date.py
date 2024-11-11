import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from datetime import date, timedelta
from pendulum import Date, PendulumException, WeekDay

@pytest.fixture
def setup_date():
    # Setup code if needed
    yield Date(2023, 1, 1)
    # Teardown code if needed

def test_set_new_date(setup_date):
    new_date = setup_date.set(2023, 2, 2)
    assert new_date.year == 2023
    assert new_date.month == 2
    assert new_date.day == 2

def test_day_of_week(setup_date):
    assert setup_date.day_of_week == WeekDay.SUNDAY

def test_day_of_year(setup_date):
    assert setup_date.day_of_year == 1

def test_week_of_year(setup_date):
    assert setup_date.week_of_year == 52

def test_days_in_month(setup_date):
    assert setup_date.days_in_month == 31

def test_week_of_month(setup_date):
    setup_date = Date(2023, 1, 31)
    assert setup_date.week_of_month == 5

def test_age_future_date():
    future_date = Date(2025, 1, 1)
    with pytest.raises(PendulumException):
        future_date.age

def test_quarter(setup_date):
    assert setup_date.quarter == 1

def test_to_date_string(setup_date):
    assert setup_date.to_date_string() == "2023-01-01"

def test_to_formatted_date_string(setup_date):
    assert setup_date.to_formatted_date_string() == "Jan 01, 2023"

def test_closest(setup_date):
    dt1 = date(2023, 2, 2)
    dt2 = date(2023, 1, 15)
    assert setup_date.closest(dt1, dt2) == Date(2023, 1, 15)

def test_farthest(setup_date):
    dt1 = date(2023, 2, 2)
    dt2 = date(2023, 1, 15)
    assert setup_date.farthest(dt1, dt2) == Date(2023, 2, 2)

def test_is_future(setup_date):
    assert not setup_date.is_future()

def test_is_past(setup_date):
    past_date = Date(2020, 1, 1)
    assert past_date.is_past()

def test_is_leap_year():
    leap_year_date = Date(2024, 1, 1)
    assert leap_year_date.is_leap_year()

def test_is_same_day(setup_date):
    same_day = date(2023, 1, 1)
    assert setup_date.is_same_day(same_day)

def test_is_anniversary(setup_date):
    assert setup_date.is_anniversary(date(2024, 1, 1))

def test_addition(setup_date):
    added_date = setup_date.add(years=1, months=1, days=1)
    assert added_date == Date(2024, 2, 2)

def test_subtraction(setup_date):
    subtracted_date = setup_date.subtract(years=1, months=1, days=1)
    assert subtracted_date == Date(2021, 11, 30)

def test_add_timedelta(setup_date):
    added_date = setup_date + timedelta(days=1)
    assert added_date == Date(2023, 1, 2)

def test_subtract_timedelta(setup_date):
    subtracted_date = setup_date - timedelta(days=1)
    assert subtracted_date == Date(2022, 12, 31)

def test_diff(setup_date):
    other_date = Date(2023, 1, 2)
    assert setup_date.diff(other_date).in_days() == 1

def test_diff_for_humans(setup_date):
    other_date = Date(2023, 1, 2)
    assert setup_date.diff_for_humans(other_date) == "1 day before"

def test_start_of(setup_date):
    start_of_month = setup_date.start_of('month')
    assert start_of_month == Date(2023, 1, 1)

def test_end_of(setup_date):
    end_of_month = setup_date.end_of('month')
    assert end_of_month == Date(2023, 1, 31)

def test_invalid_start_of_unit(setup_date):
    with pytest.raises(ValueError):
        setup_date.start_of('invalid_unit')

def test_invalid_end_of_unit(setup_date):
    with pytest.raises(ValueError):
        setup_date.end_of('invalid_unit')

def test_today():
    today = Date.today()
    assert today == Date(date.today().year, date.today().month, date.today().day)

def test_fromtimestamp():
    timestamp_date = Date.fromtimestamp(1609459200)  # 2021-01-01 00:00:00 UTC
    assert timestamp_date == Date(2021, 1, 1)

def test_fromordinal():
    ordinal_date = Date.fromordinal(737791)  # 2021-01-01
    assert ordinal_date == Date(2021, 1, 1)

def test_replace(setup_date):
    replaced_date = setup_date.replace(year=2024)
    assert replaced_date.year == 2024
    assert replaced_date.month == 1
    assert replaced_date.day == 1