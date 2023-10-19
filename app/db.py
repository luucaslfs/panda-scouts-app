from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class MongoDB:
    def __init__(self):
        self.client = MongoClient(getenv('MONGODB_URI'))
        self.db = self.client[getenv('DB_NAME')]

    def update_league_data(self, league_id: int, season: int, data: dict):
        self.collection = self.db["standings"]
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
        self.collection = self.db["standings"]
        result = self.collection.find_one(query)

        if result:
            return result
        else:
            raise ValueError(
                f"No standings data found for league_id {league_id} and season {season}.")

    # Adicione aqui outras funções relacionadas a operações no banco de dados, se necessário.
    # Por exemplo, funções para consultar dados, deletar documentos, etc.

# Usando a classe no seu código
# db_instance = MongoDB()
# db_instance.update_league_data(39, 2023, data)
