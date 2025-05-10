import numpy as np
import requests
from datetime import date
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

import time

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
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

# Função para gerar pesos aleatórios que somam 1
def generate_random_weights(n):
    weights = np.random.random(n)
    weights /= weights.sum()
    return weights

# Função para calcular métricas da carteira para uma combinação
def calculate_portfolio_metrics(retornos_dia, combo_indices, tickers):
    # Selecionar retornos dos tickers da combinação
    selected_indices = list(combo_indices)
    selected_tickers = [tickers[i] for i in selected_indices]
    retornos_combo = retornos_dia[:, selected_indices]

    best_sharpe = -np.inf
    melhor_pesos = None

    # Testar 10 conjuntos de pesos aleatórios
    for _ in range(10):
        pesos_carteira = generate_random_weights(25)
        
        # Retorno esperado anualizado
        mi = retornos_combo.mean(axis=0) * 252
        mi_portfolio = mi @ pesos_carteira
        
        # Desvio padrão anualizado
        cov_matrix = np.cov(retornos_combo.T)
        sigma_portfolio = np.sqrt(pesos_carteira.T @ cov_matrix @ pesos_carteira) * np.sqrt(252)
        
        # Índice de Sharpe (sem taxa livre de risco)
        sharpe = mi_portfolio / sigma_portfolio
        
        if sharpe > best_sharpe:
            best_sharpe = sharpe
            melhor_pesos = pesos_carteira
    
    return best_sharpe, melhor_pesos, selected_tickers

# Função principal
def main():
    # Obter dados da API
    data = get_daily_returns()
    if data is None:
        print("Falha ao obter dados da API. Encerrando.")
        return

    # Obter todos os tickers disponíveis
    tickers = list(data["returns"].keys())

    # Converter retornos diários para matriz NumPy
    retornos_dia = np.array([data["returns"][ticker] for ticker in tickers]).T

    # Inicializar variáveis para armazenar a melhor combinação
    best_sharpe = -np.inf
    best_tickers = None
    best_pesos = None

    # Gerar todas as combinações de 25 tickers
    combinations_list = list(combinations(range(len(tickers)), 25))
    print(f"Total de combinações: {len(combinations_list)}")

    # Configurar o número de trabalhadores (ajuste conforme necessário)
    num_workers = multiprocessing.cpu_count()  # Usa o número de núcleos disponíveis

    # Processar combinações em paralelo
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        
        # Submeter todas as combinações para processamento
        future_to_combo = {
            executor.submit(calculate_portfolio_metrics, retornos_dia, combo, tickers): combo
            for combo in combinations_list
        }

        # Monitorar progresso
        completed = 0
        for future in as_completed(future_to_combo):
            sharpe, pesos, selected_tickers = future.result()
            
            # Atualizar melhor combinação se Sharpe for maior
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_tickers = selected_tickers
                best_pesos = pesos

            completed += 1
            if completed % 10000 == 0:
                print(f"Processadas {completed} combinações...")

    # Exibir resultados
    print("\nMelhor combinação encontrada:")
    print(f"Sharpe Ratio: {best_sharpe:.4f}")
    print("\nTickers selecionados:")
    print(", ".join(best_tickers))
    print("\nPesos da carteira:")
    for ticker, peso in zip(best_tickers, best_pesos):
        print(f"{ticker}: {peso*100:.4f}%")

if __name__ == "__main__":
    start_time = time.time()
    
    main()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTempo total de execução: {elapsed_time:.2f} segundos")