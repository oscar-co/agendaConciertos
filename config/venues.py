from parsers.elsol import parse_elsol
from parsers.lariviera import parse_lariviera
from parsers.movistar_arena import parse_movistar_arena

VENUES = [
    
    {
        "venue": "Sala La Riviera",
        "url": "https://salariviera.com/conciertossalariviera/",
        "parser": parse_lariviera,
        "debug_html": "response_lariviera.html",
        "city": "Madrid",
    },
    {
        "venue": "Movistar Arena",
        "url": "https://www.movistararena.es/calendario?categoria=Conciertos",
        "parser": parse_movistar_arena,
        "debug_html": "response_movistar_arena.html",
        "city": "Madrid",
    },
	{
        "venue": "Sala El Sol",
        "url": "https://salaelsol.com/agenda/",
        "parser": parse_elsol,
        "debug_html": "response_elsol.html",
    }   
]


