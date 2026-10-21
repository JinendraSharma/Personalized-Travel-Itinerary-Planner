"""Trip and itinerary routes."""

import logging
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends

from app.utils.auth import get_current_user_id
from app.services.history import get_history_service
from app.schemas import (
    CreateTripRequest,
    TripResponse,
    ItineraryResponse,
    DayItinerary,
    TripPlanRequest,
    TripResponseSchema,
    RegenerateDayRequest,
    ItineraryDaySchema,
)
from app.services.trip import get_trip_service, get_itinerary_service
from app.services.ai import get_ai_orchestrator
from app.prompts import (
    SYSTEM_PROMPT,
    build_itinerary_prompt,
)
from app.utils.errors import NotFoundError, ValidationError, AIGenerationError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/plan", response_model=TripResponse, summary="Generate personalized trip itinerary")
async def plan_trip(
    request: CreateTripRequest,
    user_id: str = Depends(get_current_user_id),
    ai_orchestrator=Depends(get_ai_orchestrator),
    history_service=Depends(get_history_service),
) -> TripResponse:
    """Generate intelligent destination recommendations and day-by-day itinerary."""
    if not request.destination:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Destination cannot be empty.",
        )

    try:
        logger.info(f"Generating itinerary for destination: {request.destination} (User: {user_id})")
        itinerary_result = await ai_orchestrator.generate_itinerary(request)

        # Log action to history service
        history_service.log_action(
            user_id=user_id,
            action="GENERATE_ITINERARY",
            details={
                "destination": request.destination,
                "days": itinerary_result.days,
                "travel_style": request.travel_style,
            },
        )
        return itinerary_result
    except Exception as e:
        logger.error(f"Error in plan_trip: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate itinerary: {str(e)}",
        )


@router.post("/regenerate-day", response_model=ItineraryDaySchema, summary="Refine or regenerate a specific day's activities")
async def regenerate_day(
    request: RegenerateDayRequest,
    user_id: str = Depends(get_current_user_id),
    ai_orchestrator=Depends(get_ai_orchestrator),
    history_service=Depends(get_history_service),
) -> ItineraryDaySchema:
    """Refine a single day's plan adapting to user feedback or travel vibe shifts."""
    try:
        updated_day = ai_orchestrator.regenerate_day(
            destination=request.destination,
            day_number=request.day_number,
            travel_style=request.travel_style or "cultural",
            interests=request.interests,
            feedback=request.feedback,
            budget_per_day=request.budget_per_day or 5000.0,
        )

        history_service.log_action(
            user_id=user_id,
            action="REGENERATE_DAY",
            details={
                "destination": request.destination,
                "day_number": request.day_number,
                "feedback": request.feedback,
            },
        )
        return updated_day
    except Exception as e:
        logger.error(f"Error in regenerate_day: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to regenerate day: {str(e)}",
        )


@router.post("/create", response_model=TripResponse, status_code=status.HTTP_201_CREATED, summary="Save trip to database")
async def create_trip(
    request: CreateTripRequest,
    user_id: str = Depends(get_current_user_id),
    trip_service=Depends(get_trip_service),
    itinerary_service=Depends(get_itinerary_service),
    ai_orchestrator=Depends(get_ai_orchestrator),
    history_service=Depends(get_history_service),
) -> TripResponse:
    """Generate and permanently save a trip and its itinerary into Supabase."""
    try:
        generated = await ai_orchestrator.generate_itinerary(request)

        # Save trip record
        saved_trip = trip_service.create_trip(
            user_id=user_id,
            trip_data={
                "destination": generated.destination,
                "start_date": generated.start_date,
                "end_date": generated.end_date,
                "travel_style": generated.travel_style,
                "budget_per_day": generated.budget_per_day,
                "currency": generated.currency,
                "pace": generated.pace,
                "num_travelers": generated.num_travelers,
                "interests": generated.interests,
                "dietary_needs": generated.dietary_needs,
            },
        )

        trip_id = saved_trip["id"]

        # Save itinerary days
        days_payload = [day.model_dump() for day in generated.itinerary]
        itinerary_service.save_itinerary(trip_id=trip_id, days_data=days_payload)

        # Log to history
        history_service.log_action(
            user_id=user_id,
            action="CREATE_TRIP",
            trip_id=trip_id,
            details={"destination": generated.destination},
        )

        generated.id = trip_id
        return generated
    except Exception as e:
        logger.error(f"Error creating trip: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save trip: {str(e)}",
        )


@router.get("", response_model=List[dict], summary="List all trips")
def get_trips(
    user_id: str = Depends(get_current_user_id),
    trip_service=Depends(get_trip_service),
) -> List[dict]:
    """Retrieve all trips for the authenticated user."""
    return trip_service.get_trips(user_id=user_id)


@router.get("/{trip_id}", summary="Get trip by ID with itinerary")
def get_trip(
    trip_id: str,
    trip_service=Depends(get_trip_service),
    itinerary_service=Depends(get_itinerary_service),
):
    """Retrieve trip details including its full itinerary."""
    try:
        trip = trip_service.get_trip_by_id(trip_id)
        itinerary_days = itinerary_service.get_itinerary_by_trip(trip_id)
        trip["itinerary"] = itinerary_days
        return trip
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a trip")
def delete_trip(
    trip_id: str,
    user_id: str = Depends(get_current_user_id),
    trip_service=Depends(get_trip_service),
    history_service=Depends(get_history_service),
):
    """Delete a trip from the database."""
    success = trip_service.delete_trip(trip_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")
    history_service.log_action(user_id=user_id, action="DELETE_TRIP", trip_id=trip_id)
    return None
