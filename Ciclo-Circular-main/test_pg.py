import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

print("DATABASE_URL:", os.getenv('DATABASE_URL'))

with open(r'C:\Program Files\PostgreSQL\18\data\pg_hba.conf', 'rb') as f:
    data = f.read()
print(data[90:110])
print('byte 96:', hex(data[96]))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cicloProduccion.settings')

import django
django.setup()

from django.conf import settings
print("BD:", settings.DATABASES['default'])

import psycopg2
try:
    conn = psycopg2.connect(
        dbname='ciclo_circular_local',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    print("Conexión exitosa!")
except Exception as e:
    print("Error:", type(e).__name__, str(e))