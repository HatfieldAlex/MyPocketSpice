from django.contrib import admin
from .models import (
    SkillLevel,
    Ingredient,
    Category,
    Recipe,
    Instruction,
    RecipeIngredient,
)


@admin.register(SkillLevel)
class SkillLevelAdmin(admin.ModelAdmin):
    list_display = ["id", "level"]
    search_fields = ["level"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class InstructionInline(admin.TabularInline):
    model = Instruction
    extra = 1
    fields = ["step_number", "content"]
    ordering = ["step_number"]


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ["ingredient", "quantity"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "category", "preparation_duration",
                    "servings", "skill_level", "created_at"]
    search_fields = ["title", "description"]
    list_filter = ["category", "skill_level"]
    inlines = [InstructionInline, RecipeIngredientInline]


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "step_number"]
    list_filter = ["recipe"]
    ordering = ["recipe", "step_number"]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "ingredient", "quantity"]
    list_filter = ["recipe", "ingredient"]
