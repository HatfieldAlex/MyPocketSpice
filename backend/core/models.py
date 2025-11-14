from django.db import models


class SkillLevel(models.Model):
    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=50)

    def __str__(self):
        return self.level


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="recipes",
        null=True,
        blank=True,
    )
    description = models.TextField()
    preparation_duration = models.IntegerField() 
    servings = models.IntegerField(null=True, blank=True)
    skill_level = models.ForeignKey(
        SkillLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Instruction(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="instructions"
    )
    step_number = models.IntegerField()
    content = models.TextField()

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"{self.recipe.title} - Step {self.step_number}"


class RecipeIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.CharField(max_length=200)  # "2 cups", "100g", etc.

    def __str__(self):
        return f"{self.quantity} {self.ingredient.name} for {self.recipe.title}"
