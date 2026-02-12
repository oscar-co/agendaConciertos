import json
import requests
from datetime import datetime, timezone

from parsers.lariviera import parse_lariviera
from parsers.elsol import parse_elsol
from parsers.movistar_arena import parse_movistar_arena
from db.database import SessionLocal
from db.repository import save_concerts

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IndieConcertScraper/0.1)"
}

VENUES = [
    # {
    #     "venue": "Sala La Riviera",
    #     "url": "https://salariviera.com/conciertossalariviera/",
    #     "parser": parse_lariviera,
    #     "debug_html": "response_lariviera.html",
    # },
    # {
    #     "venue": "Sala El Sol",
    #     "url": "https://salaelsol.com/agenda/",
    #     "parser": parse_elsol,
    #     "debug_html": "response_elsol.html",
    # }
    # ,
    {
        "venue": "Movistar Arena",
        "url": "https://www.movistararena.es/calendario?categoria=Conciertos",
        "parser": parse_movistar_arena,
        "debug_html": "response_movistar_arena.html",
    }

    
]

def fetch(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text

def main():
    all_concerts = []

    for v in VENUES:
        venue_name = v["venue"]
        url = v["url"]
        parser = v["parser"]
        debug_file = v["debug_html"]

        print(f"\n==> Descargando: {venue_name}")
        html = fetch(url)

        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(html)

        concerts = parser(html, source_url=url, limit=2)
        print(f"   Conciertos parseados: {len(concerts)}")

        all_concerts.extend(concerts)
    
    db = SessionLocal()
    try:
        inserted = save_concerts(db, all_concerts)
        print(f"Insertados en BD: {inserted}")
    finally:
        db.close()

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "city": "Madrid",
        "concerts": all_concerts
    }

    with open("concerts_madrid.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print(f"\nOK: guardado concerts_madrid.json con {len(all_concerts)} conciertos")

if __name__ == "__main__":
    main()
