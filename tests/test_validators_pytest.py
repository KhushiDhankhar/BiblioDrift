"""
Pytest test suite for BiblioDrift API validators.
Tests edge cases not covered by existing manual test scripts.
These are proper pytest tests (unlike test_validation.py 
which has __test__ = False).
"""

import sys
import os
import pytest

# Add backend folder to path so we can import validators
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from validators import (
    validate_request,
    AnalyzeMoodRequest,
    MoodTagsRequest,
    MoodSearchRequest,
    GenerateNoteRequest,
    ChatRequest,
    RegisterRequest,
    LoginRequest,
    AddToLibraryRequest,
    UpdateLibraryItemRequest,
    ChatMessage
)


# ==================== HELPER ====================

def is_valid(result):
    """Check if validation passed."""
    return result[0]

def get_error(result):
    """Get error dict from validation result."""
    return result[1]


# ==================== MOOD SEARCH TESTS ====================

class TestMoodSearchRequest:
    """Tests for MoodSearchRequest validator."""

    def test_valid_mood_query_passes(self):
        """A normal mood query should pass validation."""
        result = validate_request(
            MoodSearchRequest,
            {"query": "cozy rainy evening mystery"}
        )
        assert is_valid(result) is True

    def test_empty_query_fails(self):
        """An empty query string should fail validation."""
        result = validate_request(
            MoodSearchRequest,
            {"query": ""}
        )
        assert is_valid(result) is False

    def test_whitespace_only_query_fails(self):
        """A whitespace-only query should fail validation."""
        result = validate_request(
            MoodSearchRequest,
            {"query": "     "}
        )
        assert is_valid(result) is False

    def test_missing_query_field_fails(self):
        """Missing query field entirely should fail validation."""
        result = validate_request(
            MoodSearchRequest,
            {}
        )
        assert is_valid(result) is False

    def test_query_too_long_fails(self):
        """Query exceeding 500 characters should fail validation."""
        result = validate_request(
            MoodSearchRequest,
            {"query": "x" * 501}
        )
        assert is_valid(result) is False

    def test_none_body_fails(self):
        """Sending None as body should fail validation."""
        result = validate_request(
            MoodSearchRequest,
            None
        )
        assert is_valid(result) is False

    def test_none_body_returns_correct_error_format(self):
        """None body should return correct error structure."""
        result = validate_request(
            MoodSearchRequest,
            None
        )
        error = get_error(result)
        assert "success" in error
        assert error["success"] is False
        assert "error" in error


# ==================== ANALYZE MOOD TESTS ====================

class TestAnalyzeMoodRequest:
    """Tests for AnalyzeMoodRequest validator."""

    def test_valid_title_and_author_passes(self):
        """Valid title and author should pass."""
        result = validate_request(
            AnalyzeMoodRequest,
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald"
            }
        )
        assert is_valid(result) is True

    def test_empty_title_fails(self):
        """Empty title should fail validation."""
        result = validate_request(
            AnalyzeMoodRequest,
            {"title": "", "author": "Some Author"}
        )
        assert is_valid(result) is False

    def test_missing_title_fails(self):
        """Missing title field should fail validation."""
        result = validate_request(
            AnalyzeMoodRequest,
            {"author": "Some Author"}
        )
        assert is_valid(result) is False

    def test_author_is_optional(self):
        """Author field should be optional."""
        result = validate_request(
            AnalyzeMoodRequest,
            {"title": "The Great Gatsby"}
        )
        assert is_valid(result) is True

    def test_title_too_long_fails(self):
        """Title exceeding 255 characters should fail."""
        result = validate_request(
            AnalyzeMoodRequest,
            {"title": "x" * 256, "author": "Author"}
        )
        assert is_valid(result) is False

    def test_none_body_fails(self):
        """None body should fail validation."""
        result = validate_request(AnalyzeMoodRequest, None)
        assert is_valid(result) is False


# ==================== MOOD TAGS TESTS ====================

class TestMoodTagsRequest:
    """Tests for MoodTagsRequest validator."""

    def test_valid_request_passes(self):
        """Valid title and author should pass."""
        result = validate_request(
            MoodTagsRequest,
            {
                "title": "1984",
                "author": "George Orwell"
            }
        )
        assert is_valid(result) is True

    def test_empty_title_fails(self):
        """Empty title should fail validation."""
        result = validate_request(
            MoodTagsRequest,
            {"title": "", "author": "George Orwell"}
        )
        assert is_valid(result) is False

    def test_missing_title_fails(self):
        """Missing title entirely should fail."""
        result = validate_request(
            MoodTagsRequest,
            {"author": "George Orwell"}
        )
        assert is_valid(result) is False

    def test_author_optional(self):
        """Author should be optional for mood tags."""
        result = validate_request(
            MoodTagsRequest,
            {"title": "1984"}
        )
        assert is_valid(result) is True


# ==================== CHAT REQUEST TESTS ====================

class TestChatRequest:
    """Tests for ChatRequest validator."""

    def test_valid_message_passes(self):
        """Valid message with history should pass."""
        result = validate_request(
            ChatRequest,
            {
                "message": "I want something cozy for a rainy evening",
                "history": []
            }
        )
        assert is_valid(result) is True

    def test_empty_message_fails(self):
        """Empty message should fail validation."""
        result = validate_request(
            ChatRequest,
            {"message": "", "history": []}
        )
        assert is_valid(result) is False

    def test_whitespace_message_fails(self):
        """Whitespace-only message should fail validation."""
        result = validate_request(
            ChatRequest,
            {"message": "     ", "history": []}
        )
        assert is_valid(result) is False

    def test_missing_message_fails(self):
        """Missing message field should fail."""
        result = validate_request(
            ChatRequest,
            {"history": []}
        )
        assert is_valid(result) is False

    def test_message_too_long_fails(self):
        """Message exceeding 2000 characters should fail."""
        result = validate_request(
            ChatRequest,
            {"message": "x" * 2001, "history": []}
        )
        assert is_valid(result) is False

    def test_history_is_optional(self):
        """History field should be optional."""
        result = validate_request(
            ChatRequest,
            {"message": "Recommend something mysterious"}
        )
        assert is_valid(result) is True


# ==================== REGISTER REQUEST TESTS ====================

class TestRegisterRequest:
    """Tests for RegisterRequest validator."""

    def test_valid_registration_passes(self):
        """Valid username, email, password should pass."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "Password123!"
            }
        )
        assert is_valid(result) is True

    def test_username_too_short_fails(self):
        """Username shorter than 3 characters should fail."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "ab",
                "email": "test@example.com",
                "password": "Password123!"
            }
        )
        assert is_valid(result) is False

    def test_invalid_email_fails(self):
        """Invalid email format should fail."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "testuser",
                "email": "not-an-email",
                "password": "Password123!"
            }
        )
        assert is_valid(result) is False

    def test_password_too_short_fails(self):
        """Password shorter than 8 characters should fail."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "123"
            }
        )
        assert is_valid(result) is False

    def test_missing_email_fails(self):
        """Missing email field should fail."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "testuser",
                "password": "Password123!"
            }
        )
        assert is_valid(result) is False

    def test_missing_password_fails(self):
        """Missing password field should fail."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "testuser",
                "email": "test@example.com"
            }
        )
        assert is_valid(result) is False

    def test_username_with_special_chars_fails(self):
        """Username with special characters should fail."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "test@user!",
                "email": "test@example.com",
                "password": "Password123!"
            }
        )
        assert is_valid(result) is False


# ==================== LOGIN REQUEST TESTS ====================

class TestLoginRequest:
    """Tests for LoginRequest validator."""

    def test_valid_login_passes(self):
        """Valid username and password should pass."""
        result = validate_request(
            LoginRequest,
            {
                "username": "testuser",
                "password": "password123"
            }
        )
        assert is_valid(result) is True

    def test_empty_username_fails(self):
        """Empty username should fail."""
        result = validate_request(
            LoginRequest,
            {"username": "", "password": "password123"}
        )
        assert is_valid(result) is False

    def test_empty_password_fails(self):
        """Empty password should fail."""
        result = validate_request(
            LoginRequest,
            {"username": "testuser", "password": ""}
        )
        assert is_valid(result) is False

    def test_missing_username_fails(self):
        """Missing username field should fail."""
        result = validate_request(
            LoginRequest,
            {"password": "password123"}
        )
        assert is_valid(result) is False

    def test_missing_password_fails(self):
        """Missing password field should fail."""
        result = validate_request(
            LoginRequest,
            {"username": "testuser"}
        )
        assert is_valid(result) is False

    def test_none_body_fails(self):
        """None body should fail validation."""
        result = validate_request(LoginRequest, None)
        assert is_valid(result) is False


# ==================== ERROR RESPONSE FORMAT TESTS ====================

class TestErrorResponseFormat:
    """Tests to ensure error responses follow correct format."""

    def test_none_body_returns_success_false(self):
        """None body error should have success=False."""
        result = validate_request(MoodSearchRequest, None)
        error = get_error(result)
        assert error["success"] is False

    def test_none_body_returns_error_key(self):
        """None body error should have error key."""
        result = validate_request(MoodSearchRequest, None)
        error = get_error(result)
        assert "error" in error

    def test_validation_error_has_validation_errors_key(self):
        """Validation errors should include validation_errors list."""
        result = validate_request(
            MoodSearchRequest,
            {"query": ""}
        )
        error = get_error(result)
        assert "validation_errors" in error

    def test_validation_error_list_is_not_empty(self):
        """Validation errors list should not be empty on failure."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "ab",
                "email": "bad-email",
                "password": "123"
            }
        )
        error = get_error(result)
        assert len(error.get("validation_errors", [])) > 0

    def test_validation_error_has_field_key(self):
        """Each validation error should have a field key."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "ab",
                "email": "bad-email",
                "password": "123"
            }
        )
        error = get_error(result)
        errors = error.get("validation_errors", [])
        for e in errors:
            assert "field" in e

    def test_validation_error_has_message_key(self):
        """Each validation error should have a message key."""
        result = validate_request(
            RegisterRequest,
            {
                "username": "ab",
                "email": "bad-email",
                "password": "123"
            }
        )
        error = get_error(result)
        errors = error.get("validation_errors", [])
        for e in errors:
            assert "message" in e
