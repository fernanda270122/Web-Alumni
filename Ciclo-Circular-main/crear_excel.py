import pandas as pd
import os

# Definimos los datos de la plantilla
data = {
    'username': ['ejemplo.user'],
    'first_name': ['NombreEjemplo'],
    'last_name': ['ApellidoEjemplo'],
    'email': ['correo@ejemplo.com'],
    'area': ['Nombre Exacto de la Carrera']
}

# Creamos el DataFrame
df = pd.read_json(pd.DataFrame(data).to_json()) # Truco simple para convertir dict a df

# Aseguramos que la carpeta static exista
if not os.path.exists('static'):
    os.makedirs('static')

# Guardamos el archivo Excel
ruta = 'static/ejemplo_carga_usuarios.xlsx'
df.to_excel(ruta, index=False)

print(f"✅ Archivo creado exitosamente en: {ruta}")