"""Trip and Itinerary persistence service with Supabase integration."""

import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.services.supabase_service import get_supabase_client
from app.utils.errors import NotFoundError

logger = logging.getLogger(__name__)


class TripService:
    def __init__(self):
        self._trips_store: Dict[str, Dict[str, Any]] = {}

    def create_trip(self, user_id: str, trip_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a new trip to the Supabase trips table or local store."""
        trip_id = str(uuid.uuid4())
        record = {
            "id": trip_id,
            "user_id": user_id,
            "destination": trip_data.get("destination", "Unknown"),
            "start_date": trip_data.get("start_date", datetime.utcnow().strftime("%Y-%m-%d")),
            "end_date": trip_data.get("end_date", datetime.utcnow().strftime("%Y-%m-%d")),
            "preferences": {
                "travel_style": trip_data.get("travel_style", "cultural"),
                "interests": trip_data.get("interests", []),
                "budget_per_day": trip_data.get("budget_per_day", 5000.0),
                "currency": trip_data.get("currency", "INR"),
                "pace": trip_data.get("pace", "moderate"),
                "num_travelers": trip_data.get("num_travelers", 1),
                "dietary_needs": trip_data.get("dietary_needs"),
            },
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        client = get_supabase_client()
        if client:
            try:
                res = client.table("trips").insert(record).execute()
                if res.data:
                    return res.data[0]
            except Exception as e:
                logger.warning(f"Supabase trip insert fallback: {e}")

        self._trips_store[trip_id] = record
        return record

    def get_trips(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all trips for a user or all saved trips."""
        client = get_supabase_client()
        if client:
            try:
                query = client.table("trips").select("*").order("created_at", desc=True)
                if user_id:
                    query = query.eq("user_id", user_id)
                res = query.execute()
                return res.data or []
            except Exception as e:
                logger.warning(f"Supabase trip fetch fallback: {e}")

        if user_id:
            return [t for t in self._trips_store.values() if t.get("user_id") == user_id]
        return list(self._trips_store.values())

    def get_trip_by_id(self, trip_id: str) -> Dict[str, Any]:
        """Fetch a specific trip record by id."""
        client = get_supabase_client()
        if client:
            try:
                res = client.table("trips").select("*").eq("id", trip_id).execute()
                if res.data:
                    return res.data[0]
            except Exception as e:
                logger.warning(f"Supabase trip fetch by id fallback: {e}")

        trip = self._trips_store.get(trip_id)
        if not trip:
            raise NotFoundError(f"Trip with ID {trip_id} not found.")
        return trip

    def delete_trip(self, trip_id: str) -> bool:
        """Delete a trip by its ID."""
        client = get_supabase_client()
        if client:
            try:
                client.table("trips").delete().eq("id", trip_id).execute()
                return True
            except Exception as e:
                logger.warning(f"Supabase trip delete fallback: {e}")

        if trip_id in self._trips_store:
            del self._trips_store[trip_id]
            return True
        return False


class ItineraryService:
    def __init__(self):
        self._itinerary_store: Dict[str, List[Dict[str, Any]]] = {}

    def save_itinerary(self, trip_id: str, days_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Save day-by-day itineraries associated with a trip."""
        saved_days: List[Dict[str, Any]] = []

        client = get_supabase_client()
        for idx, day_info in enumerate(days_data, start=1):
            day_id = str(uuid.uuid4())
            record = {
                "id": day_id,
                "trip_id": trip_id,
                "day_number": day_info.get("day", idx),
                "title": day_info.get("title", f"Day {idx}"),
                "activities": day_info.get("activities", []),
                "notes": day_info.get("summary", ""),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            if client:
                try:
                    res = client.table("itineraries").insert(record).execute()
                    if res.data:
                        saved_days.append(res.data[0])
                        continue
                except Exception as e:
                    logger.warning(f"Supabase itinerary insert fallback: {e}")

            saved_days.append(record)

        self._itinerary_store[trip_id] = saved_days
        return saved_days

    def get_itinerary_by_trip(self, trip_id: str) -> List[Dict[str, Any]]:
        """Retrieve itinerary days for a specific trip."""
        client = get_supabase_client()
        if client:
            try:
                res = client.table("itineraries").select("*").eq("trip_id", trip_id).order("day_number").execute()
                if res.data:
                    return res.data
            except Exception as e:
                logger.warning(f"Supabase itinerary fetch fallback: {e}")

        return self._itinerary_store.get(trip_id, [])


_trip_service_instance = TripService()
_itinerary_service_instance = ItineraryService()


def get_trip_service() -> TripService:
    """Return TripService singleton."""
    return _trip_service_instance


def get_itinerary_service() -> ItineraryService:
    """Return ItineraryService singleton."""
    return _itinerary_service_instance
