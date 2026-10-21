"""Schemas used by the trip-planning API."""

from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    destination: str = Field(min_length=1, max_length=120)
    days: int = Field(default=3, ge=1, le=30)
    interests: list[str] = Field(default_factory=list)


class ItineraryDay(BaseModel):
    day: int
    title: str
    activities: list[str]


class TripResponse(BaseModel):
    destination: str
    days: int
    interests: list[str]
    itinerary: list[ItineraryDay]
