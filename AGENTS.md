# AGENTS.md

Single-file Python Telegram bot (`main.py`) that posts USD exchange rates from DolarAPI to a Telegram chat, run only via GitHub Actions schedule. Managed with `uv` (`pyproject.toml` + `uv.lock`), Python 3.11. No test suite, linter, or formatter is configured.

## Run locally

```bash
TELEGRAM_TOKEN=<token> CHAT_ID=<chat-id> uv run python main.py
```

`uv sync` first if `uv.lock` changed. `TELEGRAM_TOKEN` and `CHAT_ID` come from GitHub Secrets (see `.github/workflows/bot_schedule.yml`); the script does not fail without them — it silently skips sending (`main.py:68`). `get_exchange_rates` needs no env vars.

**Send-window guard:** `main()` exits without fetching unless the current `America/Caracas` time is inside a send window — first 45 minutes of 09:00 or 17:00 (`in_send_window`, `main.py:80`). Running it at any other time just prints `Outside send window (...); skipping.`. To see the fetch/message path locally, run it during a window (or call `get_exchange_rates`/`format_message` directly from a REPL).

## Structure / flow

- `main.py` is the whole app: fetch rates from `https://ve.dolarapi.com/v1/dolares` → filter entries by `fuente == "oficial"` and `"paralelo"` → use their `promedio` field → send via pyTelegramBotAPI with Markdown parse mode.
- CI runs on a `*/15` cron and sends only inside the windows above (`main.py` gates the send, the cron just keeps the runner warm). Plus manual `workflow_dispatch`; `concurrency: group: bot` prevents overlap, `timeout-minutes: 10` bounds the job. Deps installed via `astral-sh/setup-uv@v10` + `uv sync --frozen`, then `uv run python main.py`. Changes only take effect after pushing to `main` and triggering the workflow.
- Times are formatted with stdlib `zoneinfo` `America/Caracas` (UTC-4, no DST).

## Conventions

- Style follows black-ish formatting (double quotes, two blank lines between top-level defs) even though no formatter config is committed.
- Message text is Spanish; keep that when editing user-facing strings.
- Dependency changes go through `uv add`/`uv remove` so `uv.lock` stays in sync; keep the lockfile committed.