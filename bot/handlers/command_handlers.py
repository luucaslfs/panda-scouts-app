from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime
from api_utils import get_match_data, get_quartile_matches, get_filtered_matches  # Supondo que você tenha uma função para obter dados da API

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
        print(f"Erro ao obter dados da partida: {e}")
        await update.message.reply_text("Erro ao obter dados da partida. Tente novamente mais tarde.")
        return

    formatted_data = format_match_data(match_data)  # Implemente a função 'format_match_data' conforme necessário
    await update.message.reply_text(formatted_data)

async def handle_quartil(update: Update, context: CallbackContext) -> None:
    """Manipulador para o comando /quartil."""
    try:
        quartil = await get_quartile_matches()
    except Exception as e:
        print(f"Erro ao obter dados das partidas: {e}")
        await update.message.reply_text("Erro ao obter dados da partida. Tente novamente mais tarde.")
        return
    
    formatted_data = await format_quartile_matches(quartil) 
    await update.message.reply_text(formatted_data)

async def handle_filtered_matches(update: Update, context: CallbackContext) -> None:
    """Manipulador para o comando /filtered-matches {min_med_cartoes} {max_med_cartoes}."""
    try:
        # Obtenha os parâmetros fornecidos pelo usuário
        cartoes_min_med, cartoes_max_med = map(float, context.args)
        filtered_matches_data = await get_filtered_matches(cartoes_min_med, cartoes_max_med)
    except ValueError:
        print(f"Erro ao obter dados da partida: Valores de input inválidos.")
        await update.message.reply_text("Por favor, forneça valores numéricos válidos.")
        return
    except Exception as e:
        print(f"Erro ao obter dados da partida: {e}")
        await update.message.reply_text("Erro ao obter dados da partida. Tente novamente mais tarde.")
        return
    
    formatted_data = await format_filtered_matches(filtered_matches_data)  
    await update.message.reply_text(formatted_data)

async def format_quartile_matches(quartile_matches_data):
    """Função para formatar os dados das partidas de quartil."""
    if not quartile_matches_data or 'matches' not in quartile_matches_data:
        return "Nenhuma partida encontrada com os critérios fornecidos."

    formatted_matches = []
    for match in quartile_matches_data['matches']:
        formatted_match = format_match_data(match)
        formatted_matches.append(formatted_match)

    separator = "\n\n" + "=" * 30  # Separador entre cada partida
    formatted_data = separator.join(formatted_matches)

    return formatted_data
    
async def format_filtered_matches(filtered_matches_data):
    """Função para formatar os dados das partidas filtradas."""
    if not filtered_matches_data or 'confrontos_filtrados' not in filtered_matches_data:
        return "Nenhuma partida encontrada com os critérios fornecidos."

    formatted_matches = []
    for match in filtered_matches_data['confrontos_filtrados']:
        formatted_match = format_match_data(match)
        formatted_matches.append(formatted_match)

    separator = "\n\n" + "=" * 30  # Separador entre cada partida
    formatted_data = separator.join(formatted_matches)

    return formatted_data
    
def format_match_data(match_data):
    """Função para formatar os dados de uma partida."""
    match_id = match_data.get("match_id", "N/A")
    venue = match_data.get("venue", "N/A")
    date = match_data.get("date", "N/A")
    ref = match_data.get("referee", "N/A")

    home_team = match_data.get("home", {})
    away_team = match_data.get("away", {})

    home_team_name = home_team.get("team_name", "N/A")
    away_team_name = away_team.get("team_name", "N/A")

    home_goals_for = home_team["statistics"].get("total_goals_for", "N/A")
    away_goals_for = away_team["statistics"].get("total_goals_for", "N/A")

    home_win_percentage = home_team["statistics"].get("win_percentage_home", "N/A")
    away_win_percentage = away_team["statistics"].get("win_percentage_away", "N/A")

    home_team_rank = home_team.get("team_rank")
    away_team_rank = away_team.get("team_rank")

    formatted_text = (
        f"🏟 Dados da Partida 🏟\n"
        f"ID: {match_id}\n"
        f"Data: {format_date(date)}\n"
        f"Local: {venue}\n\n"
        f"⚽ Equipe da Casa: {home_team_name}\n"
        f"   Gols: {home_goals_for}\n"
        f"   Classificação: {home_team_rank}\n"
        f"   Percentual de Vitórias em Casa: {format_percentage(home_win_percentage)}\n\n"
        f"⚔️ Equipe Visitante: {away_team_name}\n"
        f"   Gols: {away_goals_for}\n"
        f"   Classificação: {away_team_rank}\n"
        f"   Percentual de Vitórias como Visitante: {format_percentage(away_win_percentage)}"
    )

    return formatted_text

def format_date(raw_date):
    """Formatar a data para exibição."""
    try:
        formatted_date = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S+00:00").strftime("%d/%m/%Y %H:%M")
    except ValueError:
        formatted_date = "N/A"
    return formatted_date

def format_percentage(raw_percentage):
    """Arredondar e formatar a porcentagem."""
    try:
        rounded_percentage = round(float(raw_percentage), 2)
        formatted_percentage = f"{rounded_percentage}%"
    except (ValueError, TypeError):
        formatted_percentage = "N/A"
    return formatted_percentage
