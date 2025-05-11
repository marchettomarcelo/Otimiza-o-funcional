import requests
# Configurações da API
API_URL = "http://0.0.0.0:8000/dow/daily-returns"
DATE_RANGE = {
    "start_date": "2024-08-01",
    "end_date": "2024-12-31"
}

# Função para obter dados da API
def get_daily_returns():
    try:
        response = requests.post(API_URL, json=DATE_RANGE, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None


