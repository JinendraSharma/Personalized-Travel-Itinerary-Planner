"""Pydantic schemas for request/response validation."""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ============ Authentication Schemas ============

class UserRegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: str = Field(..., min_length=2, description="Name must be at least 2 characters")


class UserLoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None


class UserResponse(BaseModel):
    """User response."""
    id: str
    email: str
    name: str
    created_at: Optional[datetime] = None


# ============ Trip & Itinerary Schemas ============

class ItineraryActivitySchema(BaseModel):
    """Detailed activity within a single day's itinerary."""
    time_slot: str = Field(..., description="e.g. Morning, Afternoon, Evening")
    title: str
    description: str
    location: Optional[str] = None
    category: Optional[str] = Field(default="Attraction", description="Attraction, Dining, Transit, Leisure")
    estimated_cost: Optional[float] = Field(default=0.0, description="Estimated cost in currency")
    transit_time: Optional[str] = Field(default=None, description="e.g. 15 mins via Metro")
    transit_mode: Optional[str] = Field(default=None, description="Walk, Metro, Taxi")
    neighborhood: Optional[str] = Field(default=None, description="District or cluster area")


class ItineraryDaySchema(BaseModel):
    """Single day itinerary containing activities."""
    day: int
    date: Optional[str] = None
    title: str
    summary: Optional[str] = None
    activities: List[ItineraryActivitySchema] = Field(default_factory=list)


class TripPlanRequest(BaseModel):
    """Trip creation & itinerary generation request from user preferences."""
    destination: str = Field(..., min_length=1, max_length=120)
    start_date: str
    end_date: str
    travel_style: str = Field(default="cultural", description="cultural, adventure, relaxation, foodie, budget, luxury")
    num_travelers: int = Field(default=1, ge=1, le=50)
    budget_per_day: Optional[float] = Field(default=5000.0, ge=0)
    currency: str = Field(default="INR")
    interests: List[str] = Field(default_factory=list)
    dietary_needs: Optional[str] = Field(default=None)
    pace: str = Field(default="moderate", description="relaxed, moderate, fast-paced")
    itinerary: Optional[List[ItineraryDaySchema]] = None


class TripCreateRequest(TripPlanRequest):
    """Alias for trip creation request."""
    user_id: Optional[str] = None


class SavedTripUpdateRequest(BaseModel):
    """Editable fields for a saved trip and its itinerary."""
    destination: Optional[str] = Field(default=None, min_length=1, max_length=120)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    travel_style: Optional[str] = None
    num_travelers: Optional[int] = Field(default=None, ge=1, le=50)
    budget_per_day: Optional[float] = Field(default=None, ge=0)
    currency: Optional[str] = None
    interests: Optional[List[str]] = None
    dietary_needs: Optional[str] = None
    pace: Optional[str] = None
    itinerary: Optional[List[ItineraryDaySchema]] = None


class TripResponseSchema(BaseModel):
    """Standardized response schema for trips."""
    id: Optional[str] = None
    destination: str
    start_date: str
    end_date: str
    days: int
    travel_style: str
    num_travelers: int = 1
    budget_per_day: Optional[float] = None
    currency: str = "INR"
    interests: List[str] = Field(default_factory=list)
    pace: Optional[str] = "moderate"
    dietary_needs: Optional[str] = None
    itinerary: List[ItineraryDaySchema] = Field(default_factory=list)
    created_at: Optional[datetime] = None


# ============ User Preferences Schemas ============

class PreferenceRequest(BaseModel):
    """User default preferences."""
    travel_style: Optional[str] = "cultural"
    interests: List[str] = Field(default_factory=list)
    budget_per_day: Optional[float] = 5000.0
    currency: str = "INR"
    pace: Optional[str] = "moderate"
    dietary_requirements: Optional[str] = None


class PreferenceResponse(PreferenceRequest):
    id: Optional[str] = None
    user_id: str
    updated_at: Optional[datetime] = None


# Aliases for route convention compatibility
CreateTripRequest = TripPlanRequest
TripResponse = TripResponseSchema
ItineraryResponse = TripResponseSchema
DayItinerary = ItineraryDaySchema


class RegenerateDayRequest(BaseModel):
    """Request schema for refining or regenerating a specific day."""
    destination: str
    day_number: int
    original_title: Optional[str] = "Day Highlights"
    travel_style: Optional[str] = "cultural"
    interests: List[str] = Field(default_factory=list)
    feedback: Optional[str] = Field(default=None, description="e.g. make it more relaxed, more budget-friendly, more outdoor")
    budget_per_day: Optional[float] = 5000.0
    currency: Optional[str] = "INR"
    dietary_needs: Optional[str] = None
