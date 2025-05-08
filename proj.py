import numpy as np
import requests

# Configurações da API
API_URL = "http://0.0.0.0:8000/dow/daily-returns"

DATE_RANGE = {
    "start_date": "2025-01-08",
    "end_date": "2025-05-08"
}

# Função para obter dados da API
def get_daily_returns():
    try:
        response = requests.post(API_URL, json=DATE_RANGE)
        response.raise_for_status()  # Levanta exceção para códigos de status 4xx/5xx
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

# Função para gerar pesos aleatórios que somam 1
def generate_random_weights(n):
    weights = np.random.random(n)
    weights /= weights.sum()  # Normaliza para soma = 1
    return weights

# Obter dados da API
data = get_daily_returns()

# Obter todos os tickers disponíveis
tickers = list(data["returns"].keys())


# Converter retornos diários para matriz NumPy
retornos_dia = np.array([data["returns"][ticker] for ticker in tickers]).T


pesos_carteira = generate_random_weights(len(tickers))

# Retorno esperado anualizado
mi = retornos_dia.mean(axis=0) * 252

mi_portfolio = mi @ pesos_carteira

# Desvio padrão anualizado
cov_matrix = np.cov(retornos_dia.T)

sigma_portfolio = np.sqrt(pesos_carteira.T @ cov_matrix @ pesos_carteira) * np.sqrt(252)

# Índice de Sharpe (sem taxa livre de risco)
sharpe = mi_portfolio / sigma_portfolio

# Resultados
print(f"Retorno esperado: {mi_portfolio:.4f}")
print(f"Desvio padrão: {sigma_portfolio:.4f}")
print(f"Sharpe Ratio: {sharpe:.4f}")

