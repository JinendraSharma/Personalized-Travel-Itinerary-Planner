"""Supabase client setup and database access helpers."""

from typing import Optional
from supabase import Client
from app.db.database import get_service_client


def get_supabase_client() -> Optional[Client]:
    """Return the backend-only database client (service role), never the anon client."""
    return get_service_client()


def get_supabase_service_client() -> Optional[Client]:
    """Return an administrative Supabase service role client."""
    return get_service_client()
