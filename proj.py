import numpy as np
import requests
from datetime import date
from itertools import combinations

# Configurações da API
API_URL = "http://0.0.0.0:8000/dow/daily-returns"
DATE_RANGE = {
    "start_date": "2024-08-01",
    "end_date": "2024-12-31"
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

# Função para calcular métricas da carteira
def calculate_portfolio_metrics(retornos_dia ):

    best_sharpe = -np.inf
    melhor_pesos = None

    for _ in range(10):
        
        pesos_carteira = generate_random_weights(25)
        
        mi = retornos_dia.mean(axis=0) * 252

        mi_portfolio = mi @ pesos_carteira
        
        # Desvio padrão anualizado
        cov_matrix = np.cov(retornos_dia.T)

        sigma_portfolio = np.sqrt(pesos_carteira.T @ cov_matrix @ pesos_carteira) * np.sqrt(252)
        
        # Índice de Sharpe (sem taxa livre de risco)
        sharpe = mi_portfolio / sigma_portfolio
        
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            melhor_pesos = pesos_carteira
        
    return sharpe, melhor_pesos

# Obter dados da API
data = get_daily_returns()

# Obter todos os tickers disponíveis
tickers = list(data["returns"].keys())

# Converter retornos diários para matriz NumPy
retornos_dia = np.array([data["returns"][ticker] for ticker in tickers]).T

# Inicializar variáveis para armazenar a melhor combinação
best_sharpe = -np.inf
best_tickers = None
best_pesos = None

# Gerar todas as combinações de 25 tickers
n_tickers = len(tickers)
combinations_list = list(combinations(range(n_tickers), 25))
print(f"Total de combinações: {len(combinations_list)}")

# Iterar sobre todas as combinações
for idx, combo in enumerate(combinations_list):
    # Selecionar índices dos tickers na combinação
    selected_indices = list(combo)
    selected_tickers = [tickers[i] for i in selected_indices]
    
    # Selecionar retornos dos tickers escolhidos
    retornos_combo = retornos_dia[:, selected_indices]
        
    # Calcular métricas da carteira
    sharpe, melhor_peso = calculate_portfolio_metrics(retornos_combo)
    
    # Atualizar melhor combinação se Sharpe for maior
    if sharpe > best_sharpe:
        best_sharpe = sharpe
        best_tickers = selected_tickers
        best_pesos = melhor_peso

    # Progresso (opcional, para monitorar)
    if (idx + 1) % 10000 == 0:
        print(f"Processadas {idx + 1} combinações...")

# Resultados
print("\nMelhor combinação encontrada:")
print(f"Sharpe Ratio: {best_sharpe:.4f}")
print("\nTickers selecionados:")
print(", ".join(best_tickers))
print("\nPesos da carteira:")

for ticker, peso in zip(best_tickers, best_pesos):
    print(f"{ticker}: {peso*100:.4f}%")