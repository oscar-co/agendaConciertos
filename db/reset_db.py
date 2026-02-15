from db.database import engine, Base
from db import models

def reset_db():
    Base.metadata.drop_all(bind=engine)     # borra tablas existentes
    Base.metadata.create_all(bind=engine)   # crea con el modelo actualizado

if __name__ == "__main__":
    reset_db()
    print("Tablas recreadas.")