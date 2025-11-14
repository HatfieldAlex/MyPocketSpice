from django.urls import path
from .views import (
    RecipeLandingPageView,
    RecipeByCategoryView,
    RecipeSearchView,
    RecipeDetailView,
    RecipeCreateView,
    ai_recipe_match,
)
from .auth_views import (
    UserRegistrationView,
    user_login_view,
    user_logout_view,
    current_user_view,
)

urlpatterns = [
    # Authentication endpoints
    path("auth/register/", UserRegistrationView.as_view(), name="user-register"),
    path("auth/login/", user_login_view, name="user-login"),
    path("auth/logout/", user_logout_view, name="user-logout"),
    path("auth/me/", current_user_view, name="current-user"),

    # Recipe endpoints
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

    # 5. Create a new full recipe with nested relationships (requires auth)
    path("recipes/create/", RecipeCreateView.as_view(), name="recipe-create"),

    # 6. AI Recipe Matching endpoint
    path("recipes/ai-match/", ai_recipe_match, name="ai-recipe-match"),

]
