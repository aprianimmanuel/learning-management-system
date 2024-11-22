from __future__ import annotations

import pytest
from django.db import IntegrityError

from api.user.models import User


@pytest.mark.django_db
class TestUserModel:
    """Test the User model."""

    def test_create_user_with_email(self):
        """Test creating a user with an email."""
        user = User.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
        )
        assert user.email == "testuser@example.com"
        assert user.whatsapp_number is None
        assert user.is_verified is False
        assert user.check_password("securepassword123") is True

    def test_create_user_with_whatsapp_number(self):
        """Test creating a user with a Whatsapp number."""
        user = User.objects.create_user(
            whatsapp_number="6281234567890",
            password="securepassword123",
        )
        assert user.email is None
        assert user.whatsapp_number == "621234567890"
        assert user.is_verified is False
        assert user.check_password("securepassword123") is True

    def test_create_user_requires_email_or_whatsapp(self):
        """Test creating a user with neither email nor Whatsapp number."""
        with pytest.raises(ValueError) as exc:
            User.objects.create_user(
                email=None,
                whatsapp_number=None,
                password="securepassword123",
            )
        assert "Either an email or a Whatsapp number is required." in str(exc.value)

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = User.objects.create_superuser(
            email="testsuperuser@example.com",
            whatsapp_number="6281234567890",
            password="securepassword123",
        )
        assert superuser.email == "testsuperuser@example.com"
        assert superuser.whatsapp_number == "6281234567890"
        assert superuser.is_verified is True
        assert superuser.is_admin is True
        assert superuser.check_password("securepassword123") is True

    def test_create_user_duplicate_email(self):
        """Test creating a user with a duplicate email."""
        User.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="testuser@example.com",
                password="securepassword123",
            )

    def test_create_user_duplicate_whatsapp(self):
        """Test creating a user with a duplicate Whatsapp number raises IntegrityError."""
        User.objects.create_user(
            whatsapp_number="6281234567890",
            password="securepassword123",
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                whatsapp_number="6281234567890",
                password="different_password123"
            )

    def test_user_string_representation_with_email(self):
        """Test the string representation of a user with an email."""
        user = User.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
        )
        assert str(user) == "testuser@example.com"

    def test_user_string_representation_with_whatsapp(self):
        """Test the string representation of a user with a Whatsapp number."""
        user = User.objects.create_user(
            whatsapp_number="6281234567890",
            password="securepassword123",
        )
        assert str(user) == "6281234567890"

    def test_modified_at_updated_on_save(self):
        """Test that modified_at is updated on save."""
        user = User.objects.create_user(
            email="testuser@example.com",
            password="securepassword123",
        )
        original_modified_at = user.modified_at
        user.is_verified = True
        user.save()
        assert user.modified_at > original_modified_at