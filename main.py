import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
import telebot

# Configuration
API_URL = "https://ve.dolarapi.com/v1/dolares"
VZLA_TZ = ZoneInfo("America/Caracas")
SEND_HOURS = (9, 17)
SEND_WINDOW_MINUTES = 15
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def get_exchange_rates():
    """Fetches exchange rates from DolarAPI."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def format_message(data):
    """Formats the exchange rate data into a readable message."""
    if not data:
        return "Error: Could not retrieve exchange rates."

    # Find specific rates in the list
    bcv_rate = next((item for item in data if item["fuente"] == "oficial"), None)
    parallel_rate = next((item for item in data if item["fuente"] == "paralelo"), None)

    # Get current time in Venezuela
    date_str = datetime.now(VZLA_TZ).strftime("%d/%m/%Y %I:%M %p")

    message = f"💰 *Reporte del Dólar - {date_str}*\n\n"

    if bcv_rate:
        message += f"🏛 *BCV (Oficial):* Bs. {bcv_rate['promedio']}\n"
        message += (
            f"   _Actualizado: {format_api_date(bcv_rate['fechaActualizacion'])}_\n\n"
        )

    if parallel_rate:
        message += f"💸 *Paralelo:* Bs. {parallel_rate['promedio']}\n"
        message += f"   _Actualizado: {format_api_date(parallel_rate['fechaActualizacion'])}_\n"

    message += "\n_Datos obtenidos de DolarAPI_"
    return message


def format_api_date(date_string):
    """Helper to format the API date string to something more readable."""
    try:
        # API returns ISO format like "2023-10-27T09:00:00.000Z"
        dt = datetime.fromisoformat(date_string)
        return dt.strftime("%d/%m %I:%M %p")
    except ValueError:
        return date_string


def send_telegram_message(message):
    """Sends the formatted message to the configured Telegram chat."""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_TOKEN or CHAT_ID not found in environment variables.")
        return

    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    try:
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")
        print("Message sent successfully!")
    except (telebot.apihelper.ApiTelegramException, requests.RequestException) as e:
        print(f"Error sending message: {e}")


def in_send_window(now):
    """True when the current VET time is inside a send window."""
    return now.hour in SEND_HOURS and now.minute < SEND_WINDOW_MINUTES


def main():
    print("Starting bot execution...")
    now = datetime.now(VZLA_TZ)
    if not in_send_window(now):
        print(f"Outside send window ({now.strftime('%H:%M')}); skipping.")
        return

    data = get_exchange_rates()
    if data:
        message = format_message(data)
        print("Generated Message:")
        print(message)
        send_telegram_message(message)
    else:
        print("No data to send.")
    print("Execution finished.")


if __name__ == "__main__":
    main()
