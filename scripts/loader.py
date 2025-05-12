import requests

def get_daily_returns(date_range):

    API_URL = "https://yahoo-dow-data-py-production.up.railway.app/dow/daily-returns"
    try:
        response = requests.post(API_URL, json=date_range, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None


