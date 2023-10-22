from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
import datetime

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

    def get_standings_data(self, league_id: int, season: int) -> dict:
        """
        Busca os dados de classificação de uma liga específica com base no ID da liga e na temporada.

        Args:
        - league_id (int): ID da liga.
        - season (int): Temporada.

        Returns:
        - dict: Dados de classificação da liga.
        """
        query = {"league_info.id": league_id, "league_info.season": season}

        result = self.collection.find_one(query)

        if result:
            return result
        else:
            raise ValueError(
                f"No standings data found for league_id {league_id} and season {season}.")

    def update_today_matches(self, league_id: int, season: int, today_matches: list):
        """
        Atualiza os jogos do dia na coleção MongoDB para uma liga específica.

        Args:
        - league_id (int): ID da liga.
        - season (int): Temporada.
        - today_matches (list): Lista de informações completas dos jogos do dia.

        Esta função atualiza os jogos do dia na coleção MongoDB para a liga e temporada especificadas.
        """
        query = {"league_info.id": league_id, "league_info.season": season}
        new_data = {"$set": {"today_matches": today_matches}}

        self.collection.update_one(query, new_data)

    def get_today_matches(self, league_id: int, season: int):
        """
        Obtém os jogos do dia para uma liga específica do banco de dados MongoDB.

        Args:
        - league_id (int): ID da liga.
        - season (int): Temporada.

        Returns:
        - list: Uma lista de informações completas dos jogos do dia.
        """
        query = {
            "league_info.id": league_id,
            "league_info.season": season,
            "today_matches": {"$exists": True, "$not": {"$size": 0}}
        }

        projection = {"_id": 0, "today_matches": 1}
        matches = self.collection.find(query, projection)

        return list(matches)

    def update_team_statistics(self, league_id: int, season: int, team_id: int, team_stats: dict):
        query = {"league_info.id": league_id, "league_info.season": season}
        update_query = {
            "$set": {
                # Use o ID do time como chave no campo "team_stats"
                f"team_stats.{team_id}": team_stats
            }
        }
        self.collection.update_one(query, update_query)


# Usando a classe no seu código
# db_instance = MongoDB()
# db_instance.update_league_data(39, 2023, data)
