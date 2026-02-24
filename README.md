## Madrid Indie Concert Scraper

Aplicación en Python que:
Hace scraping de salas de conciertos de Madrid
Normaliza los datos
Los guarda en PostgreSQL usando SQLAlchemy ORM
Genera un JSON con los conciertos encontrados
Guarda HTML de debug por sala

# EndPoints
API Documentation

Swagger UI:
http://localhost:8000/docs

ReDoc documentation:
http://localhost:8000/redoc

Raw OpenAPI schema (JSON):
http://localhost:8000/openapi.json

- Main Endpoint: GET /concerts

Returns a paginated list of concerts with filtering options.

Query Parameters
Parameter	Type	Default	Description
upcoming	bool	true	If true, returns concerts from today to today + days.
days	int	60	Number of days ahead when upcoming=true.
q	string	–	Search by artist OR venue name (case-insensitive).
artist_q	string	–	Search by artist name only.
venue_q	string	–	Search by venue name only.
venue_id	int	–	Filter by venue ID.
date_from	date	–	Start date filter (YYYY-MM-DD).
date_to	date	–	End date filter (YYYY-MM-DD).
page	int	1	Page number.
page_size	int	25	Items per page (max 100).

- Examples
Default (upcoming 60 days)
GET /concerts

Next 14 days only
GET /concerts?upcoming=true&days=14

Disable upcoming window
GET /concerts?upcoming=false

Search by artist or venue
GET /concerts?q=mayhem

Search only by venue
GET /concerts?venue_q=wizink

Custom date range
GET /concerts?upcoming=false&date_from=2025-01-01&date_to=2025-12-31

# Response Structure
{
  "items": [...],
  "page": 1,
  "page_size": 25,
  "total": 42
}


- Requisitos
Python 3.11+ (recomendado)
Docker + Docker Compose
pip

# Instalación paso a paso
- Clonar el proyecto
git clone https://github.com/oscar-co/agendaConciertos
cd agendaConcerts

- Crear entorno virtual (venv)

Desde la raíz del proyecto:

Mac / Linux
python3 -m venv .venv
source .venv/bin/activate


Cuando esté activo verás algo así:
(.venv) usuario@maquina agendaConcerts %

- Instalar dependencias

Con el venv activo:
pip install -r requirements.txt
Si no tienes requirements.txt, instala manualmente:
pip install requests sqlalchemy psycopg2-binary python-dotenv beautifulsoup4

🐘 Base de Datos (PostgreSQL con Docker)
- Levantar PostgreSQL
Desde la raíz del proyecto:
docker compose up -d

Verifica que está corriendo:
docker ps

Deberías ver el contenedor concerts-postgres.

- Crear tablas en la base de datos

Con el venv activo:
python -m db.scripts.init_db

Esto crea:
venues
concerts

⚙️ Configuración
Archivo .env
En la raíz del proyecto crea un archivo .env:
DEBUG_DIR=debugFiles
Esto define dónde se guardan los HTML de debug.
Si no existe, se usará debugFiles por defecto.


# !!!!! Ejecutar la aplicación

Con el entorno virtual activo:
Forma recomendada
EJECUTAR SCRAPING:  python -m scraping.cli

ARRANCAR API: uvicorn api.main:app --reload



- Qué ocurre al ejecutar
Descarga la página de cada sala
Guarda el HTML en la carpeta definida en .env
Parsea los conciertos
Inserta nuevos conciertos en PostgreSQL
Actualiza last_seen_at si ya existen
Genera concerts_madrid.json

Salida típica:
==> Descargando: Movistar Arena
   Conciertos parseados: 2
Insertados: 2 | Actualizados(last_seen): 0
OK: guardado concerts_madrid.json con 2 conciertos


# Estructura del Proyecto
├── README.md
├── TODO.md
├── __pycache__
│   ├── config.cpython-313.pyc
│   └── main.cpython-313.pyc
├── config
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── http.cpython-313.pyc
│   │   ├── settings.cpython-313.pyc
│   │   └── venues.cpython-313.pyc
│   ├── http.py
│   ├── settings.py
│   └── venues.py
├── db
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── database.cpython-313.pyc
│   │   ├── init_db.cpython-313.pyc
│   │   ├── models.cpython-313.pyc
│   │   ├── repository.cpython-313.pyc
│   │   └── reset_db.cpython-313.pyc
│   ├── database.py
│   ├── models.py
│   ├── repository.py
│   └── scripts
│       ├── __pycache__
│       ├── init_db.py
│       └── reset_db.py
├── debugFiles
│   ├── concerts_madrid.json
│   ├── response_elsol.html
│   ├── response_lariviera.html
│   └── response_movistar_arena.html
├── docker-compose.yml
├── main.py
├── parsers
│   ├──  __init__.py
│   ├── __pycache__
│   │   ├── elsol.cpython-313.pyc
│   │   ├── lariviera.cpython-313.pyc
│   │   └── movistar_arena.cpython-313.pyc
│   ├── elsol.py
│   ├── lariviera.py
│   └── movistar_arena.py
├── scraping
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── fetch.cpython-313.pyc
│   │   └── runner.cpython-313.pyc
│   ├── fetch.py
│   └── runner.py
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-313.pyc
    │   ├── dates.cpython-313.pyc
    │   ├── dates_constants.cpython-313.pyc
    │   ├── normalize_datetime.cpython-313.pyc
    │   └── time.cpython-313.pyc
    ├── dates_constants.py
    └── normalize_datetime.py


🧹 Reiniciar todo desde cero

Si quieres resetear la base de datos:

docker compose down -v
docker compose up -d
python -m db.scripts.reset_db

📊 Consultar la base de datos manualmente

Entrar en PostgreSQL:
docker exec -it concerts-postgres psql -U concerts_user -d concerts

Ver tablas:
\dt

Ver conciertos:
SELECT * FROM concerts ORDER BY event_date;

Salir:
\q
