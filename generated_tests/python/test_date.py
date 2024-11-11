import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from datetime import date, timedelta
import pendulum
from pendulum.date import Date
from pendulum.exceptions import PendulumException

@pytest.fixture
def setup_date():
    """Fixture for setting up a Date instance."""
    return Date(2023, 1, 1)

def test_set_new_date(setup_date):
    """Test setting a new date."""
    new_date = setup_date.set(2024, 12, 31)
    assert new_date.year == 2024
    assert new_date.month == 12
    assert new_date.day == 31

def test_day_of_week(setup_date):
    """Test day of the week."""
    assert setup_date.day_of_week == pendulum.SUNDAY

def test_day_of_year(setup_date):
    """Test day of the year."""
    assert setup_date.day_of_year == 1

def test_week_of_year(setup_date):
    """Test week of the year."""
    assert setup_date.week_of_year == 52

def test_days_in_month(setup_date):
    """Test days in the month."""
    assert setup_date.days_in_month == 31

def test_week_of_month(setup_date):
    """Test week of month."""
    assert setup_date.week_of_month == 1

def test_age(setup_date, mocker):
    """Test age."""
    mocker.patch.object(Date, 'today', return_value=Date(2024, 1, 1))
    assert setup_date.age == 1

def test_quarter(setup_date):
    """Test quarter."""
    assert setup_date.quarter == 1

def test_to_date_string(setup_date):
    """Test conversion to date string."""
    assert setup_date.to_date_string() == "2023-01-01"

def test_to_formatted_date_string(setup_date):
    """Test conversion to formatted date string."""
    assert setup_date.to_formatted_date_string() == "Jan 01, 2023"

def test_closest(setup_date):
    """Test finding the closest date."""
    dt1 = Date(2022, 12, 31)
    dt2 = Date(2023, 1, 2)
    assert setup_date.closest(dt1, dt2) == dt1

def test_farthest(setup_date):
    """Test finding the farthest date."""
    dt1 = Date(2022, 12, 31)
    dt2 = Date(2023, 1, 2)
    assert setup_date.farthest(dt1, dt2) == dt2

def test_is_future(setup_date, mocker):
    """Test if date is in the future."""
    mocker.patch.object(Date, 'today', return_value=Date(2022, 12, 31))
    assert setup_date.is_future()

def test_is_past(setup_date, mocker):
    """Test if date is in the past."""
    mocker.patch.object(Date, 'today', return_value=Date(2023, 1, 2))
    assert setup_date.is_past()

def test_is_leap_year(setup_date):
    """Test if year is a leap year."""
    assert not setup_date.is_leap_year()

def test_is_long_year(setup_date):
    """Test if year is a long year."""
    assert not setup_date.is_long_year()

def test_is_same_day(setup_date):
    """Test if it's the same day."""
    dt = Date(2023, 1, 1)
    assert setup_date.is_same_day(dt)

def test_is_anniversary(setup_date, mocker):
    """Test if it's the anniversary."""
    mocker.patch.object(Date, 'today', return_value=Date(2024, 1, 1))
    assert setup_date.is_anniversary()

def test_add_years(setup_date):
    """Test adding years."""
    new_date = setup_date.add(years=1)
    assert new_date.year == 2024

def test_subtract_years(setup_date):
    """Test subtracting years."""
    new_date = setup_date.subtract(years=1)
    assert new_date.year == 2022

def test_add_months_edge_case(setup_date):
    """Test adding months at edge case."""
    new_date = setup_date.add(months=11)
    assert new_date.month == 12

def test_subtract_months_edge_case(setup_date):
    """Test subtracting months at edge case."""
    new_date = setup_date.subtract(months=1)
    assert new_date.month == 12
    assert new_date.year == 2022

def test_addition_with_timedelta(setup_date):
    """Test addition with timedelta."""
    new_date = setup_date + timedelta(days=1)
    assert new_date.day == 2

def test_subtraction_with_timedelta(setup_date):
    """Test subtraction with timedelta."""
    new_date = setup_date - timedelta(days=1)
    assert new_date.day == 31
    assert new_date.month == 12
    assert new_date.year == 2022

def test_diff(setup_date):
    """Test difference between two dates."""
    dt = Date(2023, 1, 2)
    assert setup_date.diff(dt).in_days() == 1

def test_invalid_unit_start_of(setup_date):
    """Test invalid unit for start_of method."""
    with pytest.raises(ValueError):
        setup_date.start_of('invalid_unit')

def test_invalid_unit_end_of(setup_date):
    """Test invalid unit for end_of method."""
    with pytest.raises(ValueError):
        setup_date.end_of('invalid_unit')

@pytest.mark.parametrize("unit", ['day', 'month', 'year', 'decade', 'century'])
def test_start_of_valid_units(setup_date, unit):
    """Test start_of method with valid units."""
    assert isinstance(setup_date.start_of(unit), Date)

@pytest.mark.parametrize("unit", ['month', 'year', 'decade', 'century'])
def test_end_of_valid_units(setup_date, unit):
    """Test end_of method with valid units."""
    assert isinstance(setup_date.end_of(unit), Date)