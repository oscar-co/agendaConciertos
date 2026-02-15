from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils.normalize_datetime import normalize_date, normalize_time

def parse_movistar_arena(html: str, source_url: str, limit: int | None = None) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")

    # Cada evento parece estar dentro de un div.product-thumb
    nodes = soup.select("div.product-thumb")
    if limit is not None:
        nodes = nodes[:limit]

    venue_name = "Movistar Arena"
    results: list[dict] = []

    for node in nodes:
        # Nombre / artista
        title_node = node.select_one("h5.title3lineas")
        artist = title_node.get_text(" ", strip=True) if title_node else None

        # Fecha (ej: "Miércoles 28 enero 2026")
        date_node = node.select_one("h2.product-title")
        date_raw = date_node.get_text(" ", strip=True) if date_node else None
        date = normalize_date(date_raw)

        # Hora (ej: "20:30 H.")
        time_node = node.select_one("li.label-azulclaro")
        time_raw = time_node.get_text(" ", strip=True) if time_node else None
        time = normalize_time(time_raw)

        # Link comprar (relativo)
        buy_a = node.select_one("a.btn.btn-primary[href]")
        ticket_url = urljoin(source_url, buy_a["href"]) if buy_a and buy_a.get("href") else None

        # Filtro mínimo para evitar basura
        if not artist or not date or not ticket_url:
            continue

        results.append({
            "artist": artist,
            "venue_name": venue_name,
            "event_date": date,                 # DD-MM-YYYY
            "event_time": time,                 # HH:MM o None
            "ticket_url": ticket_url,
            "source_url": source_url
        })

    return results
