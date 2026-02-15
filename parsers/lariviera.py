from bs4 import BeautifulSoup
from utils.normalize_datetime import normalize_date, normalize_time


def parse_lariviera(html: str, source_url: str, limit: int | None = None) -> list[dict]:
    """
    Devuelve una lista de conciertos en formato común (list[dict]).
    - html: HTML ya descargado
    - source_url: URL de la agenda (para trazabilidad)
    - limit: si quieres limitar (ej. 5 para debug)
    """
    soup = BeautifulSoup(html, "lxml")
    articles = soup.select("article.act-post")

    if limit is not None:
        articles = articles[:limit]

    venue_name = "Sala La Riviera"
    results: list[dict] = []

    for art in articles:
        # Artista
        a_title = art.select_one("h2.title1 a") or art.select_one("h2.title2 a")
        artist = a_title.get_text(strip=True) if a_title else None

        # Fecha
        date_node = art.select_one("span.decm_date")
        date_raw = date_node.get_text(" ", strip=True) if date_node else None
        date = normalize_date(date_raw)

        # Hora
        time_node = art.select_one("span.decm_time")
        time_raw = time_node.get_text(" ", strip=True) if time_node else None
        time = normalize_time(time_raw)

        # Link de compra
        buy_link = art.select_one("a.act-view-more[href]") or art.select_one("a[href]")
        ticket_url = buy_link["href"].strip() if buy_link and buy_link.get("href") else None

        # Filtrado mínimo para evitar basura
        if not artist or not date or not ticket_url:
            continue

        results.append({
            "artist": artist,
            "venue_name": venue_name,
            "event_date": date,
            "event_time": time,                 # puede ser None si no vino bien
            "ticket_url": ticket_url,
            "source_url": source_url
        })

    return results