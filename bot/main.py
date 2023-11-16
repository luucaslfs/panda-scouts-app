import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters
from handlers.command_handlers import handle_get_match_data  # Importe os manipuladores de comando necessários
from handlers.message_handlers import handle_text_message, handle_match_data_request  # Importe os manipuladores de mensagem necessários
from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")

# Configuração do logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
application = Application.builder().token(token).build()

# Adição dos manipuladores de comando
application.add_handler(CommandHandler("getmatchdata", handle_get_match_data, has_args=True))

# Adição dos manipuladores de mensagem
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
application.add_handler(MessageHandler(filters.Regex(r'/getmatchdata (\d+)'), handle_match_data_request))

# Adição do teclado personalizado
keyboard = [["/getmatchdata"],
            ["/help"]]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: CallbackContext) -> None:
    """Enviar mensagem inicial com o teclado personalizado."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Oi {user.mention_html()}! Como posso ajudar?",
        reply_markup=reply_markup,
    )

application.add_handler(CommandHandler("start", start))


# Execução da aplicação
application.run_polling(allowed_updates=Update.ALL_TYPES)
