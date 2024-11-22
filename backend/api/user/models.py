from __future__ import annotations

import uuid
from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now


class UserManager(BaseUserManager):
    """Manager for the custom User model."""

    def create_user(
            self,
            email: str | None = None,
            whatsapp_number: str | None = None,
            password: str | None = None,
            **extra_fields: Any,
    ) -> Any:
        """Create a user.

        Args:
            email (Optional[str]): Email of the user. Defaults to None.
            whatsapp_number (Optional[str]): Whatsapp number of the user. Defaults to None.
            password (Optional[str]): Password of the user. Defaults to None.
            extra_fields (dict): Additional fields for user creation.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If neither email nor whatsapp_number is provided.
        """
        if not email and not whatsapp_number:
            msg = "Either an email or a Whatsapp number is required."
            raise ValueError(msg)

        if email:
            email = self.normalize_email(email)
            extra_fields.setdefault("is_verified", False)

        user = self.model(
            email=email,
            whatsapp_number=whatsapp_number,
            **extra_fields,
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(
            self: UserManager,
            email: str | None =None,
            whatsapp_number: str | None =None,
            password: str | None = None,
            **extra_fields: Any,
    ) -> Any:
        """To create superuser.

        Args:
        ----
            email (str | None, optional): Email of the user. Defaults to None.
            whatsapp_number (str | None, optional): Whatsapp number of the user. Defaults to None.
            password (str | None, optional): Password of the user. Defaults to None.
            extra_fields (dict): Additional fields for user creation.

        Returns:
        -------
            User: User object

        Raises:
        ------
            ValueError: If email or whatsapp number is not provided
        """
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(
            email=email,
            whatsapp_number=whatsapp_number,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    """To create model for the `users` table.

    Attributes
    ----------
        user_id (UUIDField): Unique identifier for the user.
        email (EmailField): Email address of the user.
        whatsapp_number (CharField): Whatsapp number of the user.
        password_hash (CharField): Hashed password of the user.
        is_verified (BooleanField): Whether the user has been verified or not.
        is_admin (BooleanField): Whether the user is an admin or not.
        created_at (DateTimeField): Timestamp of when the user was created.
        modified_at (DateTimeField): Timestamp of when the user was last modified.

    """

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    password_hash = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now, editable=False)
    modified_at = models.DateTimeField(default=now)

    objects = UserManager()

    # Required attributes for custom user model
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> Any:
        """To return the string representation of the user.

        Returns either the `email` or the `whatsapp_number`,
        whichever is available.

        Returns:
            str: The string representation of the user.
        """
        return self.email if self.email else self.whatsapp_number

    class Meta:  # noqa: DJ012
        db_table = "users"
        ordering = ["created_at"]  # noqa: RUF012
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Overrides save method to update `modified_at` automatically."""  # noqa: D401
        self.modified_at = now()
        super().save(*args, **kwargs)

    def set_password(
        self,
        raw_password: str,
        ) -> None:
        """Hashes the password and assigns it to the password_hash field."""
        self.password_hash = make_password(raw_password)
