import pytest

from main import format_api_date


def test_formats_valid_iso_date():
    assert format_api_date("2026-09-16T09:00:00.000Z") == "16/09 09:00 AM"


def test_formats_iso_with_offset():
    assert format_api_date("2026-09-16T21:30:00.000+00:00") == "16/09 09:30 PM"


@pytest.mark.parametrize("invalid", ["garbage", "", "2026-13-99"])
def test_returns_input_unchanged_for_invalid_dates(invalid):
    assert format_api_date(invalid) == invalid