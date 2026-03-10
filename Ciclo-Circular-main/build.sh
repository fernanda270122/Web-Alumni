#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

# --- AGREGA ESTA LÍNEA AQUÍ ---
# Le decimos a Django que marque como 'hechas' las migraciones de admin_interface sin ejecutarlas
python manage.py migrate admin_interface --fake
# ------------------------------

python manage.py migrate