"""Trip-planning API endpoints."""

from fastapi import APIRouter
from app.models.trip import TripRequest, TripResponse

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("/plan", response_model=TripResponse)
def plan_trip(request: TripRequest) -> TripResponse:
    """Return a starter itinerary response; replace with generation logic later."""
    days = max(1, request.days)
    return TripResponse(
        destination=request.destination,
        days=days,
        interests=request.interests,
        itinerary=[
            {"day": day, "title": f"Explore {request.destination}", "activities": ["Add a local attraction", "Try local food"]}
            for day in range(1, days + 1)
        ],
    )
