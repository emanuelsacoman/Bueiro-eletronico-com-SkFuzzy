import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Passo 1: Definir as variáveis linguísticas

# Variáveis de entrada
temperature = ctrl.Antecedent(np.arange(-40, 41, 1), 'temperature')
water_level = ctrl.Antecedent(np.arange(2, 11, 1), 'water_level')
luminosity = ctrl.Antecedent(np.arange(0, 1025, 1), 'luminosity')
humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')

# Variável de saída
sewer_state = ctrl.Consequent(np.arange(0, 101, 1), 'sewer_state')

# Passo 2: Definir as funções de pertinência

# Funções de pertinência para temperatura
temperature['low'] = fuzz.trimf(temperature.universe, [-40, -40, 15])
temperature['medium'] = fuzz.trimf(temperature.universe, [10, 16, 22])
temperature['high'] = fuzz.trimf(temperature.universe, [15, 40, 40])

# Funções de pertinência para nível da água
water_level['low'] = fuzz.trimf(water_level.universe, [2, 2, 5])
water_level['medium'] = fuzz.trimf(water_level.universe, [4, 5.5, 7])
water_level['high'] = fuzz.trimf(water_level.universe, [5, 10, 10])

# Funções de pertinência para luminosidade
luminosity['low'] = fuzz.trimf(luminosity.universe, [0, 0, 600])
luminosity['medium'] = fuzz.trimf(luminosity.universe, [400, 575, 750])
luminosity['high'] = fuzz.trimf(luminosity.universe, [600, 1024, 1024])

# Funções de pertinência para umidade
humidity['low'] = fuzz.trimf(humidity.universe, [0, 0, 50])
humidity['medium'] = fuzz.trimf(humidity.universe, [40, 50, 60])
humidity['high'] = fuzz.trimf(humidity.universe, [60, 100, 100])

# Funções de pertinência para estado do bueiro
sewer_state['closed'] = fuzz.trimf(sewer_state.universe, [0, 0, 50])
sewer_state['partially_open'] = fuzz.trimf(sewer_state.universe, [25, 50, 75])
sewer_state['open'] = fuzz.trimf(sewer_state.universe, [50, 100, 100])

# Passo 3: Definir as regras fuzzy

rule1 = ctrl.Rule((water_level['high'] & luminosity['low']) | 
                  (temperature['high'] & water_level['medium'] & luminosity['low']) | 
                  (temperature['high'] & water_level['medium'] & luminosity['medium'] & humidity['high']),
                  sewer_state['open'])

rule2 = ctrl.Rule((humidity['high'] & water_level['low'] & luminosity['medium']) | 
                  (temperature['medium'] & humidity['high'] & water_level['low']),
                  sewer_state['partially_open'])

rule3 = ctrl.Rule((temperature['high'] & humidity['low'] & luminosity['high']) | 
                  (temperature['low'] & luminosity['high'] & humidity['medium'] & water_level['low']),
                  sewer_state['closed'])

# Passo 4: Criar o sistema de controle fuzzy
sewer_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
sewer = ctrl.ControlSystemSimulation(sewer_ctrl)

# Passo 5: Fornecer as entradas e calcular a saída
# Exemplo: definir valores de entrada
sewer.input['temperature'] = 25
sewer.input['water_level'] = 3
sewer.input['luminosity'] = 600
sewer.input['humidity'] = 75

# Calcular a saída
sewer.compute()

# Obter o valor de saída defuzzificado
print(f"Estado do Bueiro: {sewer.output['sewer_state']}")
sewer_state_value = sewer.output['sewer_state']

# Classificar a saída
if sewer_state_value <= 33:
    state = 'Fechado'
elif sewer_state_value <= 66:
    state = 'Parcialmente Aberto'
else:
    state = 'Aberto'

print(f"Estado do Bueiro: {state}")

# Passo 6: Visualizar as funções de pertinência (opcional)

temperature.view(sim=sewer)
water_level.view(sim=sewer)
luminosity.view(sim=sewer)
humidity.view(sim=sewer)
sewer_state.view(sim=sewer)

# Mostrar os gráficos e manter a janela aberta
plt.show()
