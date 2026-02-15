from pathlib import Path
from config.venues import VENUES
from scraping.fetch import fetch

def run_scraping(debug_dir: Path, limit: int | None = None) -> list[dict]:
    all_concerts: list[dict] = []

    for v in VENUES:
        venue_name = v["venue"]
        url = v["url"]
        parser = v["parser"]
        debug_file = v["debug_html"]

        print(f"\n==> Descargando: {venue_name}")
        html = fetch(url)

        (debug_dir / debug_file).write_text(html, encoding="utf-8")

        concerts = parser(html, source_url=url, limit=limit)
        print(f"   Conciertos parseados: {len(concerts)}")

        all_concerts.extend(concerts)

    return all_concerts
