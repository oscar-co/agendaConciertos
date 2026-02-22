import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from api.deps import get_db
from db.models import Concert, Venue

router = APIRouter(prefix="/concerts", tags=["concerts"])


def _today() -> dt.date:
    # Se evalúa por request (no se queda “congelado” al iniciar el servidor)
    return dt.date.today()


def _apply_filters(
    stmt,
    *,
    q: str | None,
    artist_q: str | None,
    venue_q: str | None,
    venue_id: int | None,
    date_from: dt.date | None,
    date_to: dt.date | None,
):
    # Búsqueda “general”: artista O sala
    if q:
        like = f"%{q}%"
        stmt = stmt.where(
            or_(
                Concert.artist.ilike(like),
                Venue.name.ilike(like),
            )
        )

    if artist_q:
        stmt = stmt.where(Concert.artist.ilike(f"%{artist_q}%"))

    if venue_q:
        stmt = stmt.where(Venue.name.ilike(f"%{venue_q}%"))

    if venue_id:
        stmt = stmt.where(Concert.venue_id == venue_id)

    if date_from:
        stmt = stmt.where(Concert.event_date >= date_from)

    if date_to:
        stmt = stmt.where(Concert.event_date <= date_to)

    return stmt


def _serialize_concert(c: Concert) -> dict:
    # Un solo sitio para decidir el “shape” del JSON
    return {
        "id": c.id,
        "artist": c.artist,
        "event_date": c.event_date.isoformat(),
        "event_time": c.event_time.isoformat() if c.event_time else None,
        "ticket_url": c.ticket_url,
        "source_url": c.source_url,
        "last_seen_at": c.last_seen_at.isoformat(),
        "created_at": c.created_at.isoformat(),
        "venue": {
            "id": c.venue.id,
            "name": c.venue.name,
            "city": c.venue.city,
            "source_url": c.venue.source_url,
        },
    }


@router.get("")
def list_concerts(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Search artist OR venue name contains"),
    artist_q: str | None = Query(default=None, description="Search artist contains"),
    venue_q: str | None = Query(default=None, description="Search venue name contains"),
    venue_id: int | None = Query(default=None),
    date_from: dt.date | None = Query(default=None),
    date_to: dt.date | None = Query(default=None),
    upcoming: bool = Query(default=True),
    days: int = Query(default=60, ge=1, le=365),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
):
    today = _today()

    if upcoming:
        if date_from is None:
            date_from = today
        if date_to is None:
            date_to = today + dt.timedelta(days=days)

    base = select(Concert).join(Venue)
    base = _apply_filters(
        base,
        q=q,
        artist_q=artist_q,
        venue_q=venue_q,
        venue_id=venue_id,
        date_from=date_from,
        date_to=date_to,
    )

    count_base = select(Concert.id).join(Venue)
    count_base = _apply_filters(
        count_base,
        q=q,
        artist_q=artist_q,
        venue_q=venue_q,
        venue_id=venue_id,
        date_from=date_from,
        date_to=date_to,
    )
    total = db.execute(select(func.count()).select_from(count_base.subquery())).scalar_one()

    # 4) Paginación + orden
    stmt = (
        base.order_by(Concert.event_date.asc(), Concert.event_time.asc().nulls_last())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    concerts = db.execute(stmt).scalars().all()

    return {
        "items": [_serialize_concert(c) for c in concerts],
        "page": page,
        "page_size": page_size,
        "total": int(total),
    }


@router.get("/{concert_id}")
def get_concert(concert_id: int, db: Session = Depends(get_db)):
    stmt = select(Concert).where(Concert.id == concert_id)
    c = db.execute(stmt).scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=404, detail="Concert not found")

    # aquí podrías decidir si quieres devolver venue también o no.
    return {
        "id": c.id,
        "artist": c.artist,
        "event_date": c.event_date.isoformat(),
        "event_time": c.event_time.isoformat() if c.event_time else None,
        "ticket_url": c.ticket_url,
        "source_url": c.source_url,
        "last_seen_at": c.last_seen_at.isoformat(),
        "created_at": c.created_at.isoformat(),
        "venue_id": c.venue_id,
    }