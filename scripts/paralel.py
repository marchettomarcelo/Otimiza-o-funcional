import numpy as np
from itertools import combinations
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
from tqdm import tqdm

# Função para calcular métricas da carteira para uma combinação
def calculate_portfolio_metrics(args):

    retornos_dia, combo_indices, tickers, n_vetores_pesos = args
    
    selected_indices = list(combo_indices)
    selected_tickers = [tickers[i] for i in selected_indices]
    retornos_combo = retornos_dia[:, selected_indices]

    # Pré-calcular métricas fixas
    mi = retornos_combo.mean(axis=0) * 252  # Retorno esperado anualizado
    cov_matrix = np.cov(retornos_combo.T) * 252  # Covariância anualizada


    pesos = np.random.random((n_vetores_pesos, 25))
    pesos /= pesos.sum(axis=1, keepdims=True)  # Normalizar para soma = 1

    # Calcular retornos do portfólio (vetorizado)
    mi_portfolio = pesos @ mi

    # Calcular volatilidade do portfólio (vetorizado)
    sigma_portfolio = np.sqrt(np.einsum('ij,jk,ik->i', pesos, cov_matrix, pesos))

    # Calcular Sharpe (sem taxa livre de risco)
    sharpe = mi_portfolio / sigma_portfolio

    # Encontrar o melhor Sharpe
    best_idx = np.argmax(sharpe)
    best_sharpe = sharpe[best_idx]
    melhor_pesos = pesos[best_idx]

    return best_sharpe, melhor_pesos, selected_tickers

# Função principal
def paralel_optimization(data, n_vetores_pesos = 1000):
    # Obter todos os tickers disponíveis
    tickers = list(data["returns"].keys())

    # Converter retornos diários para matriz NumPy
    retornos_dia = np.array([data["returns"][ticker] for ticker in tickers]).T

    # Gerar todas as combinações de 25 tickers
    combinations_list = list(combinations(range(len(tickers)), 25))
    print(f"Total de combinações: {len(combinations_list)}")

    # Configurar número de trabalhadores
    num_workers = min(multiprocessing.cpu_count(), 16)  # Limite para evitar sobrecarga

    # Inicializar variáveis para a melhor combinação
    best_sharpe = -np.inf
    best_tickers = None
    best_pesos = None

    # Processar combinações em paralelo
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submeter todas as combinações
        future_to_combo = {
            executor.submit(calculate_portfolio_metrics, (retornos_dia, combo, tickers, n_vetores_pesos)): combo
            for combo in combinations_list
        }

        # Monitorar progresso com tqdm
        for future in tqdm(as_completed(future_to_combo), total=len(combinations_list), desc="Processando combinações"):
            sharpe, pesos, selected_tickers = future.result()
            
            # Atualizar melhor combinação
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_tickers = selected_tickers
                best_pesos = pesos

    return best_sharpe, best_tickers, best_pesos
