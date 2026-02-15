import datetime as dt
import re
from typing import Any, Optional

from utils.dates_constants import MONTHS_ES

# --- DATE ---

def normalize_date(value: Any, default_year: int | None = None) -> Optional[dt.date]:
    """
    Acepta:
      - dt.date / dt.datetime
      - "2026-02-17" (ISO)
      - "17-02-2026" / "17/02/2026"
      - "Miércoles 28 enero 2026"
      - "24 de enero de 2026"
      - "jueves 29 enero" + default_year
    Devuelve dt.date o None.
    """
    if value is None:
        return None

    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value

    if not isinstance(value, str):
        return None

    s = value.strip().lower()
    if not s:
        return None

    # 1) ISO: YYYY-MM-DD
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        pass

    # 2) DD-MM-YYYY o DD/MM/YYYY
    m = re.fullmatch(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", s)
    if m:
        d, mo, y = map(int, m.groups())
        return dt.date(y, mo, d)

    # 3) "24 de enero de 2026"
    m = re.search(r"(\d{1,2})\s+de\s+([a-záéíóúñ]+)\s+de\s+(\d{4})", s)
    if m:
        day, month_name, year = m.groups()
        month = MONTHS_ES.get(month_name)
        if month:
            return dt.date(int(year), int(month), int(day))

    # 4) "Miércoles 28 enero 2026" (o sin día de semana)
    m = re.search(r"(\d{1,2})\s+([a-záéíóúñ]+)\s+(\d{4})", s)
    if m:
        day, month_name, year = m.groups()
        month = MONTHS_ES.get(month_name)
        if month:
            return dt.date(int(year), int(month), int(day))

    # 5) "jueves 29 enero" + default_year
    m = re.search(r"(\d{1,2})\s+([a-záéíóúñ]+)", s)
    if m and default_year is not None:
        day, month_name = m.groups()
        month = MONTHS_ES.get(month_name)
        if month:
            return dt.date(int(default_year), int(month), int(day))

    return None


# --- TIME ---

def normalize_time(value: Any) -> Optional[dt.time]:
    """
    Acepta:
      - dt.time / dt.datetime
      - "21:00", "21.00", "21:00 h", "20:30 H."
      - "9:00 PM"
      - "21.00 - 23.30h" (coge el inicio)
    Devuelve dt.time o None.
    """
    if value is None:
        return None

    if isinstance(value, dt.datetime):
        return value.time().replace(microsecond=0)
    if isinstance(value, dt.time):
        return value.replace(microsecond=0)

    if not isinstance(value, str):
        return None

    s = value.strip().upper()
    if not s:
        return None

    # 1) AM/PM: "9:00 PM"
    m = re.search(r"(\d{1,2}):(\d{2})\s*(AM|PM)", s)
    if m:
        hh, mm, ap = m.groups()
        hh = int(hh)
        mm = int(mm)
        if ap == "PM" and hh != 12:
            hh += 12
        if ap == "AM" and hh == 12:
            hh = 0
        return dt.time(hh, mm)

    # 2) Rango: "21.00 - 23.30H" -> coge primera hora
    m = re.search(r"(\d{1,2})[.:](\d{2})", s)
    if m:
        hh, mm = m.groups()
        return dt.time(int(hh), int(mm))

    return None
