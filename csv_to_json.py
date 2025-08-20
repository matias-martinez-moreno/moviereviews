import pandas as pd
import json

# Leer el archivo CSV
df = pd.read_csv('movies_initial.csv')

# Convertir a JSON con orient='records'
movies_json = df.to_json(orient='records', indent=2)

# Guardar el archivo JSON
with open('movies.json', 'w', encoding='utf-8') as f:
    f.write(movies_json)

print("Archivo movies.json creado exitosamente!")
