from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        *UserAdmin.fieldsets,  # Expands existing Django user fields
        (
            "Custom Fields",  # Custom section in the admin panel
            {"fields": ("date_of_birth", "profile_photo")},
        ),
    )

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            "Custom Fields",
            {"fields": ("date_of_birth", "profile_photo")},
        ),
    )

    list_display = ("username", "email", "date_of_birth", "is_staff")
    search_fields = ("username", "email")

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)

