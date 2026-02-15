from parsers.movistar_arena import parse_movistar_arena

VENUES = [
    {
        "venue": "Movistar Arena",
        "url": "https://www.movistararena.es/calendario?categoria=Conciertos",
        "parser": parse_movistar_arena,
        "debug_html": "response_movistar_arena.html",
        "city": "Madrid",
    },
]