import os
from dotenv import load_dotenv

load_dotenv() 

# devuelve debugFiles por defecto si no se le indica otra en el .env
DEBUG_DIR = os.getenv("DEBUG_DIR", "debugFiles")
