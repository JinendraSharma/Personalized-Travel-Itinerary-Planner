"""Prompt engineering service for travel itinerary generation."""

from typing import List, Optional, Union, Dict, Any


def get_system_prompt() -> str:
    """Return the system prompt defining the AI travel concierge persona and rules."""
    return (
        "You are an expert AI Travel Concierge and local tour planner with deep knowledge "
        "of global destinations, hidden gems, local cultures, transit routes, and budget management. "
        "Your task is to craft detailed, realistic, and personalized day-by-day itineraries. "
        "Always respect the user's travel pace, group size, dietary restrictions, mobility needs, and daily budget. "
        "You must return ONLY a valid, parseable JSON object matching the requested schema without conversational filler."
    )


def build_itinerary_prompt(
    destination: str,
    start_date: str,
    end_date: str,
    travel_style: str,
    interests: List[str],
    group_size: int = 1,
    pace: str = "moderate",
    budget_per_day: float = 5000.0,
    currency: str = "INR",
    dietary_restrictions: Optional[Union[List[str], str]] = None,
    mobility_concerns: Optional[str] = None,
) -> str:
    """Build the structured user prompt for generative AI itinerary generation."""
    # Format dietary restrictions
    if isinstance(dietary_restrictions, list):
        dietary_info = f"Dietary restrictions: {', '.join(dietary_restrictions)}" if dietary_restrictions else ""
    elif isinstance(dietary_restrictions, str) and dietary_restrictions.strip():
        dietary_info = f"Dietary restrictions: {dietary_restrictions.strip()}"
    else:
        dietary_info = ""

    mobility_info = f"Mobility considerations: {mobility_concerns}" if mobility_concerns else ""

    interests_str = ", ".join(interests) if interests else "Top sights, local culture, and landmark attractions"

    pace_description = {
        "relaxed": "one or two main activities per day with plenty of downtime and leisure",
        "moderate": "two to three main activities per day with balanced exploration and rest",
        "fast": "three to four main activities per day, constantly exploring and active",
        "fast-paced": "three to four main activities per day, constantly exploring and active",
    }.get(pace.lower(), "two to three main activities per day with balanced exploration and rest")

    prompt = f"""Create a detailed {destination} itinerary from {start_date} to {end_date}.

Trip Profile:
- Destination: {destination}
- Dates: {start_date} to {end_date}
- Travel Style: {travel_style} (e.g. cultural, adventure, foodie, relaxation, beach, nightlife)
- Group Size: {group_size} traveler(s)
- Pacing: {pace} ({pace_description})
- Daily Budget per Person: {budget_per_day:,.2f} {currency}
- Interests: {interests_str}
{f"- {dietary_info}" if dietary_info else ""}
{f"- {mobility_info}" if mobility_info else ""}

Instructions & Constraints:
1. Provide a day-by-day plan for each day of the trip.
2. For every day, include Morning, Afternoon, and Evening activities with realistic sequencing and geographic proximity to minimize transit time.
3. Keep meal suggestions aligned with {dietary_info if dietary_info else 'local culinary highlights'}.
4. Provide estimated costs in {currency} for activities, dining, and admission fees to keep within the daily budget of {budget_per_day:,.2f} {currency}.
5. Format the entire response strictly as a JSON object adhering to this schema:
{{
  "destination": "{destination}",
  "start_date": "{start_date}",
  "end_date": "{end_date}",
  "days": <total_number_of_days>,
  "travel_style": "{travel_style}",
  "currency": "{currency}",
  "budget_per_day": {budget_per_day},
  "itinerary": [
    {{
      "day": 1,
      "date": "{start_date}",
      "title": "<Catchy Day 1 Title>",
      "summary": "<Short summary of the day's vibe and highlights>",
      "activities": [
        {{
          "time_slot": "Morning (09:00 - 12:30)",
          "title": "<Activity Name>",
          "description": "<Engaging description with practical tips>",
          "location": "<Specific location or neighborhood>",
          "category": "Attraction | Dining | Transit | Leisure",
          "estimated_cost": <number_in_{currency}>
        }},
        {{
          "time_slot": "Afternoon (13:00 - 16:30)",
          "title": "<Activity Name>",
          "description": "<Description>",
          "location": "<Location>",
          "category": "Dining | Attraction",
          "estimated_cost": <number_in_{currency}>
        }},
        {{
          "time_slot": "Evening (17:30 - 21:00)",
          "title": "<Activity Name>",
          "description": "<Description>",
          "location": "<Location>",
          "category": "Dining | Entertainment",
          "estimated_cost": <number_in_{currency}>
        }}
      ]
    }}
  ]
}}
"""
    return prompt.strip()


def build_regeneration_prompt(
    destination: str,
    day_number: int,
    original_theme: str,
    travel_style: str,
    interests: List[str],
    user_feedback: Optional[str] = None,
) -> str:
    """Build a prompt to regenerate or modify a specific day's itinerary."""
    interests_str = ", ".join(interests) if interests else "Local highlights"
    feedback_clause = f"User specific feedback/change request: {user_feedback}" if user_feedback else "Provide fresh alternative activities"

    return f"""Regenerate Day {day_number} for a trip to {destination}.
Original theme: {original_theme}
Travel Style: {travel_style}
Interests: {interests_str}
{feedback_clause}

Return a revised Day {day_number} plan in the same JSON format with Morning, Afternoon, and Evening activities.
""".strip()
