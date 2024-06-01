import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variáveis fuzzy (antecedentes e consequentes)
distance = ctrl.Antecedent(np.arange(0, 11, 1), 'distance')
speed = ctrl.Antecedent(np.arange(0, 101, 1), 'speed')
braking = ctrl.Consequent(np.arange(0, 101, 1), 'braking')

# Funções de pertinência para a distância
distance['near'] = fuzz.trimf(distance.universe, [0, 0, 5])
distance['medium'] = fuzz.trimf(distance.universe, [0, 5, 10])
distance['far'] = fuzz.trimf(distance.universe, [5, 10, 10])

# Funções de pertinência para a velocidade
speed['low'] = fuzz.trimf(speed.universe, [0, 0, 50])
speed['medium'] = fuzz.trimf(speed.universe, [0, 50, 100])
speed['high'] = fuzz.trimf(speed.universe, [50, 100, 100])

# Funções de pertinência para a frenagem
braking['light'] = fuzz.trimf(braking.universe, [0, 0, 50])
braking['moderate'] = fuzz.trimf(braking.universe, [0, 50, 100])
braking['hard'] = fuzz.trimf(braking.universe, [50, 100, 100])

# Regras fuzzy
rule1 = ctrl.Rule(distance['near'] & speed['high'], braking['hard'])
rule2 = ctrl.Rule(distance['near'] & speed['medium'], braking['moderate'])
rule3 = ctrl.Rule(distance['near'] & speed['low'], braking['light'])
rule4 = ctrl.Rule(distance['medium'] & speed['high'], braking['moderate'])
rule5 = ctrl.Rule(distance['medium'] & speed['medium'], braking['light'])
rule6 = ctrl.Rule(distance['medium'] & speed['low'], braking['light'])
rule7 = ctrl.Rule(distance['far'] & speed['high'], braking['light'])
rule8 = ctrl.Rule(distance['far'] & speed['medium'], braking['light'])
rule9 = ctrl.Rule(distance['far'] & speed['low'], braking['light'])

# Criação do sistema de controle
braking_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
braking_simulation = ctrl.ControlSystemSimulation(braking_ctrl)

# Simulação do sistema de controle com entradas específicas
braking_simulation.input['distance'] = 4
braking_simulation.input['speed'] = 60

# Computar o resultado
braking_simulation.compute()

# Mostrar o resultado
print(f"Braking: {braking_simulation.output['braking']}")

# Plotar os gráficos de pertinência
distance.view()
speed.view()
braking.view(sim=braking_simulation)
