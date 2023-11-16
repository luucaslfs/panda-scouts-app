from telegram import Update
from telegram.ext import CallbackContext
from api_utils import get_match_data  # Supondo que você tenha uma função para obter dados da API

async def handle_text_message(update: Update, context: CallbackContext) -> None:
    """Manipulador para mensagens de texto."""
    user_message = update.message.text.lower()

    if 'oi' in user_message:
        await update.message.reply_text("Olá! Como posso ajudar?")

# Adicione outros manipuladores de mensagem, se necessário

async def handle_match_data_request(update: Update, context: CallbackContext) -> None:
    """Manipulador para solicitações de dados de partida."""
    # Obtenha o ID da partida a partir da mensagem do usuário
    try:
        match_id = int(context.matches[0].group(1))
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

# Função para formatar os dados da partida (exemplo)
def format_match_data(match_data):
    formatted_text = f"Dados da Partida:\n\n" \
                     f"ID: {match_data['match_id']}\n" \
                     f"Data: {match_data['date']}\n" \
                     f"Local: {match_data['venue']}\n" \
                     # Adicione mais campos conforme necessário

    return formatted_text
