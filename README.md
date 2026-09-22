# 🇻🇪 Dolar Venezuela Telegram Bot

A lightweight, serverless Telegram bot that automatically sends daily reports of the official (BCV) and parallel dollar exchange rates in Venezuela.

Powered by [DolarAPI](https://dolarapi.com/docs/venezuela/) and GitHub Actions.

## 🚀 Features

- **Automated Reports:** Sends updates twice a day (9:00 AM and 5:00 PM VET).
- **Zero Cost:** Runs entirely on GitHub Actions Free Tier (no VPS or hosting required).
- **Dual Rates:** Fetches both the Official (BCV) and Parallel average rates.
- **Timezone Aware:** Correctly handles Venezuela Standard Time (UTC-4).

## 🛠️ Prerequisites

Before setting up the repository, you need two things from Telegram:

1. **Telegram Bot Token:**

    - Chat with `@BotFather`.
    - Send `/newbot` and follow the instructions.
    - Copy the HTTP API Token.

2. **Your Chat ID:**
    - Chat with `@userinfobot` (or add your new bot to a group and get the group ID).
    - Copy the numeric ID (e.g., `12345678`).

## ⚙️ Installation & Setup

### 1. Repository Setup

Fork or Clone this repository.
Ensure you have the following files:

- `main.py` (The logic script)
- `pyproject.toml` + `uv.lock` (Dependencies, managed with [uv](https://docs.astral.sh/uv/))
- `.github/workflows/bot_schedule.yml` (Automation schedule)

### 2. Configure Secrets

To keep your tokens safe, do not put them in the code. Use GitHub Secrets:

1. Go to your Repository **Settings**.
2. On the left sidebar, click **Secrets and variables** > **Actions**.
3. Click **New repository secret** and add:
    - Name: `TELEGRAM_TOKEN` -> Value: `Your_Token_From_BotFather`
    - Name: `CHAT_ID` -> Value: `Your_User_Or_Group_ID`

### 3. Activate

Once the secrets are set and the code is pushed to the `main` branch, the bot is active.

To test it immediately: Go to the **Actions** tab in GitHub, select **Run DolarVzlaBot**, and click **Run workflow**.

## ⏰ Schedule Configuration

The workflow is scheduled twice a day, and the bot sends a message only when it runs during the 9:00 AM or 5:00 PM hour in Venezuela (UTC-4). The hour-wide gate absorbs GitHub Actions start delays (scheduled runs can begin tens of minutes late) and blocks accidental manual sends outside those hours.

**Default Schedule (Venezuela Time UTC-4):**

- 9:00–9:59 AM VET (13:00–13:59 UTC)
- 5:00–5:59 PM VET (21:00–21:59 UTC)

To change the send hours, edit `SEND_HOURS` in `main.py`; to change the workflow trigger, edit the cron line:

```yaml
- cron: "0 13,21 * * *"
```

Keep the cron at a low frequency: GitHub Actions heavily throttles high-frequency schedules (a `*/15` cron was observed firing only ~7 times a day instead of 96), so extra ticks cannot be relied on to catch delayed sends.

## 📂 File Structure

```bash
.
├── .github/
│   └── workflows/
│       └── bot_schedule.yml  # GitHub Actions configuration
├── main.py                   # Python script to fetch data and send message
├── pyproject.toml            # Project metadata and dependencies
├── uv.lock                   # Locked dependency versions
└── README.md                 # This file
```

## ⚠️ Disclaimer

This project uses public APIs provided by third parties. The accuracy of the exchange rates depends entirely on [DolarAPI](https://dolarapi.com/docs/venezuela/). This tool is for informational purposes only.
