import httpx

async def get_match_data(match_id):
    """Função para obter dados da API usando o ID da partida."""
    # Substitua a URL abaixo pela URL real do seu endpoint da API
    api_url = f"http://127.0.0.1:8000/get-detailed-match-data/{match_id}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()  # Lança uma exceção se a resposta indicar um erro HTTP

        match_data = response.json()
        return match_data
    except Exception as e:
        # Trate os erros adequadamente, por exemplo, logando o erro
        print(f"Erro ao obter dados da API: {e}")
        raise  # Re-levanta a exceção para que o chamador saiba que houve um erro
