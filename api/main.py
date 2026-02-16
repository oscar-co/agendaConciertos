from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.concerts import router as concerts_router
from api.routers.venues import router as venues_router

app = FastAPI(title="AgendaConcerts API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(venues_router)
app.include_router(concerts_router)
