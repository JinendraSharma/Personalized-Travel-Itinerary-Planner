"""Database connection and initialization."""

import logging
from typing import Optional
from supabase import create_client, Client
from app.config import get_settings

logger = logging.getLogger(__name__)


class Database:
    """Supabase database client wrapper."""

    def __init__(self):
        """Initialize Supabase client."""
        settings = get_settings()
        self.client: Optional[Client] = None
        self.service_client: Optional[Client] = None

        url = settings.supabase_url
        key = settings.supabase_key
        # Never silently elevate the public client: admin access must be configured
        # with the dedicated service-role secret.
        service_key = settings.supabase_service_role_key

        if url and key and not key.startswith("your_") and url.startswith("http"):
            try:
                self.client = create_client(url, key)
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize Supabase public client: {e}")

        if url and service_key and not service_key.startswith("your_") and url.startswith("http"):
            try:
                self.service_client = create_client(url, service_key)
                logger.info("Supabase service-role client initialized successfully")
            except Exception as e:
                logger.warning(f"Could not initialize Supabase service-role client: {e}")

    def get_client(self) -> Optional[Client]:
        """Get Supabase client."""
        return self.client

    def get_service_client(self) -> Optional[Client]:
        """Get service role client for admin operations."""
        return self.service_client


_database_instance: Optional[Database] = None


def get_database() -> Database:
    """Return singleton Database instance."""
    global _database_instance
    if _database_instance is None:
        _database_instance = Database()
    return _database_instance


def get_client() -> Optional[Client]:
    """Dependency helper to get active Supabase client."""
    return get_database().get_client()


def get_service_client() -> Optional[Client]:
    """Dependency helper to get active Supabase service-role client."""
    return get_database().get_service_client()
