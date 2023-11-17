import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters
from handlers.command_handlers import handle_get_match_data, handle_quartil, handle_filtered_matches
from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")

# Configuração do logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
application = Application.builder().token(token).build()

# Adição dos manipuladores de comando
application.add_handler(CommandHandler("getmatchdata", handle_get_match_data, has_args=True))
application.add_handler(CommandHandler("filtered_matches", handle_filtered_matches))
application.add_handler(CommandHandler("quartil", handle_quartil))

# Adição do teclado personalizado
keyboard = [["./getmatchdata {id da partida} - Obter dados da partida"],
            ["/quartil - Obter partidas de primeiros vs ultimos"],
            ["/filtered_matches - Obter partidas filtradas por medias de cartoes por jogo"],]
            

            

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: CallbackContext) -> None:
    """Enviar mensagem inicial com o teclado personalizado."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Oi {user.mention_html()}! Sou um bot de Scouts de apostas esportivas. Como posso ajudar?",
        reply_markup=reply_markup,
    )

application.add_handler(CommandHandler("start", start))


# Execução da aplicação
application.run_polling(allowed_updates=Update.ALL_TYPES)
