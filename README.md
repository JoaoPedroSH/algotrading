## Scope
1. Desenvolvimento do Simulador em MQL5 (MetaQuotes Language 5):
    1.1 Implementação do Simulador:
    Desenvolver um script ou EA (Expert Advisor) que simule negociações com base em regras predefinidas.
    O código deve ser capaz de executar operações de compra e venda, calcular ganhos ou perdas e manter um registro dos resultados.
    1.2 Integração de Modelos Matemáticos:
    Permitir que o simulador receba modelos matemáticos como entrada.
    Implementar a lógica necessária para incorporar esses modelos nas decisões de compra e venda.
2. Uso como Emissor de Sinais:
Modificar o código para gerar sinais de compra e venda com base nas decisões do modelo matemático.
Exibir esses sinais em um gráfico para facilitar a análise visual.
3. Trabalho nos Modelos Matemáticos:
    3.1 Calibração:
    Calibrar os modelos matemáticos usando dados históricos.
    Ajustar parâmetros para otimizar o desempenho do modelo.
    3.2 Tratamento de Dados:
    Desenvolver rotinas para tratamento de dados, incluindo limpeza, normalização e seleção de recursos relevantes.
    3.3 Backtesting:
    Implementar um sistema de backtesting para avaliar o desempenho histórico do modelo em diferentes cenários de mercado.
4. Equação Ótima e Algoritmo ABC:
Formular o problema de day trade como uma equação matemática.
Utilizar o Algoritmo ABC (Artificial Bee Colony) ou outro algoritmo apropriado para otimizar os parâmetros do modelo.
5. Integração com Page Flask:
Receber os sinais do modelo otimozado e fazer entradas de compra e venda  

## Flask ['https://flask.palletsprojects.com/en/3.0.x/installation/']

## Tailwind ['https://tailwindui.com/components/preview']

## MQL5 + Python ['https://www.mql5.com/en/docs/python_metatrader5']

## Prerequisites 
MetaTrader5
Microsoft Visual C++ 14.0 (Build Tool) ['https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/']

### Active Enviroment
.venv\Scripts\activate

### Start Server (Interactive Mode)
flask --app app run --debug 

### Init database
flask --app app init-db

### Start Run File 
python [name do arquivo].py

### Status Configs IA
0 - Preparado
1 - Executando
2 - Posicionado