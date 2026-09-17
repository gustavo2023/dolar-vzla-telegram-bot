from unittest.mock import Mock, patch

import requests
from telebot.apihelper import ApiTelegramException

import main


def test_skips_send_without_env_vars(monkeypatch, capsys):
    monkeypatch.setattr(main, "TELEGRAM_TOKEN", None)
    monkeypatch.setattr(main, "CHAT_ID", None)
    with patch("main.telebot.TeleBot") as mock_bot:
        main.send_telegram_message("hola")
    mock_bot.assert_not_called()
    assert "not found in environment variables" in capsys.readouterr().out


def test_sends_message_with_markdown(monkeypatch):
    monkeypatch.setattr(main, "TELEGRAM_TOKEN", "token")
    monkeypatch.setattr(main, "CHAT_ID", "123")
    mock_bot = Mock()
    with patch("main.telebot.TeleBot", return_value=mock_bot):
        main.send_telegram_message("mensaje")
    mock_bot.send_message.assert_called_once_with(
        "123", "mensaje", parse_mode="Markdown"
    )


def test_handles_telegram_api_error(monkeypatch, capsys):
    monkeypatch.setattr(main, "TELEGRAM_TOKEN", "token")
    monkeypatch.setattr(main, "CHAT_ID", "123")
    mock_bot = Mock()
    mock_bot.send_message.side_effect = ApiTelegramException(
        "send_message",
        None,
        {"error_code": 400, "description": "Bad Request"},
    )
    with patch("main.telebot.TeleBot", return_value=mock_bot):
        main.send_telegram_message("mensaje")
    assert "Error sending message" in capsys.readouterr().out


def test_handles_network_error(monkeypatch, capsys):
    monkeypatch.setattr(main, "TELEGRAM_TOKEN", "token")
    monkeypatch.setattr(main, "CHAT_ID", "123")
    mock_bot = Mock()
    mock_bot.send_message.side_effect = requests.RequestException("timeout")
    with patch("main.telebot.TeleBot", return_value=mock_bot):
        main.send_telegram_message("mensaje")
    assert "Error sending message: timeout" in capsys.readouterr().out