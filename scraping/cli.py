import datetime as dt
import json
from pathlib import Path

import requests

from config.settings import DEBUG_DIR
from config.venues import VENUES
from config.http import HEADERS

from db.database import SessionLocal
from db.repository import save_concerts

from scraping.runner import run_scraping


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


def write_output_json(debug_dir: Path, output: dict) -> Path:
    output_json_path = debug_dir / "concerts_madrid.json"
    with output_json_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4, default=to_jsonable)
    return output_json_path


def main():

    debug_dir = ensure_debug_dir()

    all_concerts = run_scraping(debug_dir, limit=3)

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
    output_json_path = write_output_json(debug_dir, output)

    print(f"\nOK: guardado {output_json_path.name} con {len(all_concerts)} conciertos")


if __name__ == "__main__":
    main()
