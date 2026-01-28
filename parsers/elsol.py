from bs4 import BeautifulSoup
from utils.time import parse_time_range_start
from utils.dates import parse_date_es_day_month


def parse_elsol(html: str, source_url: str, default_year: int = 2026, limit: int | None = None) -> list[dict]:
    """
    Parser Sala El Sol.
    Devuelve list[dict] en el formato común:
    {artist, venue, date, time, ticket_url, source}
    """
    soup = BeautifulSoup(html, "lxml")

    # Cada "día" parece estar agrupado en un div.agenda.gran-contenedor-agenda
    # y dentro hay contenedores de evento. En tu snippet el evento está dentro de .contenedor-2
    event_nodes = soup.select("div.contenedor-2")

    if limit is not None:
        event_nodes = event_nodes[:limit]

    venue_name = "Sala El Sol"
    results: list[dict] = []

    for node in event_nodes:
        # 1) Artista + link a la página del evento (no necesariamente tickets)
        title_a = node.select_one("p.nombre_evento a")
        artist = title_a.get_text(strip=True) if title_a else None

        # 2) Fecha: NO está dentro de contenedor-2 en tu snippet, está en un bloque cercano.
        # Para este primer parser, intentamos buscar hacia arriba el bloque de agenda que lo contiene.
        # Buscamos el ancestro más cercano con clase 'gran-contenedor-agenda' y ahí pillamos la fecha-superior.
        date_raw = None
        wrapper = node.find_parent("div", class_="gran-contenedor-agenda")
        if wrapper:
            date_p = wrapper.select_one("p.fecha-superior") or wrapper.select_one("p.fecha-superior-publico")
            date_raw = date_p.get_text(" ", strip=True) if date_p else None

        date = parse_date_es_day_month(date_raw, year=default_year)

        # 3) Hora (rango)
        time_span = node.select_one("span.espacio")
        time_raw = time_span.get_text(" ", strip=True) if time_span else None
        time = parse_time_range_start(time_raw)

        # 4) Ticket URL (si existe)
        tickets_a = node.select_one('a.Tickets[href]')
        ticket_url = tickets_a["href"].strip() if tickets_a else None

        # Filtro mínimo: artista + fecha + ticket_url
        if not artist or not date or not ticket_url:
            continue

        results.append({
            "artist": artist,
            "venue": venue_name,
            "date": date,
            "time": time,
            "ticket_url": ticket_url,
            "source": source_url
        })

    return results
