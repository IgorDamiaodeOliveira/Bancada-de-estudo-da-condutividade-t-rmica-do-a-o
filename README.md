# Análise de Transferência de Calor por Condução

Este projeto oferece solução para analisar a transferência de calor por condução em um material sólido. Utilizando um **microcontrolador (Arduino)** e dois sensores de temperatura **DS18B20**, ele coleta dados de temperatura, realiza cálculos físicos em tempo real e visualiza os resultados. A comunicação é feita via porta serial, com os dados sendo plotados dinamicamente e salvos em um arquivo CSV.

## Componentes do Projeto

O repositório é dividido em três partes principais:

* **`coleta_temperatura_arduino.ino`**: O código para o Arduino que lê a temperatura de dois sensores DS18B20 e envia os valores formatados para a porta serial.
* **`fluxo_calor.py`**: Um script em Python que se conecta ao Arduino para ler as temperaturas e, a partir dos parâmetros do material, **calcula e exibe o fluxo de calor ($Q$)** em tempo real.
* **`condutividade.py`**: Um script em Python alternativo que, com base em um fluxo de calor ($Q$) pré-determinado, utiliza as leituras de temperatura para **calcular e exibir a condutividade térmica ($k$)** do material.

## Funcionalidades Principais

* **Aquisição de Dados**: Coleta contínua e confiável de dados de temperatura através de uma conexão serial.
* **Cálculos Físicos**: Aplicação da **Lei de Fourier da Condução de Calor** para calcular as grandezas físicas. A fórmula utilizada é:
    $$ Q = \frac{k \cdot A \cdot \Delta T}{L} $$
    Onde:
    * $Q$ é o fluxo de calor.
    * $k$ é a condutividade térmica.
    * $A$ é a área da seção transversal.
    * $\Delta T$ é a diferença de temperatura entre os sensores.
    * $L$ é a distância entre os sensores.
* **Visualização em Tempo Real**: Gráficos dinâmicos gerados com a biblioteca **Matplotlib** que mostram a variação das temperaturas e do valor calculado (fluxo de calor ou condutividade) ao longo do tempo.
* **Armazenamento de Dados**: Todos os dados coletados e calculados são automaticamente salvos em um arquivo **CSV** com carimbo de data e hora para análises futuras.

## Como Usar

Para replicar o experimento, siga estes passos:

1.  **Carregue o código do Arduino**: Abra o arquivo `coleta_temperatura_arduino.ino` na IDE do Arduino e faça o upload para o seu microcontrolador.
2.  **Conecte o Hardware**: Conecte os dois sensores de temperatura DS18B20 ao pino digital definido no código.
3.  **Execute o Script Python**: No seu computador, abra um terminal e execute o script desejado. **Lembre-se de verificar e ajustar a variável `porta` (`'COM11'` por padrão) nos scripts Python para corresponder à porta serial do seu Arduino.**

   * Para calcular o fluxo de calor: `python fluxo_calor.py`
   * Para calcular a condutividade térmica: `python condutividade.py`

Este projeto é uma ferramenta ideal para **experimentos de laboratório**, **projetos de estudantes** e **análise de princípios de termodinâmica**.
