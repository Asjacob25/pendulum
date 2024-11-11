import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pytest
from src.pendulum import constants

def test_years_per_century():
    assert constants.YEARS_PER_CENTURY == 100

def test_years_per_decade():
    assert constants.YEARS_PER_DECADE == 10

def test_months_per_year():
    assert constants.MONTHS_PER_YEAR == 12

def test_weeks_per_year():
    assert constants.WEEKS_PER_YEAR == 52

def test_days_per_week():
    assert constants.DAYS_PER_WEEK == 7

def test_hours_per_day():
    assert constants.HOURS_PER_DAY == 24

def test_minutes_per_hour():
    assert constants.MINUTES_PER_HOUR == 60

def test_seconds_per_minute():
    assert constants.SECONDS_PER_MINUTE == 60

def test_seconds_per_hour():
    assert constants.SECONDS_PER_HOUR == 3600

def test_seconds_per_day():
    assert constants.SECONDS_PER_DAY == 86400

def test_microseconds_per_second():
    assert constants.US_PER_SECOND == 1000000

def test_epoch_year():
    assert constants.EPOCH_YEAR == 1970

def test_days_per_normal_year():
    assert constants.DAYS_PER_N_YEAR == 365

def test_days_per_leap_year():
    assert constants.DAYS_PER_L_YEAR == 366

def test_microseconds_per_second():
    assert constants.USECS_PER_SEC == 1000000

def test_seconds_per_minute_alias():
    assert constants.SECS_PER_MIN == 60

def test_seconds_per_hour_alias():
    assert constants.SECS_PER_HOUR == 3600

def test_seconds_per_day_alias():
    assert constants.SECS_PER_DAY == 86400

def test_seconds_per_400_years():
    assert constants.SECS_PER_400_YEARS == 146097 * constants.SECS_PER_DAY

def test_seconds_per_100_years():
    non_leap, leap = constants.SECS_PER_100_YEARS
    assert non_leap == (76 * constants.DAYS_PER_N_YEAR + 24 * constants.DAYS_PER_L_YEAR) * constants.SECS_PER_DAY
    assert leap == (75 * constants.DAYS_PER_N_YEAR + 25 * constants.DAYS_PER_L_YEAR) * constants.SECS_PER_DAY

def test_seconds_per_4_years():
    non_leap, leap = constants.SECS_PER_4_YEARS
    assert non_leap == (4 * constants.DAYS_PER_N_YEAR + 0) * constants.SECS_PER_DAY
    assert leap == (3 * constants.DAYS_PER_N_YEAR + constants.DAYS_PER_L_YEAR) * constants.SECS_PER_DAY

def test_seconds_per_year():
    non_leap, leap = constants.SECS_PER_YEAR
    assert non_leap == constants.DAYS_PER_N_YEAR * constants.SECS_PER_DAY
    assert leap == constants.DAYS_PER_L_YEAR * constants.SECS_PER_DAY

def test_days_per_year():
    non_leap, leap = constants.DAYS_PER_YEAR
    assert non_leap == constants.DAYS_PER_N_YEAR
    assert leap == constants.DAYS_PER_L_YEAR

def test_days_per_months():
    non_leap, leap = constants.DAYS_PER_MONTHS
    assert non_leap[2] == 28
    assert leap[2] == 29

def test_months_offsets():
    non_leap, leap = constants.MONTHS_OFFSETS
    assert non_leap[-1] == 365
    assert leap[-1] == 366

@pytest.mark.parametrize("day,expected", [
    (0, constants.TM_SUNDAY),
    (1, constants.TM_MONDAY),
    (6, constants.TM_SATURDAY),
])
def test_day_of_week_table(day, expected):
    assert constants.DAY_OF_WEEK_TABLE[day] == expected

@pytest.mark.parametrize("month,expected", [
    (0, constants.TM_JANUARY),
    (11, constants.TM_DECEMBER),
])
def test_month_constants(month, expected):
    assert month == expected