
# 🚀 Documentación Técnica: Plataforma Ciclo-Circular (Alumni & Networking)

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20.svg?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon.tech-336791.svg?logo=postgresql&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC.svg?logo=tailwind-css&logoColor=white)
![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0.svg?logo=alpine.js&logoColor=white)
![Render](https://img.shields.io/badge/Render-Hosted-46E3B7.svg?logo=render&logoColor=white)

## 📖 1. Descripción General del Proyecto

Plataforma web diseñada para la gestión de usuarios, alumnos (Alumni) y coordinadores universitarios. El sistema permite la administración de perfiles, gestión de currículums (CVs), control de eventos (calendarios) y un potente ecosistema de **Networking**, donde los usuarios pueden compartir sus emprendimientos o lugares de trabajo, los cuales son categorizados automáticamente mediante Inteligencia Artificial.

---

## 🛠️ 2. Stack Tecnológico (Tech Stack)

Este proyecto sigue una arquitectura monolítica moderna, optimizada para un desarrollo rápido y un mantenimiento sencillo.

### Backend & Core
* **Lenguaje:** Python 3.11+
* **Framework:** Django 5.x
* **Autenticación:** Django Allauth (Integración con Google OAuth2)
* **IA Generativa:** Google Gemini (`google-generativeai`) para clasificación de industrias.

### Frontend (Custom UI)
* **Estructura:** Django Templates (Arquitectura de herencia `base.html`).
* **Estilos:** Tailwind CSS (Enfoque *Utility-First* nativo en el HTML). Soporte total para *Dark Mode*.
* **Interactividad UI:** Alpine.js (Para modales, menús desplegables y lógica de estado del lado del cliente).
* **Peticiones Asíncronas:** HTMX (Para navegación fluida e interacciones sin recargar la página).
* **Iconografía:** Font Awesome 6.

### Base de Datos & Infraestructura (Producción)
* **Base de Datos:** PostgreSQL (Alojada en **Neon.tech** - Serverless Postgres).
* **Hosting Web:** **Render** (Platform as a Service).
* **Servidor WSGI:** Gunicorn.
* **Archivos Estáticos:** WhiteNoise.

---

## 💻 3. Configuración del Entorno Local (Local Setup)

Instrucciones paso a paso para que un nuevo desarrollador levante el proyecto en su máquina.

### Requisitos Previos
* Python 3.11 o superior.
* Git instalado.
* Cuenta de Neon.tech (o un entorno PostgreSQL local).

### Pasos de Instalación

**1. Clonar el repositorio:**
```bash
git clone [https://github.com/tu-usuario/Ciclo-Circular.git](https://github.com/tu-usuario/Ciclo-Circular.git)
cd Ciclo-Circular

2. Crear y activar el entorno virtual:
# En Windows:
python -m venv venv
venv\Scripts\activate

# En macOS/Linux:
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias:
pip install -r requirements.txt

4. Configurar Variables de Entorno (.env):
Crea un archivo llamado .env en la raíz del proyecto (al mismo nivel que manage.py) y agrega las siguientes variables. (Nota: Nunca subas este archivo a GitHub).
# Configuración Básica
SECRET_KEY=tu_secret_key_super_segura
DEBUG=True

# Base de Datos (URL proporcionada por Neon.tech)
DATABASE_URL=postgres://usuario:password@ep-midominio.neon.tech/neondb?sslmode=require

# Integraciones
GEMINI_API_KEY=tu_clave_de_google_ai_studio
MERCADOPAGO_ACCESS_TOKEN=tu_token_opcional

# Credenciales OAuth de Google (Login)
GOOGLE_CLIENT_ID=tu_client_id.apps.googleusercontent.com
GOOGLE_SECRET=tu_client_secret

5. Aplicar Migraciones:
Si es la primera vez que clonas o si hubo cambios recientes en los modelos:
python manage.py makemigrations
python manage.py migrate

6. Crear Superusuario (Admin):
python manage.py createsuperuser

7. Iniciar el Servidor de Desarrollo:
python manage.py runserver

El proyecto estará disponible en http://127.0.0.1:8000/.
🚀 4. Despliegue en Producción (Render + Neon)
El proyecto está configurado para integración continua (CI/CD) a través de GitHub hacia Render.
Configuración en Neon (Base de Datos)
 * La base de datos vive en Neon.tech.
 * Al obtener el Connection String de Neon, asegúrate de añadir ?sslmode=require al final de la URL para evitar problemas de conexión segura.
Configuración en Render (Web Service)
 * Build Command: ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   
 * Start Command: (Crucial: Ejecuta las migraciones antes de iniciar Gunicorn para evitar errores de BD tras un despliegue).
   python manage.py migrate && gunicorn cicloProduccion.wsgi

Variables de Entorno en Render (Environment):
Debes replicar todas las variables del archivo .env local en la pestaña Environment de Render. Asegúrate de configurar DEBUG=False.
📂 5. Arquitectura y Estructura Clave
 * cicloProduccion/: Carpeta core de configuraciones de Django (settings.py, urls.py, wsgi.py).
 * user/ y administrador/: Aplicaciones principales que manejan la lógica de negocio y permisos (Admin vs Coordinador vs Alumno).
 * Modelos Clave (models.py):
   * Usuario (Custom User Model): Extiende de AbstractUser añadiendo campos de ubicación, teléfono, rol y universidad.
   * TrabajoEmpresa: Relación 1 a N con el Usuario para su red de networking.
 * Integración IA: La función obtener_categoria_con_ia utiliza Gemini 1.5 Flash para leer el nombre y descripción de la empresa de un usuario y asignarle una industria automáticamente.
⚠️ 6. Notas Importantes y Buenas Prácticas (Para futuros Devs)
 * Tailwind CSS (Frontend): No crees archivos .css separados a menos que sea estrictamente necesario. Utilizamos el enfoque Utility-First. Los estilos se modifican directamente en los atributos class="..." de los archivos HTML.
 * Manejo de Formularios POST con HTMX: Si un formulario tiene integración con pasarelas externas (como el Login de Google), asegúrate de usar el atributo hx-disable en la etiqueta <form> para evitar que HTMX intercepte la redirección por políticas CORS.
 * Seguridad y Login Google: El sistema utiliza Django Allauth con la configuración SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True. Si un usuario inicia sesión con Google, su cuenta de Gmail se fusionará automáticamente con la cuenta existente en la BD que tenga el mismo correo.
 * Migraciones: Nunca alteres la base de datos en producción manualmente. Todo cambio en models.py debe ser procesado con makemigrations en local y luego pusheado a GitHub para que Render ejecute el migrate de forma automatizada.
Documentación mantenida por el equipo de Ingeniería Backend.




