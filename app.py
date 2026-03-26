import json
import os
import base64
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# === CONFIGURATION ===
ADMINS = [8037300335]                      # Your Telegram user ID
GITHUB_TOKEN = "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"   # Hardcoded (not safe for public)
GITHUB_REPO = "z4xgaming/FF-blacklist"    # Correct repo name
GITHUB_FILE_PATH = "blacklist.json"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}"

# === Blacklist Management ===
def load_blacklist():
    if os.path.exists("blacklist.json"):
        with open("blacklist.json", "r") as f:
            return json.load(f)
    return []

def save_blacklist(blacklist):
    with open("blacklist.json", "w") as f:
        json.dump(blacklist, f, indent=2)
    push_to_github(blacklist)

def push_to_github(blacklist):
    if not GITHUB_TOKEN:
        print("No GitHub token, skipping push")
        return
    content = json.dumps(blacklist, indent=2)
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    resp = requests.get(GITHUB_API_URL, headers=headers)
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    data = {
        "message": "Update blacklist via bot",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main"
    }
    if sha:
        data["sha"] = sha
    requests.put(GITHUB_API_URL, headers=headers, json=data)
    print("Pushed to GitHub")

# === Telegram Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n"
        "/check <ID> - Check if ID is blacklisted\n"
        "/add <ID> - Add ID to blacklist (admin only)\n"
        "/remove <ID> - Remove ID from blacklist (admin only)"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /check <FreeFireID>")
        return
    ff_id = context.args[0]
    blacklist = load_blacklist()
    if ff_id in blacklist:
        await update.message.reply_text(f"❌ ID {ff_id} is **BLACKLISTED**.")
    else:
        await update.message.reply_text(f"✅ ID {ff_id} is **NOT** blacklisted.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("⛔ You are not authorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /add <FreeFireID>")
        return
    ff_id = context.args[0]
    blacklist = load_blacklist()
    if ff_id in blacklist:
        await update.message.reply_text(f"ℹ️ ID {ff_id} is already blacklisted.")
    else:
        blacklist.append(ff_id)
        save_blacklist(blacklist)
        await update.message.reply_text(f"✅ ID {ff_id} added to blacklist.")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        await update.message.reply_text("⛔ You are not authorized.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /remove <FreeFireID>")
        return
    ff_id = context.args[0]
    blacklist = load_blacklist()
    if ff_id in blacklist:
        blacklist.remove(ff_id)
        save_blacklist(blacklist)
        await update.message.reply_text(f"✅ ID {ff_id} removed from blacklist.")
    else:
        await update.message.reply_text(f"ℹ️ ID {ff_id} was not in blacklist.")

def main():
    # Hardcoded token – only for local testing
    token = "8480955083:AAFVIXXvXmbt7irxXTUte3ppItRDwn_0CXA"
    # For production, use environment variable:
    # token = os.getenv("BOT_TOKEN")
    # if not token:
    #     print("Error: BOT_TOKEN not set.")
    #     return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("remove", remove))

    app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("check", "Check if a FreeFire ID is blacklisted"),
        BotCommand("add", "Add an ID to blacklist (admin only)"),
        BotCommand("remove", "Remove an ID from blacklist (admin only)"),
    ])

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
