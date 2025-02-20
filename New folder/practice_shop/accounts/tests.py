from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "password1", "password2")

class UserModelTest(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(email="testuser@example.com", full_name="Test User", password="testpass")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.full_name, "Test User")
        self.assertTrue(user.check_password("testpass"))

class ViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="testuser@example.com", full_name="Test User", password="testpass")
        self.client.login(email="testuser@example.com", password="testpass")

    def test_home_page(self):
        response = self.client.get(reverse("shop:home_page"))  # Проверить правильное имя маршрута в urls.py
        self.assertEqual(response.status_code, 200)

class FormsTest(TestCase):
    def test_valid_form(self):
        form = CustomUserCreationForm({"email": "testuser@example.com", "password1": "testpass123", "password2": "testpass123"})
        self.assertTrue(form.is_valid())

class AuthenticationTest(TestCase):
    def test_login(self):
        user = get_user_model().objects.create_user(email="testuser@example.com", full_name="Test User", password="testpass")
        login = self.client.login(email="testuser@example.com", password="testpass")
        self.assertTrue(login)

    def test_logout(self):
        self.client.login(email="testuser@example.com", password="testpass")
        response = self.client.get(reverse("accounts:user_logout"))  # Проверить правильное имя маршрута в urls.py
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после выхода
