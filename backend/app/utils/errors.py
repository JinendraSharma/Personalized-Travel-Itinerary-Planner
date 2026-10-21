"""Custom exceptions for the application."""

class NotFoundError(Exception):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, message: str = "Validation failed"):
        self.message = message
        super().__init__(self.message)


class AIGenerationError(Exception):
    """Raised when the AI model fails to generate valid itinerary content."""
    def __init__(self, message: str = "Failed to generate itinerary with AI"):
        self.message = message
        super().__init__(self.message)
