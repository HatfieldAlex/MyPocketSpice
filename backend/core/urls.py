from django.urls import path
from .views import (
    RecipeLandingPageView,
    RecipeByCategoryView,
    RecipeSearchView,
    RecipeDetailView,
    RecipeCreateView,
)

urlpatterns = [
    # 1. Landing page list (paginated)
    path("recipes/", RecipeLandingPageView.as_view(), name="recipe-list-landing"),

    # 2. Filter by category (Category.name)
    path(
        "recipes/category/<str:category>/",
        RecipeByCategoryView.as_view(),
        name="recipe-by-category",
    ),

    # 3. Title search
    path("recipes/search/", RecipeSearchView.as_view(), name="recipe-search"),

    # 4. Full detail view by recipe ID
    path("recipes/<int:id>/", RecipeDetailView.as_view(), name="recipe-detail"),

    # 5. Create a new full recipe with nested relationships
    path("recipes/create/", RecipeCreateView.as_view(), name="recipe-create"),

]
