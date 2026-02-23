import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app import crud
from app.database import SessionLocal


def _pre_hash_for_bcrypt(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str):
    pre_hashed = _pre_hash_for_bcrypt(plain_password)
    return bcrypt.checkpw(pre_hashed.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str):
    pre_hashed = _pre_hash_for_bcrypt(password)
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pre_hashed.encode("utf-8"), salt).decode("utf-8")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Der hier würde natürlich sonst woanders liegen. Zur einfachheit, hardcodiert.
SECRET_KEY = "my_super_secret_static_key_for_minidrive_which_should_be_in_env_file"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: SessionLocal = Depends(get_db),  # type: ignore
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user
