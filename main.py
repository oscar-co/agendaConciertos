import json
import requests
from datetime import datetime, timezone
import datetime as dt

from pathlib import Path

from config import DEBUG_DIR
from parsers.movistar_arena import parse_movistar_arena
from db.database import SessionLocal
from db.repository import save_concerts

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IndieConcertScraper/0.1)"
}

VENUES = [
    {
        "venue": "Movistar Arena",
        "url": "https://www.movistararena.es/calendario?categoria=Conciertos",
        "parser": parse_movistar_arena,
        "debug_html": "response_movistar_arena.html",
    }
]

def to_jsonable(obj):
    if isinstance(obj, dt.time):
        return obj.strftime("%H:%M")
    if isinstance(obj, (dt.date, dt.datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def fetch(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text

def main():
    all_concerts = []

    # Creamos la carpeta de debug si no existe
    debug_dir = Path(DEBUG_DIR)
    debug_dir.mkdir(parents=True, exist_ok=True)

    for v in VENUES:
        venue_name = v["venue"]
        url = v["url"]
        parser = v["parser"]
        debug_file = v["debug_html"]

        print(f"\n==> Descargando: {venue_name}")
        html = fetch(url)

        # Guardar HTML dentro de debug_dir
        debug_path = debug_dir / debug_file
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(html)

        concerts = parser(html, source_url=url, limit=3)
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

    outputConcertListJsonFile = debug_dir /"concerts_madrid.json"
    with open( outputConcertListJsonFile, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4, default=to_jsonable)

    print(f"\nOK: guardado concerts_madrid.json con {len(all_concerts)} conciertos")

if __name__ == "__main__":
    main()
