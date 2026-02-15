🎵 Madrid Indie Concert Scraper

Aplicación en Python que:

Hace scraping de salas de conciertos de Madrid

Normaliza los datos

Los guarda en PostgreSQL usando SQLAlchemy ORM

Genera un JSON con los conciertos encontrados

Guarda HTML de debug por sala

📦 Requisitos

Python 3.11+ (recomendado)

Docker + Docker Compose

pip

🚀 Instalación paso a paso
1️⃣ Clonar el proyecto
git clone <repo-url>
cd agendaConcerts

2️⃣ Crear entorno virtual (venv)

Desde la raíz del proyecto:

Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1


Cuando esté activo verás algo así:

(.venv) usuario@maquina agendaConcerts %

3️⃣ Instalar dependencias

Con el venv activo:
pip install -r requirements.txt


Si no tienes requirements.txt, instala manualmente:

pip install requests sqlalchemy psycopg2-binary python-dotenv beautifulsoup4

🐘 Base de Datos (PostgreSQL con Docker)
4️⃣ Levantar PostgreSQL

Desde la raíz del proyecto:

docker compose up -d


Verifica que está corriendo:

docker ps


Deberías ver el contenedor concerts-postgres.

5️⃣ Crear tablas en la base de datos

Con el venv activo:

python -m db.init_db


Esto crea:

venues

concerts

⚙️ Configuración
Archivo .env

En la raíz del proyecto crea un archivo .env:

DEBUG_DIR=debugFiles


Esto define dónde se guardan los HTML de debug.

Si no existe, se usará debugFiles por defecto.

▶️ Ejecutar la aplicación

Con el entorno virtual activo:

Forma recomendada
python main.py

Forma explícita (como tú lo haces)
/Users/oscarmb/Programing/python/agendaConcerts/.venv/bin/python /Users/oscarmb/Programing/python/agendaConcerts/main.py

📁 Qué ocurre al ejecutar

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

🗂 Estructura del Proyecto
agendaConcerts/
│
├── main.py
├── config.py
├── .env
├── docker-compose.yml
│
├── db/
│   ├── database.py
│   ├── models.py
│   ├── repository.py
│   └── init_db.py
│
├── parsers/
│   ├── movistar_arena.py
│   ├── lariviera.py
│   └── elsol.py
│
└── debugFiles/

🧹 Reiniciar todo desde cero

Si quieres resetear la base de datos:

docker compose down -v
docker compose up -d
python -m db.init_db

📊 Consultar la base de datos manualmente

Entrar en PostgreSQL:

docker exec -it concerts-postgres psql -U concerts_user -d concerts


Ver tablas:

\dt


Ver conciertos:

SELECT * FROM concerts ORDER BY event_date;


Salir:

\q

🧠 Flujo completo del sistema

Scraping → Parser → Normalización → ORM → PostgreSQL → JSON → (Futuro API / Web)

🔮 Próximos pasos posibles

Añadir más salas

Crear API con FastAPI

Añadir filtros por fecha

Generar frontend web

Añadir índices en PostgreSQL

Añadir logging estructurado