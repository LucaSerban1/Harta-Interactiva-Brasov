from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import locations, reviews

app = FastAPI(
    title="Harta Interactiva Brasov API",
    description="API pentru harta interactivă a Brașovului",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locations.router, prefix="/locations", tags=["Locații"])
app.include_router(reviews.router, prefix="/reviews", tags=["Recenzii"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "Harta Interactiva Brasov API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}