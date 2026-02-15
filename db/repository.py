import datetime as dt

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from db.models import Venue, Concert


def get_or_create_venue(db, name: str, city: str, source_url: str) -> Venue:
    venue = db.execute(select(Venue).where(Venue.name == name)).scalar_one_or_none()
    if venue:
        return venue

    venue = Venue(name=name, city=city, source_url=source_url)
    db.add(venue)
    db.flush()  # obtiene venue.id sin hacer commit aún
    return venue


def save_concerts(db, concerts: list[dict]) -> int:
    """
    Inserta conciertos en PostgreSQL usando UPSERT:
    - Si NO existen (según uq_concert_identity): INSERT
    - Si YA existen: UPDATE de campos "volátiles" (last_seen_at, ticket_url, source_url)

    Devuelve el nº de filas afectadas (insertadas o actualizadas).
    """
    if not concerts:
        return 0

    now = dt.datetime.now(dt.timezone.utc)

    # 1) Preparar filas para insertar en bulk
    rows: list[dict] = []
    for c in concerts:
        venue = get_or_create_venue(
            db,
            name=c["venue_name"],
            city="Madrid",
            source_url=c["source_url"],
        )

        rows.append({
            "venue_id": venue.id,
            "artist": c["artist"],
            "event_date": c["event_date"],                 # dt.date
            "event_time": c.get("event_time"),             # dt.time | None
            "ticket_url": c["ticket_url"],
            "source_url": c["source_url"],
            "last_seen_at": now,
            "created_at": now,
        })

    # 2) Construir INSERT ... ON CONFLICT ... DO UPDATE (PostgreSQL)
    stmt = pg_insert(Concert).values(rows)

    stmt = stmt.on_conflict_do_update(
        constraint="uq_concert_identity",  # el nombre EXACTO de tu UniqueConstraint
        set_={
            # "excluded" = los valores que venían en el INSERT
            "ticket_url": stmt.excluded.ticket_url,
            "source_url": stmt.excluded.source_url,
            "last_seen_at": stmt.excluded.last_seen_at,
            # created_at NO se toca para mantener la fecha de primera inserción
        },
    )

    # 3) Ejecutar y confirmar
    result = db.execute(stmt)
    db.commit()

    # rowcount aquí significa "filas afectadas" (insert o update).
    return int(result.rowcount or 0)
