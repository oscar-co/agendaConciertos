import datetime as dt
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from api.deps import get_db
from db.models import Concert, Venue

router = APIRouter(prefix="/concerts", tags=["concerts"])


def _apply_filters(stmt, q: str | None, venue_id: int | None, date_from: dt.date | None, date_to: dt.date | None):
    if q:
        stmt = stmt.where(Concert.artist.ilike(f"%{q}%"))
    if venue_id:
        stmt = stmt.where(Concert.venue_id == venue_id)
    if date_from:
        stmt = stmt.where(Concert.event_date >= date_from)
    if date_to:
        stmt = stmt.where(Concert.event_date <= date_to)
    return stmt


@router.get("")
def list_concerts(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Search artist contains"),
    venue_id: int | None = Query(default=None),
    date_from: dt.date | None = Query(default=None),
    date_to: dt.date | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
):
    base = select(Concert).join(Venue)
    base = _apply_filters(base, q, venue_id, date_from, date_to)

    # Total (para paginación en React)
    count_stmt = select(func.count()).select_from(
        _apply_filters(select(Concert.id), q, venue_id, date_from, date_to).subquery()
    )
    total = db.execute(count_stmt).scalar_one()

    stmt = base.order_by(
        Concert.event_date.asc(),
        Concert.event_time.asc().nulls_last()
    ).offset((page - 1) * page_size).limit(page_size)

    concerts = db.execute(stmt).scalars().all()

    items = [
        {
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
        for c in concerts
    ]

    return {
        "items": items,
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


@router.get("/upcoming")
def upcoming(
    db: Session = Depends(get_db),
    days: int = Query(default=60, ge=1, le=365),
):
    today = dt.date.today()
    until = today + dt.timedelta(days=days)

    stmt = (
        select(Concert)
        .join(Venue)
        .where(Concert.event_date >= today, Concert.event_date <= until)
        .order_by(Concert.event_date.asc(), Concert.event_time.asc().nulls_last())
        .limit(200)
    )

    concerts = db.execute(stmt).scalars().all()
    return [
        {
            "id": c.id,
            "artist": c.artist,
            "event_date": c.event_date.isoformat(),
            "event_time": c.event_time.isoformat() if c.event_time else None,
            "venue": {"id": c.venue.id, "name": c.venue.name, "city": c.venue.city},
        }
        for c in concerts
    ]
