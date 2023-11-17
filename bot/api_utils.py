import httpx

async def get_match_data(match_id):
    """Função para obter dados da API usando o ID da partida."""
    api_url = f"http://127.0.0.1:8000/get-detailed-match-data/{match_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()  # Lança uma exceção se a resposta indicar um erro HTTP

        match_data = response.json()
        return match_data
    except Exception as e:
        print(f"Erro ao obter dados da API: {e}")
        raise  # Re-levanta a exceção para que o chamador saiba que houve um erro


async def get_filtered_matches(cartoes_min_med, cartoes_med_somada):
    """Função para obter dados das partidas filtradas na API usando parametros de media de um dos times e media somada de cartões."""
    api_url = f"http://127.0.0.1:8000/confrontos-filtrados?season=2023&cartoes_min_por_time={cartoes_min_med}&cartoes_media_somada={cartoes_med_somada}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()  # Lança uma exceção se a resposta indicar um erro HTTP
            
        match_data = response.json()
        return match_data
    except Exception as e:
        print(f"Erro ao obter dados da API: {e}")
        raise  # Re-levanta a exceção para que o chamador saiba que houve um erro


async def get_quartile_matches():
    """Função para obter dados das partidas da semana de primeiros colocados vs ultimos colocados na API."""
    api_url = f"http://127.0.0.1:8000/weekly-quartile-matches/"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()  # Lança uma exceção se a resposta indicar um erro HTTP

        match_data = response.json()
        return match_data
    except Exception as e:
        print(f"Erro ao obter dados da API: {e}")
        raise  # Re-levanta a exceção para que o chamador saiba que houve um erro

