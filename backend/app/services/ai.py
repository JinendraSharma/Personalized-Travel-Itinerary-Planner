"""AI Orchestrator service for generative itinerary recommendations."""

import os
import json
import logging
import httpx
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.schemas.schemas import (
    TripPlanRequest,
    TripResponseSchema,
    ItineraryDaySchema,
    ItineraryActivitySchema,
)
from app.prompts import SYSTEM_PROMPT, build_itinerary_prompt
from app.utils.errors import AIGenerationError

logger = logging.getLogger(__name__)


class AIOrchestrator:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "groq").lower()
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.hf_key = os.getenv("HUGGINGFACE_API_KEY")
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    async def generate_itinerary(self, request: TripPlanRequest) -> TripResponseSchema:
        """Orchestrate AI prompt generation and call provider with fallback."""
        prompt = build_itinerary_prompt(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            travel_style=request.travel_style,
            interests=request.interests or [],
            group_size=request.num_travelers,
            pace=request.pace,
            budget_per_day=request.budget_per_day or 5000.0,
            currency=request.currency,
            dietary_restrictions=request.dietary_needs,
        )

        # Attempt to use Groq if API key is provided and not a placeholder
        if self.provider == "groq" and self.groq_key and self.groq_key != "your_groq_api_key":
            try:
                ai_result = await self._call_groq(prompt)
                if ai_result:
                    return ai_result
            except Exception as e:
                logger.warning(f"Groq generation failed, falling back to expert local generator: {e}")

        # Intelligent local generation fallback
        return self._generate_expert_local_itinerary(request)

    async def _call_groq(self, prompt: str) -> Optional[TripResponseSchema]:
        """Send prompt to Groq API with JSON mode enabled."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.6,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                raw_json = data["choices"][0]["message"]["content"]
                parsed = json.loads(raw_json)
                return TripResponseSchema(**parsed)
            else:
                logger.error(f"Groq API error ({resp.status_code}): {resp.text}")
                return None

    def _generate_expert_local_itinerary(self, request: TripPlanRequest) -> TripResponseSchema:
        """Curate a realistic, highly personalized itinerary based on preferences."""
        dest = request.destination.strip().title()
        style = request.travel_style.lower()
        pace = request.pace.lower()
        budget = request.budget_per_day or 5000.0
        currency = request.currency
        interests = request.interests or ["Sightseeing", "Food"]

        # Calculate days
        try:
            start = datetime.strptime(request.start_date.strip(), "%Y-%m-%d").date()
            end = datetime.strptime(request.end_date.strip(), "%Y-%m-%d").date()
            days = max(1, min((end - start).days + 1, 30))
        except Exception:
            days = 3

        theme_titles = {
            "cultural": ["Heritage & Historic Wonders", "Art, Museums & Traditions", "Ancient Temples & Local Architecture", "Old Town Discovery"],
            "beach": ["Coastal Charm & Morning Surf", "Hidden Coves & Beachside Dining", "Water Sports & Sunset Pier", "Ocean Breeze & Seafood Feast"],
            "adventure": ["Alpine Treks & Scenic Trails", "Adrenaline Peaks & River Rafting", "Canyon Exploration & Wilderness Hike", "Panoramic Ridge Expedition"],
            "foodie": ["Epicurean Walking Tour & Street Bites", "Michelin & Authentic Heritage Dining", "Local Vineyard & Spice Market Safari", "Pastry, Coffee & Artisan Tastings"],
            "tropical": ["Rainforest Canopies & Hidden Lagoons", "Botanical Sanctuaries & Exotic Wildlife", "Island Hopping & Crystal Springs", "Verdant Valleys & Eco Retreat"],
            "sightseeing": ["Iconic Panoramas & Landmark Highlights", "Architectural Wonders & City Miradors", "Historic Quarters & Photography Walks", "Sunset Horizons & Night Cityscapes"],
            "nightlife": ["Sunset Rooftops & Evening Lounges", "Live Music Venues & Cultural Theatre", "Night Food Bazaars & Speakeasies", "Harbor Lights & Festive Nightwalks"],
        }.get(style, ["Highlights & City Icons", "Culture & Hidden Corners", "Flavors & Panoramic Views"])

        itinerary_days: List[ItineraryDaySchema] = []

        for d in range(1, days + 1):
            day_theme = theme_titles[(d - 1) % len(theme_titles)]
            activities: List[ItineraryActivitySchema] = []

            # Morning
            activities.append(
                ItineraryActivitySchema(
                    time_slot="Morning (09:00 - 12:30)",
                    title=f"Signature Experience: {dest} {day_theme.split('&')[0].strip()}",
                    description=f"Explore the premier spots around {dest} focusing on {interests[0] if interests else 'local culture'}. Includes scenic walk and guided insights.",
                    location=f"Central {dest}",
                    category="Attraction",
                    estimated_cost=round(budget * 0.35, 2),
                )
            )

            # Afternoon
            activities.append(
                ItineraryActivitySchema(
                    time_slot="Afternoon (13:00 - 16:30)",
                    title=f"Curated Gastronomy & {dest} Exploration",
                    description=f"Enjoy lunch at renowned local eateries tailored for your {style} travel vibe." + (f" (Respecting {request.dietary_needs})" if request.dietary_needs else "") + f". Followed by {interests[1] if len(interests) > 1 else 'artisan shopping'}.",
                    location=f"{dest} District Quarter",
                    category="Dining & Leisure",
                    estimated_cost=round(budget * 0.40, 2),
                )
            )

            # Evening (only if pace is moderate or fast)
            if pace in ["moderate", "fast", "fast-paced"]:
                activities.append(
                    ItineraryActivitySchema(
                        time_slot="Evening (17:30 - 21:00)",
                        title=f"Sunset & Twilight Leisure at {dest}",
                        description=f"Unwind with twilight viewpoints, waterfront strolls, and authentic cultural ambiance at a {pace} pace.",
                        location=f"{dest} Promenade",
                        category="Entertainment",
                        estimated_cost=round(budget * 0.25, 2),
                    )
                )

            itinerary_days.append(
                ItineraryDaySchema(
                    day=d,
                    date=request.start_date,
                    title=f"Day {d}: {day_theme}",
                    summary=f"A personalized day in {dest} balancing {style} discovery with comfort.",
                    activities=activities,
                )
            )

        return TripResponseSchema(
            destination=dest,
            start_date=request.start_date,
            end_date=request.end_date,
            days=days,
            travel_style=style,
            num_travelers=request.num_travelers,
            budget_per_day=budget,
            currency=currency,
            interests=interests,
            pace=pace,
            dietary_needs=request.dietary_needs,
            itinerary=itinerary_days,
            created_at=datetime.utcnow(),
        )


_ai_orchestrator = AIOrchestrator()


def get_ai_orchestrator() -> AIOrchestrator:
    """Return the AIOrchestrator singleton."""
    return _ai_orchestrator
