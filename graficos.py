# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker

# sequencial = np.array([3530,3582, 3592, 3586, 3584 ])
# paralelo = np.array([35.84, 34.58, 33.74, 33.80, 33.99 ])

# # Definindo os dados
# labels = ['Sequencial', 'Paralelo']
# values = [sequencial.mean(), paralelo.mean()]
# # Definindo o tamanho da figura
# fig, ax = plt.subplots(figsize=(10, 6))
# # Criando o gráfico de barras
# ax.bar(labels, values, color=['blue', 'orange'])
# # Definindo o título e os rótulos dos eixos
# ax.set_title('Comparação entre execução sequencial e paralela', fontsize=16)

# ax.set_xlabel('Tipo de Execução', fontsize=14)
# ax.set_ylabel('Tempo médio de Execução em 5 rodagens (s)', fontsize=14)
# # Definindo o formato do eixo y
# ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))
# # Definindo o limite do eixo y
# ax.set_ylim(0, 4000)
# # Adicionando os rótulos das barras
# for i, v in enumerate(values):
#     ax.text(i, v + 50, f'{v:.2f}', ha='center', va='bottom', fontsize=12)
# # Adicionando uma grade
# ax.grid(axis='y', linestyle='--', alpha=0.7)
# # Adicionando um título geral
# # Exibindo o gráfico
# plt.tight_layout()
# plt.show()


# import matplotlib.pyplot as plt

# # Dados da carteira
# tickers = [
#     "AAPL", "AMGN", "AXP", "BA", "CAT", "CSCO", "CVX", "DIS", "GS", "HON",
#     "IBM", "INTC", "JNJ", "KO", "MCD", "MMM", "MRK", "NKE", "PG", "TRV",
#     "UNH", "V", "VZ", "WBA", "WMT"
# ]

# weights_percent = [
#     0.8772, 10.4828, 0.0412, 3.5793, 0.0010, 4.6525, 10.7271, 0.6869, 1.2697, 0.3210,
#     5.4697, 4.2142, 9.4746, 5.1583, 3.7691, 8.3090, 0.0042, 0.4288, 3.2169, 2.3535,
#     4.1257, 4.3643, 11.4009, 4.0209, 1.0509
# ]

# # Ordenar por peso (opcional, mas facilita leitura)
# tickers, weights_percent = zip(*sorted(zip(tickers, weights_percent), key=lambda x: x[1], reverse=True))

# # Plot
# plt.figure(figsize=(10, 8))
# plt.barh(tickers, weights_percent, color='skyblue')
# plt.xlabel('Peso na carteira (%)')
# plt.title('Composição da Carteira - 2025 Q1')
# plt.gca().invert_yaxis()  # Tickers mais pesados no topo
# plt.grid(True, axis='x', linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.show()
