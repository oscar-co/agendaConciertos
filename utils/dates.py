import re
from utils.dates_constants import MONTHS_ES  # o deja MONTHS_ES aquí mismo


def parse_date_es_full(date_raw: str) -> str | None:
    """'24 de enero de 2026' -> '2026-01-24'"""
    if not date_raw:
        return None
    s = date_raw.strip().lower()
    m = re.search(r"(\d{1,2})\s+de\s+([a-záéíóúñ]+)\s+de\s+(\d{4})", s)
    if not m:
        return None
    day, month_name, year = m.groups()
    month = MONTHS_ES.get(month_name)
    if not month:
        return None
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def parse_date_es_day_month(date_raw: str, year: int) -> str | None:
    """'jueves 29 enero' + year -> '2026-01-29'"""
    if not date_raw:
        return None
    s = date_raw.strip().lower()
    m = re.search(r"(\d{1,2})\s+([a-záéíóúñ]+)", s)
    if not m:
        return None
    day, month_name = m.groups()
    month = MONTHS_ES.get(month_name)
    if not month:
        return None
    return f"{year:04d}-{month:02d}-{int(day):02d}"


def parse_date_es_day_month_year(date_raw: str) -> str | None:
    """
    'Miércoles 28 enero 2026' -> '28-01-2026'
    """
    if not date_raw:
        return None

    s = date_raw.strip().lower()
    m = re.search(r"(\d{1,2})\s+([a-záéíóúñ]+)\s+(\d{4})", s)
    if not m:
        return None

    day, month_name, year = m.groups()
    month = MONTHS_ES.get(month_name)
    if not month:
        return None

    return f"{int(day):02d}-{int(month):02d}-{int(year):04d}"