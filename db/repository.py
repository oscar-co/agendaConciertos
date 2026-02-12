from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime

from db.models import Concert


def save_concerts(db: Session, concerts: list[dict]) -> int:
    """
    Inserta conciertos en la BD.
    Devuelve cuántos ha insertado realmente (ignorando duplicados).
    """
    inserted = 0

    for c in concerts:
        # Convertimos fecha DD-MM-YYYY -> datetime.date
        date_obj = datetime.strptime(c["date"], "%d-%m-%Y").date()

        # Convertimos hora HH:MM -> datetime.time (si existe)
        time_obj = None
        if c.get("time"):
            time_obj = datetime.strptime(c["time"], "%H:%M").time()

        row = Concert(
            artist=c["artist"],
            venue=c["venue"],
            date=date_obj,
            time=time_obj,
            ticket_url=c["ticket_url"],
            source_url=c["source_url"],
        )

        db.add(row)

        try:
            db.commit()
            inserted += 1
        except IntegrityError:
            db.rollback()  # duplicado u otra restricción

    return inserted
