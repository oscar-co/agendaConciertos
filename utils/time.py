import re

def parse_time_ampm(time_raw: str) -> str | None:
    """'9:00 PM' -> '21:00'"""
    if not time_raw:
        return None
    s = time_raw.strip().upper()
    m = re.search(r"(\d{1,2}):(\d{2})\s*(AM|PM)", s)
    if not m:
        return None
    hh, mm, ap = m.groups()
    hh = int(hh)
    if ap == "PM" and hh != 12:
        hh += 12
    if ap == "AM" and hh == 12:
        hh = 0
    return f"{hh:02d}:{mm}"

def parse_time_range_start(time_raw: str) -> str | None:
    """'21.00 - 23.30h' -> '21:00'"""
    if not time_raw:
        return None
    s = time_raw.strip().lower()
    m = re.search(r"(\d{1,2})[.:](\d{2})", s)
    if not m:
        return None
    hh, mm = m.groups()
    return f"{int(hh):02d}:{mm}"

def parse_time_24h_with_h(time_raw: str) -> str | None:
    """
    '20:30 H.' -> '20:30'
    """
    if not time_raw:
        return None

    s = time_raw.strip().upper()
    m = re.search(r"(\d{1,2}):(\d{2})", s)
    if not m:
        return None

    hh, mm = m.groups()
    return f"{int(hh):02d}:{mm}"
