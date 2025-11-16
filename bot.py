# type:ignore
# pip install python-telegram-bot --upgrade
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, CallbackQueryHandler
import os

TOKEN_FILE_PATH = os.path.join(os.path.dirname(__file__), 'token')
CURRENT_DIR = os.path.join(os.path.dirname(__file__))

class Bot:
    name = ""

    def __init__ (self, name):
        self.name = name

    async def start(self,  update: Update, context: CallbackContext) -> None:
        buttonMenu = BotButtonMenu
        await buttonMenu.start(update, context)

    def read_token (self, fname=TOKEN_FILE_PATH):
        with open(fname, 'r') as f:
            return f.read().strip()

    async def commands(self, update: Update, context: CallbackContext) -> None:
        botmenu = BotButtonMenu()
        await botmenu.start(update, context)


    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        data = query.data
        print(data)

    
    def exec (self):
        token = self.read_token(TOKEN_FILE_PATH)
        print(f"[Load] Token len: {len(token)}")
        app = ApplicationBuilder().token(token).build()
    
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.commands))
        app.add_handler(CommandHandler("ask", self.handle_callback))


        print("Bot is running...")
        app.run_polling()

if __name__ == '__main__':
    bot = Bot("prompter")
    bot.exec()



