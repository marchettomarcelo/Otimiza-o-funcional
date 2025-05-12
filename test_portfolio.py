import numpy as np
from scripts.loader import get_daily_returns

def test_portfolio():
    
    date_range = {
        "start_date": "2025-01-01",
        "end_date": "2025-03-31"
    }
    
    # Obter dados da API
    data = get_daily_returns(date_range)
    if not data:
        return
    
    # Tickers e pesos da carteira
    tickers = np.array([
        "AAPL", "AMGN", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS", "GS", "HON",
        "IBM", "INTC", "JNJ", "KO", "MCD", "MMM", "MRK", "NKE", "PG", "TRV",
        "UNH", "V", "VZ", "WBA", "WMT"
    ])
    
    pesos_carteira = np.array([
        0.008772, 0.104828, 0.000412, 0.035793, 0.000010, 0.046525, 0.107271, 0.006869, 0.012697, 0.003210,
        0.054697, 0.042142, 0.094746, 0.051583, 0.037691, 0.083090, 0.000042, 0.004288, 0.032169, 0.023535,
        0.041257, 0.043643, 0.114009, 0.040209, 0.010509
    ]).T
    
    # Verificar se todos os tickers estão disponíveis nos dados
    available_tickers = list(data["returns"].keys())
    missing_tickers = set(tickers) - set(available_tickers)
    
    if missing_tickers:
        print(f"Erro: Os seguintes tickers não estão disponíveis: {missing_tickers}")
        return
    
    # Converter retornos diários para matriz NumPy
    retornos_dia = np.array([data["returns"][ticker] for ticker in tickers]).T
    
    # Calcular métricas
    mi = retornos_dia.mean(axis=0) * 252  # Retorno esperado anualizado
    mi_portfolio = mi @ pesos_carteira  # Retorno esperado da carteira
    
    # Calcular covariância e volatilidade
    cov_matrix = np.cov(retornos_dia.T) * 252  # Matriz de covariância anualizada
    sigma_portfolio = np.sqrt(pesos_carteira.T @ cov_matrix @ pesos_carteira)  # Volatilidade da carteira
    
    # Calcular Sharpe Ratio (sem taxa livre de risco)
    sharpe = mi_portfolio / sigma_portfolio
    
    # Calcular retorno acumulado
    retorno_acumulado = np.prod(1 + retornos_dia @ pesos_carteira) - 1
    
    # Exibir resultados
    print("\nResultados da Carteira:")
    print("-" * 50)
    print(f"Período de análise: {date_range['start_date']} até {date_range['end_date']}")
    print(f"Retorno esperado anualizado: {mi_portfolio:.4%}")
    print(f"Volatilidade anualizada: {sigma_portfolio:.4%}")
    print(f"Sharpe Ratio: {sharpe:.4f}")
    print(f"Retorno acumulado no período: {retorno_acumulado:.4%}")
    
    print("\nComposição da Carteira:")
    print("-" * 50)
    for ticker, peso in zip(tickers, pesos_carteira):
        print(f"{ticker}: {peso:.4%}")
    
if __name__ == "__main__":
    test_portfolio() 