"""Offline reliability checks for production config and core trip scenarios."""

import os

# Set every environment variable consumed by Settings before app imports. This
# prevents dotenv from reading local .env credentials during tests.
_TEST_ENV = {
    "SUPABASE_URL": "",
    "SUPABASE_KEY": "",
    "SUPABASE_ANON_KEY": "",
    "SUPABASE_SERVICE_ROLE_KEY": "",
    "SECRET_KEY": "test-only-signing-secret-32-characters-long",
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "AI_PROVIDER": "local",
    "GROQ_API_KEY": "",
    "HUGGINGFACE_API_KEY": "",
    "OLLAMA_BASE_URL": "http://127.0.0.1:11434",
    "OLLAMA_MODEL": "llama3",
    "DEBUG": "false",
    "ENVIRONMENT": "development",
    "BACKEND_URL": "http://localhost:8000",
    "FRONTEND_URL": "http://localhost:5173",
}
os.environ.update(_TEST_ENV)

import unittest
from uuid import uuid4
from unittest.mock import patch
from fastapi import HTTPException

from app.config import Settings, get_settings
from app.main import app
from app.schemas import TripPlanRequest
from app.services.ai import AIOrchestrator
from app.services.trip import ItineraryService, TripService
from app.utils.auth import (
    _user_id_from_token,
    create_access_token,
    get_current_user_id,
    hash_password,
    verify_password,
)
from app.utils.errors import NotFoundError


class ConfigurationTests(unittest.TestCase):
    def test_production_rejects_development_signing_secret(self):
        config = Settings(
            environment="production",
            debug=False,
            secret_key="development-only-insecure-secret-key-change-me",
            supabase_url="https://database.example",
            supabase_service_role_key="server-key-placeholder",
            frontend_url="https://travel.example",
            groq_api_key="groq-placeholder",
            ai_provider="groq",
        )
        with self.assertRaisesRegex(ValueError, "SECRET_KEY"):
            config.validate_for_runtime()

    def test_production_accepts_complete_configuration(self):
        config = Settings(
            environment="production",
            debug=False,
            secret_key="a-random-production-secret-long-enough-123456",
            supabase_url="https://database.example",
            supabase_service_role_key="server-key-placeholder",
            frontend_url="https://travel.example,https://www.travel.example",
            groq_api_key="groq-placeholder",
            ai_provider="groq",
        )
        config.validate_for_runtime()
        self.assertEqual(config.allowed_origins, ["https://travel.example", "https://www.travel.example"])

    def test_application_registers_auth_trip_and_health_routes(self):
        paths = set(app.openapi()["paths"])
        self.assertIn("/auth/register", paths)
        self.assertIn("/auth/login", paths)
        self.assertIn("/trips", paths)
        self.assertIn("/health", paths)


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        get_settings.cache_clear()

    def test_signed_token_round_trip_and_tamper_rejection(self):
        user_id = str(uuid4())
        token = create_access_token(user_id)
        self.assertEqual(_user_id_from_token(token), user_id)
        header, payload, _signature = token.split(".")
        with self.assertRaises(Exception):
            _user_id_from_token(f"{header}.{payload}.invalid")

    def test_password_hash_is_salted_and_verifiable(self):
        first = hash_password("travel-password-123")
        second = hash_password("travel-password-123")
        self.assertNotEqual(first, second)
        self.assertTrue(verify_password("travel-password-123", first))
        self.assertFalse(verify_password("wrong-password", first))

    def test_production_requires_a_valid_bearer_token(self):
        user_id = str(uuid4())
        with patch.dict(os.environ, {"ENVIRONMENT": "production"}):
            get_settings.cache_clear()
            with self.assertRaises(HTTPException):
                get_current_user_id(None)
            with self.assertRaises(HTTPException):
                get_current_user_id("Bearer not-a-token")
            self.assertEqual(get_current_user_id(f"Bearer {create_access_token(user_id)}"), user_id)
        get_settings.cache_clear()


class TripScenarioTests(unittest.TestCase):
    def test_family_food_trip_generates_requested_days_and_group_size(self):
        planner = AIOrchestrator()
        request = TripPlanRequest(
            destination="Lisbon",
            start_date="2027-05-01",
            end_date="2027-05-03",
            travel_style="foodie",
            num_travelers=4,
            budget_per_day=180,
            currency="EUR",
            interests=["Local Cuisine", "Architecture"],
            pace="moderate",
        )
        result = planner._generate_expert_fallback(request)
        self.assertEqual(result.destination, "Lisbon")
        self.assertEqual(result.days, 3)
        self.assertEqual(result.num_travelers, 4)
        self.assertTrue(all(day.activities for day in result.itinerary))

    def test_saved_trip_crud_is_user_scoped_without_database_credentials(self):
        trips = TripService()
        itineraries = ItineraryService()
        owner = str(uuid4())
        record = trips.create_trip(owner, {"destination": "Osaka"})
        saved_days = itineraries.save_itinerary(record["id"], [{"day": 1, "title": "Markets", "activities": ["Explore"]}])
        self.assertEqual(len(saved_days), 1)
        self.assertEqual(trips.get_trips(owner)[0]["destination"], "Osaka")
        with self.assertRaises(NotFoundError):
            trips.get_trip_by_id(record["id"], str(uuid4()))
        trips.update_trip(record["id"], owner, {"destination": "Osaka, Japan"})
        self.assertEqual(trips.get_trip_by_id(record["id"], owner)["destination"], "Osaka, Japan")
        self.assertTrue(trips.delete_trip(record["id"], owner))
        itineraries.delete_itinerary(record["id"])
        self.assertEqual(itineraries.get_itinerary_by_trip(record["id"]), [])


if __name__ == "__main__":
    unittest.main()
