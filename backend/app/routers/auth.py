from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.httpx_client import AsyncOAuth2Client
from jose import jwt
from datetime import datetime, timedelta
import os
from app.database import get_db
from app.models.user import User
from app.dependencies import get_current_user

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALLOWED_DOMAINS = os.getenv("ALLOWED_DOMAINS", "s.unibuc.ro,unibuc.ro").split(",")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def create_jwt_token(user_id: int, email: str, is_admin: bool) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@router.get("/login")
async def login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
    }
    url = GOOGLE_AUTH_URL + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    return RedirectResponse(url)

@router.get("/callback")
async def callback(code: str, db: Session = Depends(get_db)):
    async with AsyncOAuth2Client(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET
    ) as client:
        token = await client.fetch_token(
            GOOGLE_TOKEN_URL,
            code=code,
            redirect_uri=GOOGLE_REDIRECT_URI
        )
        userinfo = await client.get(GOOGLE_USERINFO_URL)
        userinfo = userinfo.json()

    email = userinfo.get("email", "")
    domain = email.split("@")[-1]

    is_admin = domain == "unibuc.ro"

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            username=userinfo.get("name", email.split("@")[0]),
            hashed_password="oauth_no_password",
            is_active=True,
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_jwt_token(user.id, user.email, user.is_admin)

    frontend_url = f"{FRONTEND_URL}/auth/callback?token={token}"
    return RedirectResponse(frontend_url)

@router.get("/me")
async def get_me(current_user: User = Security(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "is_admin": current_user.is_admin
    }