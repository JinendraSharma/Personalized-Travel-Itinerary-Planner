"""Authentication utilities for user resolution and token handling."""

import os
from typing import Optional
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DEMO_USER_ID = "00000000-0000-0000-0000-000000000001"


def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """Extract and return the current user UUID from the Authorization header.
    
    If no token is supplied or in development mode, defaults to a mock user UUID.
    """
    if not authorization:
        return DEFAULT_DEMO_USER_ID

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return DEFAULT_DEMO_USER_ID

    # If simple format or development token
    try:
        # In full production, this verifies the JWT secret
        # For now, if the token contains a user_id payload or plain id:
        return token if len(token) > 20 and "-" in token else DEFAULT_DEMO_USER_ID
    except Exception:
        return DEFAULT_DEMO_USER_ID
