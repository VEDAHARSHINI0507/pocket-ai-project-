from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import GEMINI_API_KEY
from app.database import get_db
from app.models.models import Recommendation

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get("/dashboard")
async def dashboard_page(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # Check whether a valid GEMINI_API_KEY is detected in config
    api_key_configured = bool(GEMINI_API_KEY and GEMINI_API_KEY.strip())

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "api_key_configured": api_key_configured
        }
    )


@router.get("/home")
async def home_planner_page(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


@router.get("/party")
async def party_planner_page(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context={}
    )


@router.get("/jewelry")
async def jewelry_planner_page(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context={}
    )


@router.get("/recommendations")
async def recommendations_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    latest = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.created_at.desc())
        .first()
    )

    recommendation = latest.result_data if latest else None

    return templates.TemplateResponse(
        request=request,
        name="recommendations.html",
        context={
            "recommendation": recommendation
        }
    )


@router.get("/history")
async def history_page(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "recommendations": recommendations
        }
    )


@router.get("/testimonials")
async def testimonials_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="testimonials.html",
        context={}
    )