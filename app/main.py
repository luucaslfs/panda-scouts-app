from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
import json
import services

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
    scheduler.add_job(bulk_update_standings_data, 'cron', hour=6)
    scheduler.add_job(update_today_matches_for_all_leagues_endpoint,
                      'cron', hour=6, minute=10)
    scheduler.start()


@app.post("/bulk-update-standings-data/")
async def bulk_update_standings_data():
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
            await services.update_league_data(league["league_id"], league["season"])

        return {"message": "Data updated successfully for all leagues"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/manual-update-standings-data/")
async def update_standings_data(league_id: int, season: int):
    """
    Atualiza manualmente os dados de uma liga específica.

    Este endpoint permite a atualização manual dos dados de uma liga específica
    com base no ID da liga e na temporada fornecidos como parâmetros.

    Retorna uma mensagem de sucesso após a atualização.
    """
    try:
        await services.update_league_data(league_id, season)
        return {"message": "Data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/today-quartile-matches/{league_id}/{season}")
async def get_today_quartile_matches(league_id: int, season: int):
    try:
        # Obter dados de classificação da liga usando a função do services.py
        standings_data = services.fetch_standings_data(league_id, season)

        # Obter os jogos do dia da coleção MongoDB usando a função do services.py
        today_matches = services.get_today_matches_from_db(league_id)

        # Filtrar jogos de quartil com base nas classificações das equipes
        quartile_matches = services.filter_quartile_matches(
            today_matches, standings_data)

        return {"matches": quartile_matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update-today-matches-for-all-leagues")
async def update_today_matches_for_all_leagues_endpoint():
    try:
        # Chame a função para atualizar os jogos do dia para todas as ligas
        services.update_today_matches_for_all_leagues()

        return {"message": "Atualização dos jogos do dia para todas as ligas concluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
