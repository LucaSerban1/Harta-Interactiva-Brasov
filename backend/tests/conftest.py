import pytest
from datetime import datetime, timedelta
import os
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

@pytest.fixture(scope="session")
def auth_headers():
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    user = db.query(User).filter(User.email == "test@s.unibuc.ro").first()
    db.close()

    payload = {
        "sub": str(user.id),
        "email": user.email,
        "is_admin": user.is_admin,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}
