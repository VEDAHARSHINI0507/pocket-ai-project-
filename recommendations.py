from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.models import Recommendation
from app.services.gemini_utils import generate_recommendations


router = APIRouter()


def save_recommendation(
    db: Session,
    user_id: int,
    planner_type: str,
    budget: str,
    input_data: dict,
    result: str
):

    recommendation = Recommendation(
        user_id=user_id,
        planner_type=planner_type,
        budget=budget,
        input_data=json.dumps(input_data),
        result_data=result
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


@router.post("/generate-home")
async def generate_home(
    request: Request,
    budget: str = Form(...),
    room: str = Form(...),
    style: str = Form(...),
    colors: str = Form(...),
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    prompt = f"""
You are PocketSmart AI, a home decor recommendation assistant.

Create useful home decor recommendations based on:

Budget: {budget}
Room: {room}
Style: {style}
Preferred colors: {colors}

Give practical suggestions for furniture, decoration,
lighting, colors and accessories.

Keep the recommendations within the given budget.
Present the answer clearly with headings and bullet points.
"""

    result = generate_recommendations(prompt)

    save_recommendation(
        db=db,
        user_id=user_id,
        planner_type="home",
        budget=budget,
        input_data={
            "room": room,
            "style": style,
            "colors": colors
        },
        result=result
    )

    return RedirectResponse(
        url="/recommendations",
        status_code=303
    )


@router.post("/generate-party")
async def generate_party(
    request: Request,
    budget: str = Form(...),
    occasion: str = Form(...),
    guests: str = Form(...),
    theme: str = Form(...),
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    prompt = f"""
You are PocketSmart AI, a party planning assistant.

Create a party plan based on:

Budget: {budget}
Occasion: {occasion}
Number of guests: {guests}
Theme: {theme}

Suggest decorations, food, activities, invitations
and other useful arrangements.

Keep the plan practical and within the given budget.
Present the answer clearly with headings and bullet points.
"""

    result = generate_recommendations(prompt)

    save_recommendation(
        db=db,
        user_id=user_id,
        planner_type="party",
        budget=budget,
        input_data={
            "occasion": occasion,
            "guests": guests,
            "theme": theme
        },
        result=result
    )

    return RedirectResponse(
        url="/recommendations",
        status_code=303
    )


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: str = Form(...),
    occasion: str = Form(...),
    outfit: str = Form(...),
    metal: str = Form(...),
    db: Session = Depends(get_db)
):

    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    prompt = f"""
You are PocketSmart AI, a jewelry recommendation assistant.

Recommend jewelry based on:

Budget: {budget}
Occasion: {occasion}
Outfit description: {outfit}
Preferred metal: {metal}

Suggest suitable jewelry such as earrings, necklaces,
bracelets and rings.

Keep the recommendations within the given budget.
Explain why each recommendation matches the outfit
and occasion.

Present the answer clearly with headings and bullet points.
"""

    result = generate_recommendations(prompt)

    save_recommendation(
        db=db,
        user_id=user_id,
        planner_type="jewelry",
        budget=budget,
        input_data={
            "occasion": occasion,
            "outfit": outfit,
            "metal": metal
        },
        result=result
    )

    return RedirectResponse(
        url="/recommendations",
        status_code=303
    )