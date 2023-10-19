## Prompt-1

```
Estou criando uma aplicação em FastAPI e voce me ajudará

O objetivo é construir uma api que forneça estatisticas de jogos para sportsbetting.
A principio, estamos armazenando e atualizando as tabelas de diversas ligas.
O objetivo é, depois, extrair informações dos confrontos do dia/semana vigente para gerar análises e destacar estatísticas a partir de filtros.

esse é o main.py:

from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import json
from services import update_league_data

app = FastAPI()


@app.get("/")
async def root():
    """
    Rota principal da API.

    Retorna uma mensagem de saudação.
    """
    return {"message": "Hello World"}


@app.on_event("startup")
def start_recurring_update():
    """
    Inicia uma tarefa de atualização recorrente das ligas.

    Esta função é executada na inicialização do aplicativo e agenda uma tarefa
    para atualizar os dados das ligas diariamente às 6:30 da manhã.
    """
    tz = pytz.timezone('America/Sao_Paulo')
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_job(bulk_update_data, 'cron', hour=6, minute=30)
    scheduler.start()


@app.post("/bulk-update-standings-data/")
async def bulk_update_data():
    """
    Atualiza os dados das ligas com base em um arquivo JSON.

    Este endpoint lê um arquivo JSON contendo informações das ligas e realiza a
    atualização dos dados de todas as ligas especificadas no arquivo.

    Retorna uma mensagem de sucesso após a atualização.
    """
    try:
        with open("leagues.json", "r") as file:
            leagues = json.load(file)

        for league in leagues:
            await update_league_data(league["league_id"], league["season"])

        return {"message": "Data updated successfully for all leagues"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/manual-update-standings-data/")
async def update_data(league_id: int, season: int):
    """
    Atualiza manualmente os dados de uma liga específica.

    Este endpoint permite a atualização manual dos dados de uma liga específica
    com base no ID da liga e na temporada fornecidos como parâmetros.

    Retorna uma mensagem de sucesso após a atualização.
    """
    try:
        await update_league_data(league_id, season)
        return {"message": "Data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

e esse o db.py:

from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class MongoDB:
    def __init__(self):
        self.client = MongoClient(getenv('MONGODB_URI'))
        self.db = self.client[getenv('DB_NAME')]
        self.collection = self.db[getenv('COLLECTION_NAME')]

    def update_league_data(self, league_id: int, season: int, data: dict):
        query = {"league_info.id": league_id, "league_info.season": season}
        new_data = {"$set": data}
        self.collection.update_one(query, new_data, upsert=True)

    # Adicione aqui outras funções relacionadas a operações no banco de dados, se necessário.
    # Por exemplo, funções para consultar dados, deletar documentos, etc.

# Usando a classe no seu código
# db_instance = MongoDB()
# db_instance.update_league_data(39, 2023, data)


Agora que temos as tabelas atualizadas dos campeonatos em nosso banco, mos focar no objetivo de criar um endpoint para extrair os jogos do dia de cada campeonato e retornar apenas os ids dos confrontos entre times do primeiro contra times do ultimo quartil de acordo com a tabela do campeonato
```

### Prompt-2

```
Eu estou extraindo dados de uma API voltada a futebol. Voce pode ver no meu services.py abaixo como isso está sendo feito para as tabelas dos campeonatos:

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



Para os jogos do dia, essa api tem um endpoint /fixtures/ que retorna os jogos e tem diversos filtros:

QUERY PARAMETERS
id
integer
Value: "id"
The id of the fixture

ids
stringsMaximum of 20 fixtures ids
Value: "id-id-id"
One or more fixture ids

live
string
Enum: "all" "id-id"
All or several leagues ids

date
stringYYYY-MM-DD
A valid date

league
integer
The id of the league

season
integer = 4 characters YYYY
The season of the league

team
integer
The id of the team

last
integer <= 2 characters
For the X last fixtures

next
integer <= 2 characters
For the X next fixtures

from
stringYYYY-MM-DD
A valid date

to
stringYYYY-MM-DD
A valid date

round
string
The round of the fixture

status
string
Enum: "NS" "NS-PST-FT"
One or more fixture status short

venue
integer
The venue id of the fixture

timezone
string
A valid timezone from the endpoint Timezone
```
