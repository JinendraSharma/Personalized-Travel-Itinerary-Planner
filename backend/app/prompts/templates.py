"""Prompt templates and structuring logic for travel itinerary generation."""

from typing import List, Optional, Union

SYSTEM_PROMPT = """You are an expert AI Travel Concierge and Route Optimization Specialist.
Your mission is to generate sensible, realistic, and geographically optimized day-by-day itineraries.

Guidelines:
- Group nearby attractions within the same morning, afternoon, or evening cluster to minimize transit time and avoid backtracking.
- Respect the requested travel style, daily budget, dietary restrictions, and pacing.
- Practical with accurate timing and costs.

You provide day-by-day itineraries with specific recommendations."""


def build_itinerary_prompt(
    destination: str,
    start_date: str,
    end_date: str,
    travel_style: str,
    interests: list[str],
    group_size: int,
    pace: str,
    budget_per_day: float,
    currency: str = "INR",
    dietary_restrictions: Optional[Union[List[str], str]] = None,
    mobility_concerns: str = None,
) -> str:
    """Build the user prompt for itinerary generation."""

    if isinstance(dietary_restrictions, list):
        dietary_value = ", ".join(dietary_restrictions)
    elif isinstance(dietary_restrictions, str):
        dietary_value = dietary_restrictions.strip()
    else:
        dietary_value = ""
    dietary_info = f"Dietary restrictions: {dietary_value}" if dietary_value else ""
    mobility_info = f"Mobility considerations: {mobility_concerns}" if mobility_concerns else ""

    interests_str = ", ".join(interests) if interests else "Top sights and local highlights"
    pace_description = {
        "relaxed": "one or two main activities per day with plenty of rest",
        "moderate": "two to three main activities per day with some downtime",
        "fast": "three to four main activities per day, constantly exploring",
        "fast-paced": "three to four main activities per day, constantly exploring",
    }.get(pace.lower(), "two to three main activities per day with some downtime")

    prompt = f"""Create a detailed {destination} itinerary from {start_date} to {end_date}.

Trip Profile:
- Destination: {destination}
- Dates: {start_date} to {end_date}
- Travel Style: {travel_style}
- Group Size: {group_size} traveler(s)
- Pacing: {pace} ({pace_description})
- Daily Budget per Person: {budget_per_day:,.2f} {currency}
- Interests: {interests_str}
{f"- {dietary_info}" if dietary_info else ""}
{f"- {mobility_info}" if mobility_info else ""}

Route & Time Optimization Constraints:
1. Sequence activities geographically so morning, afternoon, and evening stops are clustered to minimize travel distance and prevent backtracking.
2. Specify realistic time slots and transit suggestions between stops (e.g. walk, metro, taxi with estimated transit duration).
3. Ensure lunch and dinner spots are located close to the preceding activity.
4. Output strictly a JSON object with this structure:
{{
  "destination": "{destination}",
  "start_date": "{start_date}",
  "end_date": "{end_date}",
  "days": <total_days>,
  "travel_style": "{travel_style}",
  "currency": "{currency}",
  "budget_per_day": {budget_per_day},
  "itinerary": [
    {{
      "day": 1,
      "date": "{start_date}",
      "title": "<Day Theme & Neighborhood>",
      "summary": "<Short summary of the day's route>",
      "activities": [
        {{
          "time_slot": "Morning (09:00 - 12:30)",
          "title": "<Activity Title>",
          "description": "<Description with local tips>",
          "location": "<Exact Neighborhood/Address>",
          "category": "Attraction | Dining | Transit",
          "estimated_cost": <number>,
          "transit_time": "<e.g. 15 mins via Metro from hotel>",
          "transit_mode": "Walk | Metro | Taxi"
        }}
      ]
    }}
  ]
}}
"""
    return prompt.strip()
