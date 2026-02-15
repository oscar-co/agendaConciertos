Perfecto 👌
Te lo genero en formato Markdown checklist, listo para copiar como REFACTOR_PLAN.md en la raíz del proyecto.

📦 AgendaConcerts – Refactor & Improvement Roadmap

Documento de mejoras progresivas para evolucionar el proyecto de forma limpia y escalable.

🟢 FASE 1 – Mejoras de Bajo Riesgo (Alta Rentabilidad)
⬜ 1. Cache de venues en memoria
Crear venue_cache: dict[str, int]
Evitar SELECT repetidos en cada concierto
Reducir llamadas innecesarias a BD
Mejorar rendimiento en scrapes grandes

⬜ 2. Argumentos CLI con argparse
Añadir --limit
Añadir --debug
Añadir --no-json
Añadir --city
Permitir ejecutar el scraper sin tocar código

⬜ 3. Logging estructurado (en vez de print)
Configurar módulo logging
Definir niveles: DEBUG / INFO / WARNING / ERROR
Activar debug HTML solo en modo DEBUG
Reducir ruido en ejecución normal

🟡 FASE 2 – Mejora de Modelo y Consistencia
⬜ 4. Crear ConcertDTO (dataclass)
Reemplazar dict por objeto tipado
Evitar errores de keys mal escritas
Mejorar autocompletado
Facilitar validación futura

⬜ 5. Normalización centralizada
Parsers devuelven datos "raw"
Función común normaliza fechas y horas
El sistema solo maneja date y time
Evitar lógica duplicada en parsers

⬜ 6. Métricas reales (insert vs update)
Diferenciar:
nuevos conciertos
actualizados
ignorados
Mejorar trazabilidad del scraper

🟠 FASE 3 – Arquitectura y Escalabilidad
⬜ 7. Salida JSON por ciudad
Generar concerts_{city}.json
O incluir city dentro de cada concierto
Preparar soporte multi-ciudad

⬜ 8. Separar completamente a paquete agenda_concerts/
Mover todo el código dentro de un paquete
Mejorar imports
Preparar para tests y packaging futuro

⬜ 9. Tests de parsers (HTML fijo)
Guardar HTML de ejemplo
Crear tests en tests/parsers/
Validar número de conciertos
Validar fechas y horas correctas
Detectar roturas cuando cambie el HTML real

⬜ 10. Fetch robusto con retry y backoff
Implementar 3 reintentos
Backoff exponencial
No romper ejecución si una sala falla
Logging adecuado de errores HTTP

🔵 FASE 4 – Profesionalización
⬜ 11. Añadir métricas básicas
Tiempo total de ejecución
Tiempo por venue
Número total de conciertos procesados

⬜ 12. Dockerizar scraper independiente
Servicio separado del backend
Programable por cron
Preparado para despliegue en servidor

⬜ 13. Preparar migraciones con Alembic
Versionado de esquema
Evolución controlada de la base de datos

🧠 Recomendación de Orden
Orden sugerido de implementación:
1️⃣ Cache de venues
2️⃣ CLI con argparse
3️⃣ Logging
4️⃣ DTO
5️⃣ Tests
6️⃣ Reestructuración de paquete

🎯 Objetivo Final

Tener un scraper:
Modular
Escalable
Seguro ante duplicados
Preparado para múltiples ciudades
Fácil de mantener cuando las webs cambien