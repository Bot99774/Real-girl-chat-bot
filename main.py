import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

user_data_file = "users.json"
if not os.path.exists(user_data_file):
    with open(user_data_file, "w") as f:
        json.dump({}, f)

def load_users():
    with open(user_data_file, "r") as f:
        return json.load(f)

def save_users(users):
    with open(user_data_file, "w") as f:
        json.dump(users, f)

def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    users = load_users()
    if user_id not in users:
        users[user_id] = {
            "premium": False,
            "free_chats": 0,
            "referrals": [],
            "balance": 0
        }
        save_users(users)

    kb = [
        [InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium")],
        [InlineKeyboardButton("🎁 My Balance", callback_data="my_balance")]
    ]
    reply_markup = InlineKeyboardMarkup(kb)
    update.message.reply_text("👋 Welcome to Real Girl Chat!
Chat 1-on-1 anonymously.

🎯 10 free chats/day
💎 ₹10 or 1 USDT = Premium
👥 5 referrals = 1 premium match", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    users = load_users()

    if query.data == "buy_premium":
        text = ("💎 *Buy Premium Access*
"
                "• ₹10 UPI: `564632879@axl`
"
                "• 1 USDT (TRC20): `TBhgRdx6Ek9nv9auaXKeKR4TKx5yJF7mDG`

"
                "🎯 ₹1 = 1 Premium Match
"
                "🔄 After payment, contact admin: @Notan99")
        query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "my_balance":
        user = users.get(user_id, {})
        free_chats = user.get("free_chats", 0)
        balance = user.get("balance", 0)
        referrals = len(user.get("referrals", []))
        premium = user.get("premium", False)
        badge = "✅" if premium else "❌"
        text = f"📊 *Your Balance*
• Premium: {badge}
• Free Chats Today: {free_chats}/10
• Premium Tokens: {balance}
• Referrals: {referrals}/5"
        query.edit_message_text(text, parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()