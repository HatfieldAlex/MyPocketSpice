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


# -------------------------------------------------
# Create serializer for full recipe creation
# -------------------------------------------------

class RecipeCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    description = serializers.CharField()
    preparation_duration = serializers.IntegerField()
    servings = serializers.IntegerField(required=False, allow_null=True)
    skill_level_id = serializers.IntegerField(required=False, allow_null=True)

    category = serializers.CharField(required=False, allow_blank=True)

    ingredients = serializers.ListField(child=serializers.DictField(), required=False)
    instructions = serializers.ListField(child=serializers.DictField(), required=False)

    def create(self, validated_data):
        category_name = validated_data.pop("category", None)
        ingredients_data = validated_data.pop("ingredients", [])
        instructions_data = validated_data.pop("instructions", [])

        # CATEGORY: get or create (case-insensitive)
        category = None
        if category_name:
            category, _ = Category.objects.get_or_create(
                name__iexact=category_name,
                defaults={"name": category_name}
            )

        # SKILL LEVEL: must exist
        skill_level = None
        skill_level_id = validated_data.pop("skill_level_id", None)
        if skill_level_id:
            skill_level = SkillLevel.objects.get(id=skill_level_id)

        # CREATE RECIPE
        recipe = Recipe.objects.create(
            category=category,
            skill_level=skill_level,
            **validated_data
        )

        # INGREDIENTS + RECIPE INGREDIENTS
        for item in ingredients_data:
            name = item.get("name")
            quantity = item.get("quantity")
            if not name:
                continue

            ingredient, _ = Ingredient.objects.get_or_create(
                name__iexact=name,
                defaults={"name": name}
            )

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity or "",
            )

        # INSTRUCTIONS
        for step in instructions_data:
            Instruction.objects.create(
                recipe=recipe,
                step_number=step.get("step_number"),
                content=step.get("content", "")
            )

        return recipe


class RecipeCreatedResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "category",
            "skill_level",
            "created_at",
            "servings",
            "preparation_duration",
        ]
