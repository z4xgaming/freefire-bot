# Free Fire Blacklist Bot & Web Checker

A Telegram bot to manage blacklisted Free Fire IDs, with a public web page for checking.

## Features
- `/add <id>` – Add an ID to blacklist (admin only)
- `/remove <id>` – Remove an ID from blacklist (admin only)
- `/check <id>` – Check if an ID is blacklisted
- Web page: instantly check any ID without Telegram

## Setup
1. Create a Telegram bot via [BotFather](https://t.me/botfather) and get the token.
2. Get your user ID from [@userinfobot](https://t.me/userinfobot).
3. Generate a GitHub personal access token with `repo` scope.
4. Fork/clone this repository.
5. Add environment variables on Render:
   - `BOT_TOKEN` = your Telegram bot token
   - `GITHUB_TOKEN` = your GitHub token
6. Deploy on Render as a **Background Worker**.
7. Enable GitHub Pages to host the web checker (Settings → Pages → branch: main).

## Web Checker
Once GitHub Pages is enabled, access:
`https://z4xgaming.github.io/freefire-blacklist-bot/checker.html`

## Notes
- The bot automatically pushes every change to GitHub, so the web checker always shows the latest blacklist.
- Admin rights are based on Telegram user IDs defined in `ADMINS`.