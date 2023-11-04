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

    def update_week_matches(self, league_id: int, season: int, week_matches: list):
        """
        Atualiza os jogos da semana na coleção MongoDB para uma liga específica.

        Args:
        - league_id (int): ID da liga.
        - season (int): Temporada.
        - week_matches (list): Lista de informações completas dos jogos da semana.

        Esta função atualiza os jogos da semana na coleção MongoDB para a liga e temporada especificadas.
        """
        query = {"league_info.id": league_id, "league_info.season": season}
        new_data = {"$set": {"week_matches": week_matches}}

        self.collection.update_one(query, new_data)

    def get_all_week_matches(self, season: int):
        """
        Obtém os jogos da semana para todas as ligas do banco de dados MongoDB em uma temporada específica.

        Args:
        - season (int): Temporada.

        Returns:
        - list: Uma lista de informações completas dos jogos da semana para todas as ligas.
        """
        query = {
            "league_info.season": season,
            "week_matches": {"$exists": True, "$not": {"$size": 0}}
        }

        projection = {"_id": 0, "week_matches": 1}
        matches = self.collection.find(query, projection)

        return list(matches)

    def get_week_matches(self, league_id: int, season: int):
        """
        Obtém os jogos da semana para uma liga específica do banco de dados MongoDB.

        Args:
        - league_id (int): ID da liga.
        - season (int): Temporada.

        Returns:
        - list: Uma lista de informações completas dos jogos da semana.
        """
        query = {
            "league_info.id": league_id,
            "league_info.season": season,
            "week_matches": {"$exists": True, "$not": {"$size": 0}}
        }

        projection = {"_id": 0, "week_matches": 1}
        matches = self.collection.find(query, projection)

        return list(matches)

    def update_team_statistics(self, league_id: int, season: int, team_id: int, team_stats: dict):
        query = {"league_info.id": league_id, "league_info.season": season}
        update_query = {
            "$set": {
                f"team_stats.{team_id}": team_stats
            }
        }
        self.collection.update_one(query, update_query)

    def get_team_stats(self, team_id: int):
        """
        Obtém as estatísticas de um time com base no ID do time.

        Args:
        - team_id (int): ID do time.

        Returns:
        - dict: Estatísticas do time.
        """
        query = {
            f"team_stats.{team_id}": {"$exists": True}
        }
        projection = {"_id": 0, f"team_stats.{team_id}": 1}

        team_stats_data = self.collection.find_one(query, projection)

        if team_stats_data:
            return team_stats_data["team_stats"][str(team_id)]
        else:
            raise ValueError(f"No team stats found for team_id {team_id}.")

    def get_match_by_id(self, match_id: int):
        """
        Get a match by its ID from the MongoDB database.

        Args:
        - match_id (int): ID of the match to retrieve.

        Returns:
        - dict: Information about the match.
        """
        query = {"week_matches.fixture.id": match_id}
        projection = {"_id": 0, "week_matches.$": 1}

        match_data = self.collection.find_one(query, projection)
        if match_data and 'week_matches' in match_data:
            # First match with the given ID
            return match_data['week_matches'][0]
        else:
            raise ValueError(f"No match found for match_id {match_id}.")

    def get_detailed_match_data(self, match_id: int):
        """
        Get detailed match data by match ID.

        Args:
        - match_id (int): ID of the match to retrieve.

        Returns:
        - dict: Detailed match data in the specified format.
        """
        match_data = self.get_match_by_id(match_id)

        if not match_data:
            raise ValueError(f"No match found for match_id {match_id}.")

        fixture = match_data.get('fixture', {})
        teams = match_data.get('teams', {})

        home_team = teams.get('home', {})
        away_team = teams.get('away', {})
        home_id = home_team.get('id', 0)
        away_id = away_team.get('id', 0)
        print(away_id)

        # Obtain team statistics using the team IDs
        home_team_stats = self.get_team_stats(home_id)
        away_team_stats = self.get_team_stats(away_id)

        # Create the detailed match data object
        detailed_match_data = {
            "match_id": match_id,
            "referee": fixture.get('referee', ""),
            "venue": fixture.get('venue', {}).get('name', ""),
            "date": fixture.get('date', ""),
            "timezone": fixture.get('timezone', ""),
            "home": {
                "team_id": home_team.get('id', 0),
                "team_name": home_team.get('name', ""),
                "team_logo": home_team.get('logo', ""),
                "statistics": home_team_stats,
            },
            "away": {
                "team_id": away_team.get('id', 0),
                "team_name": away_team.get('name', ""),
                "team_logo": away_team.get('logo', ""),
                "statistics": away_team_stats,
            },
        }

        return detailed_match_data


# Usando a classe no seu código
# db_instance = MongoDB()
# db_instance.update_league_data(39, 2023, data)
