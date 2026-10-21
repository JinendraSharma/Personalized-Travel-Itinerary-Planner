"""Trip and itinerary persistence backed by Supabase."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.supabase_service import get_supabase_client
from app.utils.errors import NotFoundError

logger = logging.getLogger(__name__)


class TripService:
    """Persist trips, with an in-memory fallback for local development."""

    def __init__(self):
        self._trips_store: Dict[str, Dict[str, Any]] = {}

    def create_trip(self, user_id: str, trip_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        record = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "destination": trip_data.get("destination", "Unknown"),
            "start_date": trip_data.get("start_date"),
            "end_date": trip_data.get("end_date"),
            "preferences": {
                key: trip_data.get(key)
                for key in (
                    "travel_style", "interests", "budget_per_day", "currency",
                    "pace", "num_travelers", "dietary_needs",
                )
            },
            "created_at": now,
            "updated_at": now,
        }
        client = get_supabase_client()
        if client:
            try:
                result = client.table("trips").insert(record).execute()
                if result.data:
                    return result.data[0]
                raise RuntimeError("Supabase did not return the inserted trip")
            except Exception:
                logger.exception("Could not save trip to Supabase")
                raise
        self._trips_store[record["id"]] = record
        return record

    def get_trips(self, user_id: str) -> List[Dict[str, Any]]:
        client = get_supabase_client()
        if client:
            try:
                result = client.table("trips").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
                return result.data or []
            except Exception:
                logger.exception("Could not retrieve trips from Supabase")
                raise
        return sorted(
            (trip for trip in self._trips_store.values() if trip.get("user_id") == user_id),
            key=lambda trip: trip.get("created_at", ""), reverse=True,
        )

    def get_trip_by_id(self, trip_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        client = get_supabase_client()
        if client:
            try:
                query = client.table("trips").select("*").eq("id", trip_id)
                if user_id:
                    query = query.eq("user_id", user_id)
                result = query.limit(1).execute()
                if result.data:
                    return result.data[0]
            except Exception:
                logger.exception("Could not retrieve trip from Supabase")
                raise
        trip = self._trips_store.get(trip_id)
        if trip and (user_id is None or trip.get("user_id") == user_id):
            return trip
        raise NotFoundError(f"Trip with ID {trip_id} not found.")

    def update_trip(self, trip_id: str, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        trip = self.get_trip_by_id(trip_id, user_id)
        preferences = dict(trip.get("preferences") or {})
        for key in ("travel_style", "interests", "budget_per_day", "currency", "pace", "num_travelers", "dietary_needs"):
            if key in updates:
                preferences[key] = updates[key]
        changes = {key: updates[key] for key in ("destination", "start_date", "end_date") if key in updates}
        changes["preferences"] = preferences
        changes["updated_at"] = datetime.now(timezone.utc).isoformat()

        client = get_supabase_client()
        if client:
            try:
                result = client.table("trips").update(changes).eq("id", trip_id).eq("user_id", user_id).execute()
                if result.data:
                    return result.data[0]
                raise NotFoundError(f"Trip with ID {trip_id} not found.")
            except NotFoundError:
                raise
            except Exception:
                logger.exception("Could not update trip in Supabase")
                raise
        trip.update(changes)
        self._trips_store[trip_id] = trip
        return trip

    def delete_trip(self, trip_id: str, user_id: str) -> bool:
        try:
            self.get_trip_by_id(trip_id, user_id)
        except NotFoundError:
            return False
        client = get_supabase_client()
        if client:
            try:
                client.table("trips").delete().eq("id", trip_id).eq("user_id", user_id).execute()
                return True
            except Exception:
                logger.exception("Could not delete trip from Supabase")
                raise
        self._trips_store.pop(trip_id, None)
        return True


class ItineraryService:
    """Persist the day-by-day itinerary for each trip."""

    def __init__(self):
        self._itinerary_store: Dict[str, List[Dict[str, Any]]] = {}

    def save_itinerary(self, trip_id: str, days_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        records = [
            {
                "id": str(uuid.uuid4()),
                "trip_id": trip_id,
                "day_number": day.get("day", index),
                "title": day.get("title", f"Day {index}"),
                "activities": day.get("activities", []),
                "notes": day.get("summary", ""),
                "created_at": now,
                "updated_at": now,
            }
            for index, day in enumerate(days_data, start=1)
        ]
        client = get_supabase_client()
        if client:
            try:
                client.table("itineraries").delete().eq("trip_id", trip_id).execute()
                if records:
                    result = client.table("itineraries").insert(records).execute()
                    records = result.data or records
            except Exception:
                logger.exception("Could not save itinerary to Supabase")
                raise
        self._itinerary_store[trip_id] = records
        return records

    def get_itinerary_by_trip(self, trip_id: str) -> List[Dict[str, Any]]:
        client = get_supabase_client()
        if client:
            try:
                result = client.table("itineraries").select("*").eq("trip_id", trip_id).order("day_number").execute()
                return result.data or []
            except Exception:
                logger.exception("Could not retrieve itinerary from Supabase")
                raise
        return self._itinerary_store.get(trip_id, [])

    def delete_itinerary(self, trip_id: str) -> None:
        """Remove the development copy; Supabase removes rows through its FK cascade."""
        self._itinerary_store.pop(trip_id, None)


_trip_service_instance = TripService()
_itinerary_service_instance = ItineraryService()


def get_trip_service() -> TripService:
    return _trip_service_instance


def get_itinerary_service() -> ItineraryService:
    return _itinerary_service_instance
