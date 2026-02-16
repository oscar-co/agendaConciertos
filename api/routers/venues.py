from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.deps import get_db
from db.models import Venue

router = APIRouter(prefix="/venues", tags=["venues"])

@router.get("")
def list_venues(db: Session = Depends(get_db)):
    venues = db.execute(select(Venue).order_by(Venue.name.asc())).scalars().all()
    return [
        {
            "id": v.id,
            "name": v.name,
            "city": v.city,
            "source_url": v.source_url,
            "created_at": v.created_at.isoformat(),
        }
        for v in venues
    ]
