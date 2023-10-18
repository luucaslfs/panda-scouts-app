import json
import http.client
import db
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
