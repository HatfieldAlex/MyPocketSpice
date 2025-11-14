from rest_framework import serializers
from .models import (
    Recipe,
    Instruction,
    RecipeIngredient,
    Ingredient,
    SkillLevel,
    Category,
)


# -------------------------------------------------
# Basic serializers for nested relationships
# -------------------------------------------------
class SkillLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillLevel
        fields = ["id", "level"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


# -------------------------------------------------
# Lightweight serializer for lists / landing page
# -------------------------------------------------
class RecipeListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    skill_level = SkillLevelSerializer()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "preparation_duration",
            "servings",
            "category",
            "skill_level",
            "created_at",
        ]


# -------------------------------------------------
# Detailed serializer for recipe detail page
# -------------------------------------------------
class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "quantity"]


class InstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruction
        fields = ["id", "step_number", "content"]


class RecipeDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    skill_level = SkillLevelSerializer()
    instructions = InstructionSerializer(many=True, read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "category",
            "description",
            "preparation_duration",
            "servings",
            "skill_level",
            "created_at",
            "instructions",
            "recipe_ingredients",
        ]
