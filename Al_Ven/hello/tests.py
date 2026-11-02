from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Review


class AuthenticationTests(TestCase):
    def test_registration_hashes_password_and_logs_user_in(self):
        response = self.client.post(reverse("reg"), {
            "name": "Test User",
            "email": "TEST@example.com",
            "password": "A-strong-test-password-481!",
            "password_confirm": "A-strong-test-password-481!",
        })

        user = get_user_model().objects.get(email="test@example.com")
        self.assertNotEqual(user.password, "A-strong-test-password-481!")
        self.assertTrue(user.check_password("A-strong-test-password-481!"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
        self.assertRedirects(response, reverse("index"))

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(reverse("reg"), {
            "name": "Test User",
            "email": "test@example.com",
            "password": "A-strong-test-password-481!",
            "password_confirm": "different-password",
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(email="test@example.com").exists())

    def test_login_accepts_email_and_logout_ends_session(self):
        user = get_user_model().objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="A-strong-test-password-481!",
        )
        response = self.client.post(reverse("vhod"), {
            "username": "test@example.com",
            "password": "A-strong-test-password-481!",
        })
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

        response = self.client.post(reverse("vyhod"))
        self.assertRedirects(response, reverse("index"))
        self.assertNotIn("_auth_user_id", self.client.session)


class ReviewTests(TestCase):
    def test_valid_review_is_saved_and_redirects(self):
        response = self.client.post(reverse("reviews"), {
            "name": "Клиент",
            "rating": 5,
            "text": "Всё понравилось!",
        })

        self.assertRedirects(response, reverse("reviews"))
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, 5)

    def test_invalid_review_is_not_saved(self):
        response = self.client.post(reverse("reviews"), {
            "name": "Клиент",
            "rating": 8,
            "text": "Отзыв",
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Review.objects.count(), 0)
