from bs4 import BeautifulSoup
from urllib.parse import urljoin

from utils.dates import parse_date_es_day_month_year
from utils.time import parse_time_24h_with_h

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
        date = parse_date_es_day_month_year(date_raw)

        # Hora (ej: "20:30 H.")
        time_node = node.select_one("li.label-azulclaro")
        time_raw = time_node.get_text(" ", strip=True) if time_node else None
        time = parse_time_24h_with_h(time_raw)

        # Link comprar (relativo)
        buy_a = node.select_one("a.btn.btn-primary[href]")
        ticket_url = urljoin(source_url, buy_a["href"]) if buy_a and buy_a.get("href") else None

        # Filtro mínimo para evitar basura
        if not artist or not date or not ticket_url:
            continue

        results.append({
            "artist": artist,
            "venue": venue_name,
            "date": date,                 # DD-MM-YYYY
            "time": time,                 # HH:MM o None
            "ticket_url": ticket_url,
            "source": source_url
        })

    return results
