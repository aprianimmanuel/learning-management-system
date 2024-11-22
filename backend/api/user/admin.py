from __future__ import annotations

from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from api.user.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "whatsapp_number", "is_verified", "is_admin")
    list_filter = ("is_verified", "is_admin")
    search_fields = ("email", "whatsapp_number")
    ordering = ("created_at",)
    fieldsets = (
        (None, {"fields": ("email", "whatsapp_number", "password_hash")}),
        ("Permissions", {"fields": ("is_verified", "is_admin")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "whatsapp_number", "password_hash", "is_verified", "is_admin"),
        }),
    )
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
