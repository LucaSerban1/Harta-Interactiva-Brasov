from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import locations, reviews, auth
from app.models import location, reviews as reviews_model, user
from fastapi.security import HTTPBearer

app = FastAPI(
    title="Harta Interactiva Brasov API",
    description="API pentru harta interactivă a Brașovului",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locations.router, prefix="/locations", tags=["Locații"])
app.include_router(reviews.router, prefix="/reviews", tags=["Recenzii"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {"status": "ok", "message": "Harta Interactiva Brasov API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}