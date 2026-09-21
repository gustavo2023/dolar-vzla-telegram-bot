from datetime import datetime

import pytest

from main import VZLA_TZ, in_send_window


@pytest.mark.parametrize(("hour", "minute"), [(9, 0), (9, 44), (17, 0), (17, 44)])
def test_in_window(hour, minute):
    assert in_send_window(datetime(2026, 9, 16, hour, minute, tzinfo=VZLA_TZ))


@pytest.mark.parametrize(
    ("hour", "minute"),
    [(9, 45), (9, 59), (17, 45), (12, 0), (8, 59), (16, 59)],
)
def test_outside_window(hour, minute):
    assert not in_send_window(datetime(2026, 9, 16, hour, minute, tzinfo=VZLA_TZ))