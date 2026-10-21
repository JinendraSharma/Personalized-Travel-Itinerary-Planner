"""History logging service for tracking trip operations."""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.supabase_service import get_supabase_client

logger = logging.getLogger(__name__)


class HistoryService:
    def __init__(self):
        self._in_memory_history: List[Dict[str, Any]] = []

    def log_action(
        self,
        user_id: str,
        action: str,
        trip_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Record an action to Supabase history table with in-memory fallback."""
        entry = {
            "user_id": user_id,
            "action": action,
            "trip_id": trip_id,
            "details": details or {},
            "created_at": datetime.utcnow().isoformat(),
        }

        client = get_supabase_client()
        if client:
            try:
                res = client.table("history").insert(entry).execute()
                if res.data:
                    return res.data[0]
            except Exception as e:
                logger.warning(f"Failed to write history to Supabase: {e}")

        # Fallback to local memory log
        self._in_memory_history.append(entry)
        return entry

    def get_user_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch history records for a specific user."""
        client = get_supabase_client()
        if client:
            try:
                res = client.table("history").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
                return res.data or []
            except Exception as e:
                logger.warning(f"Failed to fetch history from Supabase: {e}")

        return [h for h in self._in_memory_history if h.get("user_id") == user_id]


_history_service_instance = HistoryService()


def get_history_service() -> HistoryService:
    """Return singleton instance of HistoryService."""
    return _history_service_instance
