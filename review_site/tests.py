from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from .models import Category
from .forms import FeedbackForm
from .views import add_company, update_company, delete_company


class ModelCategoryTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Category 100")

    def test_category_name(self):
        self.assertEqual(self.category.name, "Category 100")

    def test_delete_category(self):
        self.category.delete()
        self.rez = Category.objects.filter(name="Category 100").exists()
        self.assertFalse(self.rez)

    def test_update_category(self):
        self.category.name = "Category 1000"
        self.assertEqual(self.category.name, "Category 1000")


class FormFeedbackTests(TestCase):
    def test_form_valid(self):
        data = {"name": "Joe Biden", "email": "joebiden@gmail.com", "message": "Nice site!"}
        form = FeedbackForm(data=data)
        self.assertEqual(form.is_valid(), True)

    def test_form_invalid(self):
        data = {"name": "", "email": "", "message": ""}
        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_email_error(self):
        data = {"name": "Name", "email": "invalid@", "message": "Hello!"}
        form = FeedbackForm(data=data)
        self.assertTrue(form.errors)


class NotAuthenticatedUserTests(TestCase):
    def test_not_authenticated_add_company(self):
        response = self.client.get(reverse('add_company'))
        self.assertEqual(response.status_code, 302)

    def test_not_authenticated_delete_company(self):
        response = self.client.get(reverse('delete_company', kwargs={"company_name": "test"}))
        self.assertEqual(response.status_code, 302)

    def test_not_authenticated_edit_company(self):
        response = self.client.get(reverse('update_company', kwargs={"company_name": "test"}))
        self.assertEqual(response.status_code, 302)


class AuthenticatedUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="testpass")
        self.client.login(username="test", password="testpass")

    def test_authenticated_add_company(self):
        response = self.client.get(reverse('add_company'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_my_companies(self):
        response = self.client.get(reverse('my_companies'))
        self.assertEqual(response.status_code, 200)


class UrlsTests(TestCase):
    def test_resolve_add_company(self):
        resolver = resolve('/add-company/')
        self.assertEqual(resolver.func, add_company)

    def test_resolve_update_company(self):
        resolver = resolve('/update-company/test/')
        self.assertEqual(resolver.func, update_company)

    def test_resolve_delete_company(self):
        resolver = resolve('/delete-company/test/')
        self.assertEqual(resolver.func, delete_company)
