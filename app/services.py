import json
import http.client
import db
import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_FOOTBALL_KEY = getenv('API_FOOTBALL_KEY')
db_instance = db.MongoDB()


def get_football_data(league_id: int, season: int) -> str:
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': API_FOOTBALL_KEY,
        'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
    }

    print(headers)

    conn.request(
        "GET", f"/v3/standings?season={season}&league={league_id}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


def organize_data(data_json: dict) -> dict:
    organized_data = {
        "league_info": {
            "id": data_json["response"][0]["league"]["id"],
            "name": data_json["response"][0]["league"]["name"],
            "country": data_json["response"][0]["league"]["country"],
            "logo": data_json["response"][0]["league"]["logo"],
            "flag": data_json["response"][0]["league"]["flag"],
            "season": data_json["response"][0]["league"]["season"],
        },
        "standings": []
    }

    for entry in data_json["response"][0]["league"]["standings"][0]:
        team_data = {
            "rank": entry["rank"],
            "team_id": entry["team"]["id"],
            "team_name": entry["team"]["name"],
            "points": entry["points"],
            "goalsDiff": entry["goalsDiff"],
            "form": entry["form"],
        }
        organized_data["standings"].append(team_data)

    return organized_data


async def update_league_data(league_id: int, season: int):
    raw_data = get_football_data(league_id, season)
    data_json = json.loads(raw_data)
    organized_data = organize_data(data_json)
    db_instance.update_league_data(league_id, season, organized_data)


def fetch_standings_data(league_id: int, season: int) -> dict:
    """
    Busca, em nosso banco, os dados de classificação de uma liga específica com base no ID da liga e na temporada.

    Args:
    - league_id (int): ID da liga.
    - season (int): Temporada.

    Returns:
    - dict: Dados de classificação da liga.
    """
    return db_instance.get_standings_data(league_id, season)


def filter_quartile_matches(today_matches: list, standings_data: dict) -> list:
    """
    Filtra os jogos do dia com base nas classificações das equipes.

    Args:
    - today_matches (list): Lista de informações completas dos jogos do dia.
    - standings_data (dict): Dados de classificação da liga.

    Returns:
    - list: Uma lista de informações completas dos jogos que atendem aos critérios.
    """
    quartile_threshold = len(standings_data["standings"]) // 4

    quartile_matches = []

    for match in today_matches:
        home_team_id = match["teams"]["home"]["id"]
        away_team_id = match["teams"]["away"]["id"]

        # Encontre as classificações das equipes
        home_team_rank = next(
            (team["rank"] for team in standings_data["standings"] if team["team_id"] == home_team_id), None)
        away_team_rank = next(
            (team["rank"] for team in standings_data["standings"] if team["team_id"] == away_team_id), None)

        # Verifique se ambas as equipes estão no primeiro ou no último quartil
        if home_team_rank is not None and away_team_rank is not None:
            if home_team_rank <= quartile_threshold and away_team_rank > 3 * quartile_threshold:
                quartile_matches.append(match)
            elif away_team_rank <= quartile_threshold and home_team_rank > 3 * quartile_threshold:
                quartile_matches.append(match)

    return quartile_matches


def update_today_matches_in_db(league_id: int, season: int):
    """
    Atualiza os jogos do dia no banco de dados MongoDB para uma liga específica.

    Args:
    - league_id (int): ID da liga.
    - season (int): Temporada.

    Esta função faz uma chamada à API externa para obter os jogos do dia e atualiza
    o campo "today_matches" na coleção do MongoDB para a liga especificada.
    """
    try:
        conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': API_FOOTBALL_KEY,
            'X-RapidAPI-Host': "api-football-v1.p.rapidapi.com"
        }

        # Obtém a data atual no formato YYYY-MM-DD
        today = datetime.date.today().isoformat()

        # Define o fuso horário para "America/Sao_Paulo"
        timezone = "America/Sao_Paulo"
        status = "NS"

        # Faz a consulta para obter os jogos do dia para a liga e temporada especificadas
        conn.request(
            "GET", f"/v3/fixtures?date={today}&league={league_id}&season={season}&timezone={timezone}&status={status}", headers=headers)

        res = conn.getresponse()
        data = res.read()

        fixtures_data = json.loads(data.decode("utf-8"))

        # Obtém os jogos do dia
        today_matches = fixtures_data.get("response", [])

        # Extrai apenas os campos "fixture" e "teams"
        extracted_matches = []
        for match in today_matches:
            extracted_match = {
                "fixture": match.get("fixture", {}),
                "teams": match.get("teams", {})
            }
            extracted_matches.append(extracted_match)

        # Atualiza o campo "today_matches" na coleção MongoDB para a liga especificada
        db_instance.update_today_matches(league_id, season, extracted_matches)

    except Exception as e:
        print(f"Erro ao atualizar jogos do dia: {str(e)}")


def update_today_matches_for_all_leagues():
    try:
        # Ler o arquivo leagues.json para obter a lista de ligas
        with open("leagues.json", "r") as file:
            leagues = json.load(file)

        # Para cada liga na lista, chame a função para atualizar os jogos do dia
        for league in leagues:
            league_id = league["league_id"]
            season = league["season"]
            update_today_matches_in_db(league_id, season)

        print("Atualização dos jogos do dia para todas as ligas concluída com sucesso")
    except Exception as e:
        print(f"Erro ao atualizar jogos do dia para todas as ligas: {str(e)}")


def get_today_matches_from_db(league_id: int, season: int):
    """
    Obtém os jogos do dia para uma liga específica do banco de dados MongoDB.

    Args:
    - league_id (int): ID da liga.
    - season (int): Temporada.

    Returns:
    - list: Uma lista de informações completas dos jogos do dia.
    """
    # Chama o método do banco de dados para obter os jogos do dia
    return db_instance.get_today_matches(league_id, season)
