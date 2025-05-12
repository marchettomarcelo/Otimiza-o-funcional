import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sequencial = np.array([3530,3582, 3592, 3586, 3584 ])
paralelo = np.array([35.84, 34.58, 33.74, 33.80, 33.99 ])

# Definindo os dados
labels = ['Sequencial', 'Paralelo']
values = [sequencial.mean(), paralelo.mean()]
# Definindo o tamanho da figura
fig, ax = plt.subplots(figsize=(10, 6))
# Criando o gráfico de barras
ax.bar(labels, values, color=['blue', 'orange'])
# Definindo o título e os rótulos dos eixos
ax.set_title('Comparação entre execução sequencial e paralela', fontsize=16)

ax.set_xlabel('Tipo de Execução', fontsize=14)
ax.set_ylabel('Tempo médio de Execução em 5 rodagens (s)', fontsize=14)
# Definindo o formato do eixo y
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}'))
# Definindo o limite do eixo y
ax.set_ylim(0, 4000)
# Adicionando os rótulos das barras
for i, v in enumerate(values):
    ax.text(i, v + 50, f'{v:.2f}', ha='center', va='bottom', fontsize=12)
# Adicionando uma grade
ax.grid(axis='y', linestyle='--', alpha=0.7)
# Adicionando um título geral
# Exibindo o gráfico
plt.tight_layout()
plt.show()
