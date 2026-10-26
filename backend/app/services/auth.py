"""User registration and login persistence."""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

from app.services.supabase_service import get_supabase_client
from app.utils.auth import hash_password, verify_password

logger = logging.getLogger(__name__)
_users: Dict[str, Dict[str, Any]] = {}


class AuthenticationError(Exception):
    pass


class EmailAlreadyRegistered(Exception):
    pass


def register_user(email: str, name: str, password: str) -> Dict[str, Any]:
    normalized_email = email.strip().lower()
    client = get_supabase_client()
    if client:
        try:
            existing = client.table("users").select("id").eq("email", normalized_email).limit(1).execute()
            if existing.data:
                raise EmailAlreadyRegistered
            record = {
                "id": str(uuid.uuid4()),
                "email": normalized_email,
                "name": name.strip(),
                "password_hash": hash_password(password),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            result = client.table("users").insert(record).execute()
            if result.data:
                return result.data[0]
            raise RuntimeError("The user could not be saved")
        except EmailAlreadyRegistered:
            raise
        except Exception:
            logger.exception("User registration failed")
            raise

    if any(user["email"] == normalized_email for user in _users.values()):
        raise EmailAlreadyRegistered
    user = {
        "id": str(uuid.uuid4()),
        "email": normalized_email,
        "name": name.strip(),
        "password_hash": hash_password(password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _users[user["id"]] = user
    return user


def authenticate_user(email: str, password: str) -> Dict[str, Any]:
    normalized_email = email.strip().lower()
    client = get_supabase_client()
    if client:
        try:
            result = client.table("users").select("*").eq("email", normalized_email).limit(1).execute()
            user = result.data[0] if result.data else None
        except Exception:
            logger.exception("User login lookup failed")
            raise
    else:
        user = next((item for item in _users.values() if item["email"] == normalized_email), None)

    if not user or not verify_password(password, user.get("password_hash", "")):
        raise AuthenticationError
    return user


def get_user_by_id(user_id: str) -> Dict[str, Any]:
    """Return safe profile fields for an authenticated user."""
    client = get_supabase_client()
    if client:
        result = client.table("users").select("id,email,name,created_at").eq("id", user_id).limit(1).execute()
        user = result.data[0] if result.data else None
    else:
        user = _users.get(user_id)
    if not user:
        raise AuthenticationError
    return {key: user.get(key) for key in ("id", "email", "name", "created_at")}
