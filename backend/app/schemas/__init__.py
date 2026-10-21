"""Schemas package initialization."""

from .schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    TripCreateRequest,
    TripPlanRequest,
    ItineraryActivitySchema,
    ItineraryDaySchema,
    TripResponseSchema,
    PreferenceRequest,
    PreferenceResponse,
    CreateTripRequest,
    TripResponse,
    ItineraryResponse,
    DayItinerary,
)

__all__ = [
    "UserRegisterRequest",
    "UserLoginRequest",
    "TokenResponse",
    "UserResponse",
    "TripCreateRequest",
    "TripPlanRequest",
    "ItineraryActivitySchema",
    "ItineraryDaySchema",
    "TripResponseSchema",
    "PreferenceRequest",
    "PreferenceResponse",
    "CreateTripRequest",
    "TripResponse",
    "ItineraryResponse",
    "DayItinerary",
]
