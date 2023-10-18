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
