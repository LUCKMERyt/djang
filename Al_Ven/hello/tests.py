from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from .models import Category, Products, Review, ProductInquiry


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
        self.assertRedirects(response, reverse("account"))

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
        self.assertRedirects(response, reverse("account"))
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


class AccountPageTests(TestCase):
    def test_account_page_requires_login(self):
        response = self.client.get(reverse("account"))

        self.assertRedirects(response, f"{reverse('vhod')}?next={reverse('account')}")

    def test_logged_in_user_sees_account_details(self):
        user = get_user_model().objects.create_user(
            username="account-user",
            email="account@example.com",
            first_name="Анна",
            password="A-strong-test-password-481!",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("account"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Анна")
        self.assertContains(response, "account@example.com")
        self.assertContains(response, "Выйти из аккаунта")


class ProductCatalogLinkTests(TestCase):
    def test_catalog_links_to_product_page(self):
        category = Category.objects.create(name="Украшения", coment="Описание категории")
        product = Products.objects.create(
            name="Тестовое украшение",
            sale=2500,
            material="Серебро",
            date_prod=date(2026, 1, 15),
            conter=3,
            cat_id=category,
        )

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="/products/{product.slug}/"')

    def test_catalog_renders_product_image(self):
        category = Category.objects.create(name="Украшения", coment="Описание категории")
        product = Products.objects.create(
            name="Товар с фото",
            sale=1500,
            material="Серебро",
            date_prod=date(2026, 2, 1),
            conter=1,
            cat_id=category,
            image=SimpleUploadedFile("product.jpg", b"test image", content_type="image/jpeg"),
        )

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'src="{product.image.url}"')
        self.assertContains(response, f'href="/products/{product.slug}/"')


class ProductDetailTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Украшения", coment="Описание категории")
        self.product = Products.objects.create(
            name="Тестовый товар",
            sale=2500,
            material="Серебро",
            date_prod=date(2026, 1, 15),
            conter=3,
            cat_id=self.category,
            description="Описание товара для карточки.",
        )

    def test_product_detail_renders(self):
        response = self.client.get(reverse("product_detail", kwargs={"slug": self.product.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.cat_id.name)
        self.assertContains(response, f'rel="canonical" href="/products/{self.product.slug}/"')

    def test_product_detail_has_jsonld_and_canonical(self):
        response = self.client.get(reverse("product_detail", kwargs={"slug": self.product.slug}))

        self.assertContains(response, '"@type": "Product"')
        self.assertContains(response, "https://schema.org/InStock")
        self.assertContains(response, f'rel="canonical" href="/products/{self.product.slug}/"')

    def test_product_detail_out_of_stock(self):
        Products.objects.filter(pk=self.product.pk).update(conter=0)
        response = self.client.get(reverse("product_detail", kwargs={"slug": self.product.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://schema.org/OutOfStock")

    def test_product_detail_404(self):
        response = self.client.get("/products/no-such-slug/")
        self.assertEqual(response.status_code, 404)

    def test_slug_generated_on_create(self):
        product = Products.objects.create(
            name="Новый товар",
            sale=100,
            material="Дерево",
            date_prod=date(2026, 3, 1),
            conter=1,
            cat_id=self.category,
        )
        self.assertTrue(product.slug)
        self.assertIn("новый-товар", product.slug)


class ProductInquiryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Украшения", coment="Описание категории")
        self.product = Products.objects.create(
            name="Товар для заявки",
            sale=1000,
            material="Серебро",
            date_prod=date(2026, 1, 1),
            conter=5,
            cat_id=self.category,
        )

    def test_inquiry_form_creates_and_redirects(self):
        url = reverse("product_inquiry_form", kwargs={"slug": self.product.slug})
        response = self.client.post(url, {
            "name": "Оптовик",
            "email": "opt@example.com",
            "message": "Нужно 10 шт. оптом.",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_detail", kwargs={"slug": self.product.slug}))
        inquiry = ProductInquiry.objects.get()
        self.assertEqual(inquiry.product, self.product)
        self.assertEqual(inquiry.name, "Оптовик")
        self.assertEqual(inquiry.status, "new")

    def test_inquiry_form_invalid_shows_errors(self):
        url = reverse("product_inquiry_form", kwargs={"slug": self.product.slug})
        response = self.client.post(url, {"name": "", "email": "", "message": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductInquiry.objects.count(), 0)

    def test_inquiry_form_page_renders(self):
        response = self.client.get(reverse("product_inquiry_form", kwargs={"slug": self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Заявка на товар: ")
        self.assertContains(response, self.product.name)
