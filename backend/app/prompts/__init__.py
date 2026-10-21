"""Prompts package for AI travel itinerary generation."""

from app.services.prompt_service import (
    get_system_prompt,
    build_itinerary_prompt,
    build_regeneration_prompt,
)

SYSTEM_PROMPT = get_system_prompt()

__all__ = [
    "SYSTEM_PROMPT",
    "get_system_prompt",
    "build_itinerary_prompt",
    "build_regeneration_prompt",
]
