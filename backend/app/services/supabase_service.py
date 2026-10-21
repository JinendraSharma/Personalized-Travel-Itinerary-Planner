"""Supabase client setup.

Keep credentials in environment variables; never commit real keys.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


@lru_cache(maxsize=1)
def get_supabase_client() -> Client | None:
    """Return a Supabase client when credentials are configured, otherwise None."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key or key == "your_supabase_anon_key":
        return None
    return create_client(url, key)
