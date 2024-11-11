import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from datetime import date, timedelta
from pendulum import Date, WeekDay
from pendulum.exceptions import PendulumException

@pytest.fixture
def setup_date():
    return Date(2022, 1, 1)  # A fixed date to use across tests

# Test success scenarios

def test_set_new_date(setup_date):
    new_date = setup_date.set(2023, 12, 31)
    assert new_date.year == 2023
    assert new_date.month == 12
    assert new_date.day == 31

def test_day_of_week(setup_date):
    assert setup_date.day_of_week == WeekDay.SATURDAY

def test_day_of_year(setup_date):
    assert setup_date.day_of_year == 1

def test_week_of_year(setup_date):
    assert setup_date.week_of_year == 52

def test_days_in_month(setup_date):
    assert setup_date.days_in_month == 31

def test_week_of_month(setup_date):
    assert setup_date.week_of_month == 1

def test_age(setup_date, mocker):
    mocker.patch('pendulum.date.Date.today', return_value=Date(2023, 1, 1))
    assert setup_date.age == 1

def test_quarter(setup_date):
    assert setup_date.quarter == 1

def test_to_date_string(setup_date):
    assert setup_date.to_date_string() == "2022-01-01"

def test_to_formatted_date_string(setup_date):
    assert setup_date.to_formatted_date_string() == "Jan 01, 2022"

def test_closest(setup_date):
    dt1 = Date(2022, 1, 2)
    dt2 = Date(2022, 1, 10)
    assert setup_date.closest(dt1, dt2) == dt1

def test_farthest(setup_date):
    dt1 = Date(2022, 1, 2)
    dt2 = Date(2022, 1, 10)
    assert setup_date.farthest(dt1, dt2) == dt2

def test_is_future(setup_date, mocker):
    mocker.patch('pendulum.date.Date.today', return_value=Date(2021, 12, 31))
    assert setup_date.is_future() is True

def test_is_past(setup_date, mocker):
    mocker.patch('pendulum.date.Date.today', return_value=Date(2023, 1, 1))
    assert setup_date.is_past() is True

def test_is_leap_year(setup_date):
    assert setup_date.is_leap_year() is False

def test_is_long_year(setup_date):
    assert setup_date.is_long_year() is False

def test_is_same_day(setup_date):
    assert setup_date.is_same_day(Date(2022, 1, 1)) is True

def test_is_anniversary(setup_date, mocker):
    mocker.patch('pendulum.date.Date.today', return_value=Date(2023, 1, 1))
    assert setup_date.is_anniversary() is True

def test_addition(setup_date):
    new_date = setup_date.add(years=1, months=1, days=1)
    assert new_date == Date(2023, 2, 2)

def test_subtraction(setup_date):
    new_date = setup_date.subtract(years=1, months=1, days=1)
    assert new_date == Date(2020, 11, 30)

def test_diff(setup_date):
    other_date = Date(2023, 1, 1)
    interval = setup_date.diff(other_date)
    assert interval.in_days() == -365

def test_diff_for_humans(setup_date, mocker):
    mocker.patch('pendulum.format_diff', return_value='1 year ago')
    other_date = Date(2023, 1, 1)
    assert setup_date.diff_for_humans(other_date) == '1 year ago'

# Test failure scenarios

def test_invalid_unit_start_of(setup_date):
    with pytest.raises(ValueError):
        setup_date.start_of('invalid')

def test_invalid_unit_end_of(setup_date):
    with pytest.raises(ValueError):
        setup_date.end_of('invalid')

def test_invalid_day_of_week_next(setup_date):
    with pytest.raises(ValueError):
        setup_date.next(7)  # 7 is not a valid WeekDay

def test_invalid_day_of_week_previous(setup_date):
    with pytest.raises(ValueError):
        setup_date.previous(-1)  # -1 is not a valid WeekDay

def test_add_timedelta(setup_date):
    delta = timedelta(days=10)
    new_date = setup_date + delta
    assert new_date == Date(2022, 1, 11)

def test_subtract_timedelta(setup_date):
    delta = timedelta(days=10)
    new_date = setup_date - delta
    assert new_date == Date(2021, 12, 22)

def test_invalid_unit_first_of(setup_date):
    with pytest.raises(ValueError):
        setup_date.first_of('invalid')

def test_invalid_unit_last_of(setup_date):
    with pytest.raises(ValueError):
        setup_date.last_of('invalid')

def test_invalid_unit_nth_of(setup_date):
    with pytest.raises(PendulumException):
        setup_date.nth_of('month', 5, WeekDay.MONDAY)