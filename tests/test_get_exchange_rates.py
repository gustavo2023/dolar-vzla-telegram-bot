from unittest.mock import Mock, patch

import requests

from main import get_exchange_rates


def test_returns_data_on_success():
    expected = [{"fuente": "oficial", "promedio": 36.5}]
    mock_response = Mock()
    mock_response.json.return_value = expected
    with patch("main.requests.get", return_value=mock_response) as mock_get:
        assert get_exchange_rates() == expected
    mock_get.assert_called_once_with(
        "https://ve.dolarapi.com/v1/dolares", timeout=10
    )


def test_returns_none_on_request_error(capsys):
    with patch("main.requests.get", side_effect=requests.RequestException("boom")):
        assert get_exchange_rates() is None
    assert "Error fetching data: boom" in capsys.readouterr().out


def test_returns_none_on_http_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500")
    with patch("main.requests.get", return_value=mock_response):
        assert get_exchange_rates() is None