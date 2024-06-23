import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Ejecutar sortLog.py primero
subprocess.run(['python3', 'sortLog.py'], check=True)

# Configurar variables de entorno para el tamaño de la ventana
WINDOW_SIZE = int(os.getenv('WINDOW_SIZE', '1'))  # Tamaño de la ventana en minutos

# Especificar la ruta completa del archivo de log ordenado
log_file = 'logCentralizado_ordenado.log'
data = []

# Leer el archivo de log
with open(log_file, 'r') as file:
    for line in file:
        parts = line.strip().split(', ')
        timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
        event_type = parts[1]
        juego = parts[2]
        action = parts[3]
        args = parts[4:]
        data.append([timestamp, event_type, juego, action] + args)

columns = ['timestamp', 'event_type', 'juego', 'action', 'arg1', 'arg2', 'arg3']
df = pd.DataFrame(data, columns=columns)

# Filtrar las acciones iniciadas
df_ini = df[df['event_type'] == 'ini']

# Gráfico 1: Jugadores creados por equipo en un juego
created_players = df_ini[df_ini['action'] == 'crea-jugador'].groupby('arg1').size()
created_players.plot(kind='bar', title='Jugadores creados por equipo')
plt.xlabel('Equipo')
plt.ylabel('Número de jugadores')
print("Imprime Grafico 1")
plt.show()

# Gráfico 2: Jugadas realizadas por jugador en un juego
player_actions = df_ini[df_ini['action'].str.contains('lanza-dado')].groupby('arg2').size()
player_actions.plot(kind='bar', title='Jugadas realizadas por jugador')
plt.xlabel('Jugador')
plt.ylabel('Número de jugadas')
print("Imprime Grafico 2")
plt.show()

# Gráfico 3: Curvas de puntuación por equipo a través del tiempo
scores_ini = df[(df['event_type'] == 'ini') & (df['action'] == 'lanza-dado')]
scores_fin = df[(df['event_type'] == 'fin') & (df['action'] == 'lanza-dado')]

# Asegurar que la columna timestamp esté correctamente especificada para ambos DataFrames
scores_ini = scores_ini.rename(columns={'timestamp': 'timestamp_ini'})
scores_fin = scores_fin.rename(columns={'timestamp': 'timestamp_fin'})

# Combinar los DataFrames
scores = pd.merge(scores_ini, scores_fin, on=['juego', 'action', 'arg1', 'arg2'], suffixes=('_ini', '_fin'))

# Convertir las columnas de timestamp a datetime64[ns]
scores['timestamp_fin'] = pd.to_datetime(scores['timestamp_fin'], errors='coerce')
scores = scores.set_index('timestamp_fin')
print(pd.to_numeric(scores['arg3_fin'], errors='coerce'))
scores['puntos'] = pd.to_numeric(scores['arg3_fin'], errors='coerce')


# Ordenar por timestamp final para asegurar que los datos estén en orden cronológico
scores = scores.sort_values(by='timestamp_fin')
#print(scores['puntos'])
# Crear gráfico de curvas de puntuación por equipo a través del tiempo
teams = scores['arg1'].unique()
#print(teams)

plt.figure(figsize=(10, 6))  # Crear una figura para el gráfico

for team in teams:
    team_scores = scores[scores['arg1'] == team]['puntos'].cumsum()
    print(team_scores)
    if team_scores.empty:
        continue
    team_scores.plot(label=f'Equipo {team}')

# Configuración del gráfico
plt.title('Curvas de puntuación por equipo a través del tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Puntuación acumulada')
plt.legend(title='Equipos')
plt.grid(True)
print("Imprime Grafico 3")
plt.show()
"""
# Gráfico 4: Equipos creados por ventanas de tiempo
teams_created = df_ini[df_ini['action'] == 'crea-jugador'].set_index('timestamp')['arg1'].resample(f'{WINDOW_SIZE}min').nunique()
teams_created.plot(title='Equipos creados por ventanas de tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Número de equipos')
print("Imprime Grafico 4")
plt.show()

# Gráfico 5: Jugadores creados por ventanas de tiempo
players_created = df_ini[df_ini['action'] == 'crea-jugador'].set_index('timestamp')['arg2'].resample(f'{WINDOW_SIZE}min').nunique()
players_created.plot(title='Jugadores creados por ventanas de tiempo')
plt.xlabel('Tiempo')
plt.ylabel('Número de jugadores')
print("Imprime Grafico 5")
plt.show()
"""