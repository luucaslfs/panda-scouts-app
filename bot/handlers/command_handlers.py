from telegram import Update
from telegram.ext import CallbackContext
from api_utils import get_match_data  # Supondo que você tenha uma função para obter dados da API

async def handle_get_match_data(update: Update, context: CallbackContext) -> None:
    """Manipulador para o comando /getmatchdata."""
    # Obtenha o ID da partida a partir do comando
    try:
        match_id = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, forneça um ID de partida válido.")
        return

    # Chame a função para obter dados da API
    try:
        match_data = await get_match_data(match_id)
    except Exception as e:
        # Trate os erros adequadamente, por exemplo, logando o erro
        print(f"Erro ao obter dados da partida: {e}")
        await update.message.reply_text("Erro ao obter dados da partida. Tente novamente mais tarde.")
        return

    # Formate os dados da partida como desejado
    formatted_data = format_match_data(match_data)  # Implemente a função 'format_match_data' conforme necessário

    # Envie a resposta para o usuário
    await update.message.reply_text(formatted_data)

# Adicione outros manipuladores de comando, se necessário

# Função para formatar os dados da partida (exemplo)
def format_match_data(match_data):
    formatted_text = f"Dados da Partida:\n\n" \
                     f"ID: {match_data['match_id']}\n" \
                     f"Data: {match_data['date']}\n" \
                     f"Local: {match_data['venue']}\n" \
                     # Adicione mais campos conforme necessário

    return formatted_text
