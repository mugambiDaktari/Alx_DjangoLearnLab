from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# Register your models here.
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

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Book, BookAdmin)


