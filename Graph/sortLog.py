import pandas as pd
from datetime import datetime

# Ruta del archivo de log
log_file = '../RMI/logCentralizado.log'
sorted_log_file = 'logCentralizado_ordenado.log'

# Leer el archivo de log
with open(log_file, 'r') as file:
    data = []
    for line in file:
        parts = line.strip().split(', ')
        timestamp = datetime.strptime(parts[0], '%Y-%m-%d %H:%M:%S')
        data.append([timestamp] + parts[1:])

# Crear un DataFrame y ordenar por fecha y hora
df = pd.DataFrame(data, columns=['timestamp', 'event_type', 'juego', 'action', 'arg1', 'arg2', 'arg3'])
df = df.sort_values(by='timestamp')

# Guardar el log ordenado en un nuevo archivo
with open(sorted_log_file, 'w') as file:
    for row in df.itertuples(index=False):
        line = f"{row.timestamp.strftime('%Y-%m-%d %H:%M:%S')}, {row.event_type}, {row.juego}, {row.action}"
        if row.arg1:
            line += f", {row.arg1}"
        if row.arg2:
            line += f", {row.arg2}"
        if row.arg3:
            line += f", {row.arg3}"
        file.write(line + '\n')

print(f"Log ordenado guardado en {sorted_log_file}")

