from unittest.mock import patch

import main


def test_skips_fetch_outside_window(capsys):
    with (
        patch("main.in_send_window", return_value=False),
        patch("main.get_exchange_rates") as mock_get,
        patch("main.send_telegram_message") as mock_send,
    ):
        main.main()
    mock_get.assert_not_called()
    mock_send.assert_not_called()
    assert "Outside send window" in capsys.readouterr().out


def test_sends_message_inside_window(rates_payload):
    with (
        patch("main.in_send_window", return_value=True),
        patch("main.get_exchange_rates", return_value=rates_payload),
        patch("main.send_telegram_message") as mock_send,
    ):
        main.main()
    mock_send.assert_called_once()
    message = mock_send.call_args[0][0]
    assert "Reporte del Dólar" in message
    assert "BCV (Oficial)" in message


def test_does_not_send_when_no_data(capsys):
    with (
        patch("main.in_send_window", return_value=True),
        patch("main.get_exchange_rates", return_value=None),
        patch("main.send_telegram_message") as mock_send,
    ):
        main.main()
    mock_send.assert_not_called()
    assert "No data to send." in capsys.readouterr().out