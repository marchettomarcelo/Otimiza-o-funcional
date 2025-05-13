# Otimização de Carteira de Investimentos

Este projeto implementa um otimizador de carteira de investimentos que utiliza dados históricos dos ativos do índice Dow Jones para encontrar a melhor combinação de ativos e seus respectivos pesos, maximizando o Índice de Sharpe.

## Funcionalidades

-   Otimização de carteira com 25 ativos selecionados entre os 30 do Dow Jones
-   Dois modos de otimização:
    -   Sequencial: Processamento em série, ideal para testes e análises menores
    -   Paralelo: Processamento distribuído, otimizado para análises mais extensas
-   Cálculo automático do Índice de Sharpe
-   Geração de gráficos comparativos de performance
-   Interface via linha de comando
-   Teste de carteiras específicas com métricas detalhadas

## Requisitos

-   Python 3.8+
-   UV (gerenciador de pacotes Python)
-   Conexão com internet para acesso à API de dados
-   Bibliotecas Python:
    -   numpy
    -   requests
    -   datetime

## Instalação

1. Primeiramente instale [UV](https://docs.astral.sh/uv/getting-started/installation/), no seu computador

2. Clone este repositório:

```bash
git clone https://github.com/marchettomarcelo/Portfolio-optimization.git
cd Portfolio-optimization
```

3. Execute o programa:

```bash
uv run main.py
```

## Como Usar

### Otimização de Carteira

1. Ao executar o programa principal, você será solicitado a escolher o modo de otimização:

    - `s` para otimização sequencial
    - `p` para otimização paralela

2. O programa irá:
    - Buscar dados históricos dos ativos
    - Realizar a otimização da carteira
    - Exibir os resultados com:
        - Melhor Índice de Sharpe encontrado
        - Tickers selecionados
        - Pesos da carteira otimizada
        - Tempo total de execução

### Teste de Carteira Específica

Para testar uma carteira específica com tickers e pesos predefinidos:

```bash
uv run test_portfolio.py
```

O script irá:

-   Buscar dados históricos do período especificado
-   Calcular métricas importantes:
    -   Retorno esperado anualizado
    -   Volatilidade anualizada
    -   Sharpe Ratio
    -   Retorno acumulado no período
-   Mostrar a composição detalhada da carteira
-   Exibir a contribuição de cada ativo para o retorno total

## Resultados

### Comparação de Performance

O gráfico abaixo compara o tempo de execução para analisar 1000 alocações diferentes para uma única combinação de 25 dos 30 ativos do índice Dow Jones. Os dados são referentes ao período de 01/08/2024 a 31/12/2024.

![comparando processos](./graficos/comparacao.png)

### Teste no Q1 2025

Ao testar 10000 alocações diferentes para 25 ativos, o melhor Sharpe obtido foi:

![q1 2025](./graficos/q1comp.png)

## Estrutura do Projeto

-   `main.py`: Arquivo principal com a interface do usuário
-   `sequential.py`: Implementação da otimização sequencial
-   `paralel.py`: Implementação da otimização paralela
-   `test_portfolio.py`: Script para testar carteiras específicas
-   `graficos/`: Diretório contendo os gráficos gerados
-   `scripts/`: Scripts auxiliares

## Métricas Calculadas

O projeto calcula várias métricas importantes para análise de carteiras:

1. **Retorno Esperado Anualizado**: Média dos retornos diários multiplicada por 252 (dias úteis)
2. **Volatilidade Anualizada**: Desvio padrão dos retornos anualizado
3. **Sharpe Ratio**: Retorno esperado dividido pela volatilidade (sem taxa livre de risco)
4. **Retorno Acumulado**: Retorno total no período analisado
5. **Contribuição por Ativo**: Impacto individual de cada ativo no retorno total

## API de Dados

A API que fornece os dados históricos pode ser encontrada [aqui](https://github.com/marchettomarcelo/yahoo-dow-data-py). Ela fornece:

-   Retornos diários dos ativos do Dow Jones
-   Dados históricos atualizados
-   Interface REST simples e eficiente
