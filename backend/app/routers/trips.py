"""Trip-planning API endpoints router re-export for modular compatibility."""

from app.routes.trips import (
    router,
    plan_trip,
    create_trip,
    get_trips,
    get_trip,
    delete_trip,
)

__all__ = [
    "router",
    "plan_trip",
    "create_trip",
    "get_trips",
    "get_trip",
    "delete_trip",
]
