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
