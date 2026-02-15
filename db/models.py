import datetime as dt
from typing import Optional

from sqlalchemy import String, Integer, Date, Time, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    # 1-N
    concerts: Mapped[list["Concert"]] = relationship(
        back_populates="venue",
        cascade="all, delete-orphan",
    )


class Concert(Base):
    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # FK REAL (columna en la tabla)
    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    event_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    event_time: Mapped[Optional[dt.time]] = mapped_column(Time, nullable=True)

    ticket_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    source_url: Mapped[str] = mapped_column(String(1024), nullable=False)

    last_seen_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: dt.datetime.now(dt.timezone.utc),
    )

    # RELACIÓN ORM (no columna)
    venue: Mapped["Venue"] = relationship(back_populates="concerts")

    __table_args__ = (
        UniqueConstraint(
            "venue_id",
            "artist",
            "event_date",
            "event_time",
            name="uq_concert_identity",
        ),
    )
