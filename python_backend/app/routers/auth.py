from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.database import get_db
from app.db_models import User
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from app.services.oauth_service import verify_google_token, verify_microsoft_token, get_github_access_token, get_github_user_info
from fastapi.responses import RedirectResponse
import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class OAuthLogin(BaseModel):
    token: str

class OAuthLoginGeneric(BaseModel):
    email: EmailStr
    provider: str # github, google, microsoft
    provider_id: Optional[str] = None

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(username=user_data.username, hashed_password=hashed_password, auth_provider="local")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate token
    access_token = create_access_token(data={"sub": db_user.username, "id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": db_user.id, "username": db_user.username}}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if not db_user or not db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    if not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        
    access_token = create_access_token(data={"sub": db_user.username, "id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": db_user.id, "username": db_user.username, "provider": db_user.auth_provider}}

@router.post("/google", response_model=Token)
def google_login(oauth_data: OAuthLogin, db: Session = Depends(get_db)):
    try:
        user_info = verify_google_token(oauth_data.token)
        email = user_info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Google token missing email")
            
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            db_user = User(email=email, auth_provider="google")
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
        access_token = create_access_token(data={"sub": db_user.email, "id": db_user.id})
        return {"access_token": access_token, "token_type": "bearer", "user": {"id": db_user.id, "email": db_user.email, "provider": db_user.auth_provider}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/microsoft", response_model=Token)
def microsoft_login(oauth_data: OAuthLogin, db: Session = Depends(get_db)):
    try:
        user_info = verify_microsoft_token(oauth_data.token)
        # MSAL tokens typically have 'preferred_username' as the email
        email = user_info.get("preferred_username") or user_info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Microsoft token missing email")
            
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            db_user = User(email=email, auth_provider="microsoft")
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
        access_token = create_access_token(data={"sub": db_user.email, "id": db_user.id})
        return {"access_token": access_token, "token_type": "bearer", "user": {"id": db_user.id, "email": db_user.email, "provider": db_user.auth_provider}}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/github/login")
def github_login():
    from app.services.oauth_service import GITHUB_CLIENT_ID
    # Redirect to GitHub
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=user:email"
    return RedirectResponse(url=github_auth_url)

@router.get("/github/callback")
async def github_callback(code: str, db: Session = Depends(get_db)):
    try:
        access_token = await get_github_access_token(code)
        user_info = await get_github_user_info(access_token)
        
        email = user_info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="GitHub missing email")
            
        db_user = db.query(User).filter(User.email == email).first()
        if not db_user:
            db_user = User(email=email, username=user_info.get("login"), auth_provider="github")
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
        jwt_token = create_access_token(data={"sub": db_user.email, "id": db_user.id})
        return RedirectResponse(url=f"{FRONTEND_URL}/oauth-success?token={jwt_token}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/oauth", response_model=Token)
def oauth_login_generic(oauth_data: OAuthLoginGeneric, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == oauth_data.email).first()
    if not db_user:
        # Auto-register OAuth user
        db_user = User(email=oauth_data.email, auth_provider=oauth_data.provider, provider_id=oauth_data.provider_id)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
    access_token = create_access_token(data={"sub": db_user.email, "id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": db_user.id, "email": db_user.email, "provider": db_user.auth_provider}}

class ForgotPassword(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()
    if not db_user:
        # For security, do not reveal whether email exists
        return {"message": "If your email is registered, you will receive a password reset link."}
    
    # In a real app, send an email here with a reset token
    # For now, just return a success message
    return {"message": "If your email is registered, you will receive a password reset link."}
