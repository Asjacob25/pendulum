import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from datetime import date, timedelta
from pendulum import Date, PendulumException, WeekDay
import calendar

# Fixtures for setup and teardown if needed, mocking external dependencies
@pytest.fixture
def mock_today(monkeypatch):
    class MockDate(Date):
        @classmethod
        def today(cls):
            return cls(2023, 1, 1)  # Mocking today's date as January 1st, 2023

    monkeypatch.setattr("src.pendulum.date.Date.today", MockDate.today)


# Test Cases

def test_set_success():
    """Test setting date attributes successfully."""
    d = Date(2023, 1, 1)
    new_date = d.set(2024, 2, 2)
    assert new_date.year == 2024
    assert new_date.month == 2
    assert new_date.day == 2

def test_day_of_week():
    """Test day_of_week property."""
    d = Date(2023, 1, 1) # Sunday
    assert d.day_of_week == WeekDay.SUNDAY

def test_day_of_year():
    """Test day_of_year property."""
    d = Date(2023, 1, 1)
    assert d.day_of_year == 1  # First day of the year

def test_week_of_year():
    """Test week_of_year property."""
    d = Date(2023, 1, 1)
    assert d.week_of_year == 52  # First day of 2023 falls in the last week of 2022

def test_days_in_month():
    """Test days_in_month property."""
    d = Date(2023, 2, 1)  # February of a non-leap year
    assert d.days_in_month == 28

def test_week_of_month():
    """Test week_of_month property."""
    d = Date(2023, 1, 1)
    assert d.week_of_month == 1

def test_age(mock_today):
    """Test age property."""
    birthday = Date(2000, 1, 1)
    assert birthday.age == 23  # Mocking today as 2023, January 1st

def test_quarter():
    """Test quarter property."""
    d = Date(2023, 4, 1)
    assert d.quarter == 2

def test_to_date_string():
    """Test to_date_string method."""
    d = Date(2023, 1, 1)
    assert d.to_date_string() == "2023-01-01"

def test_to_formatted_date_string():
    """Test to_formatted_date_string method."""
    d = Date(2023, 1, 1)
    assert d.to_formatted_date_string() == "Jan 01, 2023"

def test_closest():
    """Test closest method."""
    base_date = Date(2023, 1, 15)
    assert base_date.closest(Date(2023, 1, 10), Date(2023, 1, 20)) == Date(2023, 1, 10)

def test_farthest():
    """Test farthest method."""
    base_date = Date(2023, 1, 15)
    assert base_date.farthest(Date(2023, 1, 10), Date(2023, 1, 20)) == Date(2023, 1, 20)

def test_is_future(mock_today):
    """Test is_future method."""
    future_date = Date(2023, 2, 1)
    assert future_date.is_future() == True

def test_is_past(mock_today):
    """Test is_past method."""
    past_date = Date(2022, 12, 31)
    assert past_date.is_past() == True

def test_is_leap_year():
    """Test is_leap_year method."""
    leap_year = Date(2024, 1, 1)
    assert leap_year.is_leap_year() == True

def test_is_long_year():
    """Test is_long_year method."""
    long_year = Date(2020, 1, 1)  # 2020 is a long year
    assert long_year.is_long_year() == True

def test_add():
    """Test adding years, months, weeks, and days."""
    d = Date(2023, 1, 1)
    new_date = d.add(years=1, months=1, weeks=1, days=1)
    assert new_date == Date(2024, 2, 9)

def test_subtract():
    """Test subtracting years, months, weeks, and days."""
    d = Date(2023, 1, 1)
    new_date = d.subtract(years=1, months=1, weeks=1, days=1)
    # Expected date is 2021-11-24 because November of 2021 has 30 days
    assert new_date == Date(2021, 11, 24)

def test_diff_for_humans(mock_today):
    """Test diff_for_humans method."""
    past_date = Date(2022, 12, 25)  # Mocking today as 2023, January 1st
    assert past_date.diff_for_humans() == "1 week ago"

def test_start_of_month():
    """Test start_of_month modifier."""
    d = Date(2023, 1, 15)
    assert d.start_of('month') == Date(2023, 1, 1)

def test_end_of_month():
    """Test end_of_month modifier."""
    d = Date(2023, 2, 15)
    assert d.end_of('month') == Date(2023, 2, 28)  # February in a non-leap year

@pytest.mark.parametrize("date_input,expected_exception", [
    (Date(2023, 2, 29), ValueError),  # Test invalid date for non-leap year
    ("not a date", TypeError),  # Test passing non-date type
])
def test_invalid_date_inputs(date_input, expected_exception):
    """Test handling of invalid date inputs."""
    with pytest.raises(expected_exception):
        Date(date_input)

def test_invalid_unit_start_of():
    """Test start_of with invalid unit."""
    d = Date(2023, 1, 1)
    with pytest.raises(ValueError):
        d.start_of('invalid_unit')

def test_invalid_unit_end_of():
    """Test end_of with invalid unit."""
    d = Date(2023, 1, 1)
    with pytest.raises(ValueError):
        d.end_of('invalid_unit')