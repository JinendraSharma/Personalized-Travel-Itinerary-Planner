"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth import (
    AuthenticationError,
    EmailAlreadyRegistered,
    authenticate_user,
    get_user_by_id,
    register_user,
)
from app.utils.auth import create_access_token, get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/me", response_model=UserResponse)
def current_user(user_id: str = Depends(get_current_user_id)) -> UserResponse:
    try:
        user = get_user_by_id(user_id)
        return UserResponse(id=user["id"], email=user["email"], name=user["name"], created_at=user.get("created_at"))
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account was not found") from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Profile is temporarily unavailable") from exc


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegisterRequest) -> TokenResponse:
    try:
        user = register_user(request.email, request.name, request.password)
        return TokenResponse(
            access_token=create_access_token(user["id"]),
            user_id=user["id"],
            email=user["email"],
            name=user["name"],
        )
    except EmailAlreadyRegistered as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="An account with this email already exists") from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Registration is temporarily unavailable") from exc


@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest) -> TokenResponse:
    try:
        user = authenticate_user(request.email, request.password)
        return TokenResponse(
            access_token=create_access_token(user["id"]),
            user_id=user["id"],
            email=user["email"],
            name=user["name"],
        )
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password") from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Login is temporarily unavailable") from exc
