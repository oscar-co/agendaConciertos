import os
from dotenv import load_dotenv

load_dotenv() 

# devuelve debugFiles por defecto si no se le indica otra en el .env
DEBUG_DIR = os.getenv("DEBUG_DIR", "debugFiles")

CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")