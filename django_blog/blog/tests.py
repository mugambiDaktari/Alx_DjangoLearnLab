from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Profile  # Import your Profile model

class UserAuthTests(TestCase):
    def setUp(self):
        """Set up test client and create a user"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123**')
        self.profile = Profile.objects.create(user=self.user, about='Hello, I am a test user!')

    def test_user_registration(self):
        """Test if a new user can register successfully"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_login_invalid_credentials(self):
        """Test login with incorrect credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Page reloads with error message
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):
        """Test user logout"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertNotIn('_auth_user_id', self.client.session)  # User should be logged out

    def test_profile_view_requires_login(self):
        """Test that the profile page is only accessible to logged-in users"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Should allow access

    def test_profile_edit(self):
        """Test that a user can update their profile"""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('profile'), {
            'username': 'testuser_updated',
            'email': 'updated@example.com',
            'bio': 'Updated bio'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after profile update
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.profile.bio, 'Updated bio')

    def test_only_authenticated_user_can_edit_profile(self):
        """Ensure an unauthenticated user cannot edit a profile"""
        response = self.client.post(reverse('profile'), {
            'username': 'hacker',
            'email': 'hacker@example.com',
            'bio': 'I am a hacker'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, 'hacker@example.com')


