from datetime import date
from importlib import import_module
from types import SimpleNamespace
from urllib.parse import parse_qs

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import Category, Person, Products, Review, ProductInquiry


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

    def test_legacy_employee_photo_path_is_updated(self):
        person = Person.objects.create(
            name="Анна",
            fam="Тестовая",
            age=28,
            image="people/2-portrait.jpg",
        )
        migration = import_module("hello.migrations.0012_update_person_images")

        migration.update_person_image_paths(
            apps, SimpleNamespace(connection=connection)
        )

        person.refresh_from_db()
        self.assertEqual(person.image.name, "people/2-sulki.jpg")

    def test_account_login_field_shows_email_and_updates_it(self):
        user = get_user_model().objects.create_user(
            username="account@example.com-0123456789abcdefabcd",
            email="account@example.com",
            first_name="Test User",
            password="A-strong-test-password-481!",
        )
        self.client.force_login(user)

        page = self.client.get(reverse("account"))
        self.assertContains(page, 'value="account@example.com"')

        response = self.client.post(reverse("account"), {
            "action": "username",
            "username": "new-login@example.com",
        })
        self.assertRedirects(response, reverse("account"))
        user.refresh_from_db()
        self.assertEqual(user.email, "new-login@example.com")
        self.assertNotIn("0123456789abcdefabcd", user.username)


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
        detail_url = reverse("product_detail", kwargs={"slug": product.slug})
        self.assertContains(response, f'href="{detail_url}"')

    def test_catalog_renders_product_image(self):
        category = Category.objects.create(name="Украшения", coment="Описание категории")
        product = Products.objects.create(
            name="Товар с фото",
            sale=1500,
            material="Серебро",
            date_prod=date(2026, 2, 1),
            conter=1,
            cat_id=category,
            image="products/test.jpg",
        )

        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        detail_url = reverse("product_detail", kwargs={"slug": product.slug})
        self.assertContains(response, f'src="{product.image.url}"')
        self.assertContains(response, f'href="{detail_url}"')
        self.assertContains(response, "Фотографии приведены для примера")
        self.assertContains(response, 'href="/media/products/PHOTO_CREDITS.txt"')


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
        Products.objects.filter(pk=self.product.pk).update(image="products/test.jpg")
        response = self.client.get(reverse("product_detail", kwargs={"slug": self.product.slug}))

        self.assertEqual(response.status_code, 200)
        detail_url = reverse("product_detail", kwargs={"slug": self.product.slug})
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.cat_id.name)
        self.assertContains(response, "Фото приведено для примера")
        self.assertContains(response, f'rel="canonical" href="{detail_url}"')

    def test_product_detail_has_jsonld_and_canonical(self):
        response = self.client.get(reverse("product_detail", kwargs={"slug": self.product.slug}))

        detail_url = reverse("product_detail", kwargs={"slug": self.product.slug})
        self.assertContains(response, '"@type": "Product"')
        self.assertContains(response, "https://schema.org/InStock")
        self.assertContains(response, f'rel="canonical" href="{detail_url}"')

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


class ReviewFixTests(TestCase):
    """Проверки исправлений: кэш каталога, неверный фильтр, настройки в шаблонах."""

    def test_invalid_category_id_does_not_crash(self):
        response = self.client.get(reverse('products'), {'category_id': 'abc'})
        self.assertEqual(response.status_code, 200)

    def test_catalog_cache_is_separate_for_logged_in_user(self):
        get_user_model().objects.create_user(
            username='u1', email='u1@example.com', password='Str0ng-pass-91')
        self.client.get(reverse('products'))  # анонимная страница попадает в кэш
        self.client.login(username='u1@example.com', password='Str0ng-pass-91')
        page = self.client.get(reverse('products')).content.decode()
        self.assertIn('Аккаунт', page)

    def test_templates_do_not_expose_secret_key(self):
        from django.template import engines
        from django.test import RequestFactory
        template = engines['django'].from_string('{{ settings.SECRET_KEY }}|{{ settings.YMETRICA_ID }}')
        self.assertEqual(template.render({}, RequestFactory().get('/')), '|')

    def test_sitemap_skips_products_without_slug(self):
        category = Category.objects.create(name='K', coment='c')
        product = Products.objects.create(
            name='Без слага', sale=1, material='m', date_prod=date(2026, 1, 1), conter=1, cat_id=category)
        Products.objects.filter(pk=product.pk).update(slug=None)
        self.assertNotContains(self.client.get(reverse('sitemap_xml')), '/products/None/')


class PaginationAndValidationTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Категория', coment='Описание')

    def test_catalog_shows_all_fifty_products_and_reports_total(self):
        for number in range(50):
            Products.objects.create(
                name=f'Товар {number}',
                sale=100 + number,
                material='Серебро',
                date_prod=date(2026, 1, 1),
                conter=number,
                cat_id=self.category,
            )
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['product']), 50)
        self.assertContains(response, 'Всего позиций: <b>50</b>')

    def test_catalog_pagination_preserves_filters_after_fifty_products(self):
        for number in range(51):
            Products.objects.create(
                name=f'Товар {number}',
                sale=100 + number,
                material='Серебро',
                date_prod=date(2026, 1, 1),
                conter=1,
                cat_id=self.category,
            )
        response = self.client.get(reverse('products'), {
            'q': 'Товар',
            'category_id': self.category.pk,
            'material': 'Серебро',
            'stock': 'available',
            'sort': '-sale',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Всего позиций: <b>51</b>')
        preserved_filters = parse_qs(response.context['query_string'])
        self.assertEqual(preserved_filters['q'], ['Товар'])
        self.assertEqual(preserved_filters['category_id'], [str(self.category.pk)])
        self.assertEqual(preserved_filters['material'], ['Серебро'])
        self.assertEqual(preserved_filters['stock'], ['available'])
        self.assertEqual(preserved_filters['sort'], ['-sale'])
        escaped_query = response.context['query_string'].replace('&', '&amp;')
        self.assertContains(
            response,
            f'{escaped_query}&amp;page=2',
        )

    def test_negative_product_values_are_invalid(self):
        product = Products(
            name='Некорректный товар',
            sale=-1,
            material='Металл',
            date_prod=date(2026, 1, 1),
            conter=-1,
            cat_id=self.category,
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_reviews_are_paginated(self):
        for number in range(11):
            Review.objects.create(name=f'Клиент {number}', rating=5, text='Отлично')
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="pagination"', 1)


class FooterContactTests(TestCase):
    @override_settings(
        SITE_ADDRESS=(
            "\u0420\u0452\u0420\u0491\u0421\u0402\u0420\xb5\u0421\u0403 "
            "\u0420\u0405\u0420\xb5 \u0421\u0453\u0420\u0454\u0420\xb0"
            "\u0420\xb7\u0420\xb0\u0420\u0405"
        )
    )
    def test_footer_repairs_mojibaked_address(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, "Адрес не указан")
        self.assertNotContains(response, "\u0420\u0452")
