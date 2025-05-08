import numpy as np

pesos_carteira = np.array([0.5, 0.5]).T

retornos_dia = np.array([[0.01, 0.02], 
                        [0.03, 0.01 ],
                        [-0.01, -0.02]])


mi = retornos_dia.mean(axis=0) * 252

mi_portfolio =  mi @ pesos_carteira


sigma_portfolio = np.sqrt(pesos_carteira.T @ np.cov(retornos_dia.T) @ pesos_carteira) * np.sqrt(252)

sharpe = mi_portfolio / sigma_portfolio

print(f"Retorno esperado: {mi_portfolio}")
print(f"Desvio padrão: {sigma_portfolio}")
print(f"Sharpe Ratio: {sharpe}")