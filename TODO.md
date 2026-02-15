el error que da ahora mismo es porque cambien los modelospara que hubiera una nueva tabla con las salas aparte y me da que esta buscando en la tabla conciertos el noombre de la sala cuando solo va a encontrar un ID... hay que modificar todo eso
algo tal que asi:

✅ Solución: en Concert debes asignar venue_id (int) o venue (objeto Venue)

Como tu modelo ahora tiene:

venue_id (columna FK)

venue (relationship)

Tienes que hacer una de estas dos cosas:

Opción A (recomendada): asignar venue_id=venue.id
row = Concert(
    venue_id=venue.id,
    artist=c["artist"],
    event_date=event_date_obj,
    event_time=event_time_obj,
    ticket_url=c["ticket_url"],
    source_url=c["source_url"],
    last_seen_at=now_utc,
    created_at=now_utc,
)

Opción B: asignar venue=venue (objeto ORM)
row = Concert(
    venue=venue,  # ✅ es una instancia Venue, no string
    ...
)