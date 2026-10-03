import bcrypt
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User

router = APIRouter()


def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


@router.post("/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            return RedirectResponse(
                url="/register?error=Email+already+registered",
                status_code=303
            )

        hashed_pwd = hash_password(password)

        # Note: If your User model in app/models/models.py uses 'hashed_password' 
        # or 'password_hash' instead of 'password', update the key name below accordingly.
        user = User(
            name=name,
            email=email,
            password=hashed_pwd
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        request.session["user_id"] = user.id
        request.session["user_name"] = user.name

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    except Exception as e:
        db.rollback()
        print("\n" + "="*50)
        print("EXACT REGISTRATION ERROR:")
        print(e)
        print("="*50 + "\n")
        raise e


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            return RedirectResponse(
                url="/login?error=Invalid+email+or+password",
                status_code=303
            )

        # Check password attribute dynamically or fallback to password
        stored_hash = getattr(user, "password", getattr(user, "hashed_password", None))

        if not stored_hash or not verify_password(password, stored_hash):
            return RedirectResponse(
                url="/login?error=Invalid+email+or+password",
                status_code=303
            )

        request.session["user_id"] = user.id
        request.session["user_name"] = user.name

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )
    except Exception as e:
        print("\n" + "="*50)
        print("EXACT LOGIN ERROR:")
        print(e)
        print("="*50 + "\n")
        raise e


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        url="/",
        status_code=303
    )