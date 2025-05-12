import time
from scripts.paralel import paralel_optimization
from scripts.sequential import sequential_optimization
from scripts.loader import get_daily_returns


def main():

    DATE_RANGE = {
        "start_date": "2025-01-01",
        "end_date": "2025-03-31"
    }

    data = get_daily_returns(DATE_RANGE)

    mode = input("Escolha o modo de otimização sequential (s) ou paralel (p): ").strip().lower()

    start_time = time.time()

    if mode == "s":
        best_sharpe, best_tickers, best_pesos = sequential_optimization(data, n_vetores_pesos=1000)
    
    elif mode == "p":
        best_sharpe, best_tickers, best_pesos = paralel_optimization(data, n_vetores_pesos=1000)

     # Exibir resultados
    print("\nMelhor combinação encontrada:")
    print(f"Sharpe Ratio: {best_sharpe:.4f}")
    print("\nTickers selecionados:")
    print(", ".join(best_tickers))
    print("\nPesos da carteira:")

    for ticker, peso in zip(best_tickers, best_pesos):
        print(f"{ticker}: {peso*100:.4f}%")

    elapsed_time = time.time() - start_time
    print(f"\nTempo total de execução: {elapsed_time:.2f} segundos")


if __name__ == "__main__":
    main()
