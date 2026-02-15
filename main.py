import datetime as dt
import json
from pathlib import Path

import requests

from config.settings import DEBUG_DIR
from config.venues import VENUES
from config.http import HEADERS

from db.database import SessionLocal
from db.repository import save_concerts


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


def ensure_debug_dir() -> Path:
    debug_dir = Path(DEBUG_DIR)
    debug_dir.mkdir(parents=True, exist_ok=True)
    return debug_dir


def save_debug_html(debug_dir: Path, filename: str, html: str) -> None:
    (debug_dir / filename).write_text(html, encoding="utf-8")


def write_output_json(debug_dir: Path, output: dict) -> None:
    output_json_path = debug_dir / "concerts_madrid.json"
    with output_json_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4, default=to_jsonable)


def main():
    all_concerts: list[dict] = []
    debug_dir = ensure_debug_dir()

    for v in VENUES:
        venue_name = v["venue"]
        url = v["url"]
        parser = v["parser"]
        debug_file = v["debug_html"]

        print(f"\n==> Descargando: {venue_name}")
        html = fetch(url)

        save_debug_html(debug_dir, debug_file, html)

        concerts = parser(html, source_url=url, limit=3)
        print(f"   Conciertos parseados: {len(concerts)}")

        all_concerts.extend(concerts)

    # Guardar en BD
    db = SessionLocal()
    try:
        affected = save_concerts(db, all_concerts)
        print(f"Filas afectadas en BD (insert/update): {affected}")
    finally:
        db.close()

    # Export JSON (debug / reporte)
    output = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "city": "Madrid",
        "concerts": all_concerts,
    }
    write_output_json(debug_dir, output)

    print(f"\nOK: guardado concerts_madrid.json con {len(all_concerts)} conciertos")


if __name__ == "__main__":
    main()
