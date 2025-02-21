from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.profile.role == 'Member'

# Decorators for role-based access
admin_required = user_passes_test(is_admin, login_url='/login/')
librarian_required = user_passes_test(is_librarian, login_url='/login/')
member_required = user_passes_test(is_member, login_url='/login/')