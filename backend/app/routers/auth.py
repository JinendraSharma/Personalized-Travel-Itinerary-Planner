"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.schemas import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth import (
    AuthenticationError,
    EmailAlreadyRegistered,
    authenticate_user,
    register_user,
)
from app.utils.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegisterRequest) -> UserResponse:
    try:
        user = register_user(request.email, request.name, request.password)
        return UserResponse(id=user["id"], email=user["email"], name=user["name"], created_at=user.get("created_at"))
    except EmailAlreadyRegistered as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists") from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Registration is temporarily unavailable") from exc


@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest) -> TokenResponse:
    try:
        user = authenticate_user(request.email, request.password)
        return TokenResponse(access_token=create_access_token(user["id"]), user_id=user["id"])
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Login is temporarily unavailable") from exc
