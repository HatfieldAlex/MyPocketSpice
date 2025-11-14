from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Recipe, Category, SkillLevel


class RecipeApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Italian")
        self.skill = SkillLevel.objects.create(level="low")
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            category=self.category,
            description="Test description",
            preparation_duration=20,
            servings=2,
            skill_level=self.skill,
        )

    def test_list_recipes(self):
        """GET /api/recipes/ returns a paginated list of recipes"""
        url = reverse("recipe-list-landing")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data.get("count", 0), 1)

    def test_recipe_detail(self):
        """GET /api/recipes/{id}/ returns recipe detail"""
        url = reverse("recipe-detail", kwargs={"id": self.recipe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Recipe")


class AuthApiTests(APITestCase):
    def test_register_validation(self):
        """POST /api/auth/register/ validates password mismatch"""
        url = reverse("user-register")
        payload = {
            "username": "testuser",
            "password": "password123",
            "password_confirm": "different",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_requires_credentials(self):
        """POST /api/auth/login/ requires username and password"""
        url = reverse("user-login")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AiMatchTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="Vegetarian")
        skill = SkillLevel.objects.create(level="low")
        self.recipe = Recipe.objects.create(
            title="Vegetable Curry",
            category=category,
            description="",
            preparation_duration=30,
            servings=3,
            skill_level=skill,
        )

    def test_ai_match_requires_ingredients(self):
        """POST /api/recipes/ai-match/ requires ingredients field"""
        url = reverse("ai-recipe-match")
        response = self.client.post(url, {"ingredients": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
