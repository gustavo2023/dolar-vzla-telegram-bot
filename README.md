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

The workflow runs every 15 minutes on a cron schedule, but the bot only sends a message when the current time in Venezuela (UTC-4) falls inside a send window: the first 15 minutes of 9:00 AM or 5:00 PM VET. This window-based gate self-corrects GitHub Actions scheduling delays and prevents duplicate sends.

**Default Schedule (Venezuela Time UTC-4):**

- 9:00–9:15 AM VET (13:00–13:15 UTC)
- 5:00–5:15 PM VET (21:00–21:15 UTC)

To change this, edit the cron line in the workflow file (the send windows themselves are configured in `main.py`):

```yaml
- cron: "*/15 * * * *"
```

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
