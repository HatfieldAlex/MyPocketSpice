from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Recipe, Category
from .serializers import (
    RecipeListSerializer,
    RecipeDetailSerializer,
)


# -------------------------------------------------
# Pagination used across list views
# -------------------------------------------------
class RecipePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# -------------------------------------------------
# 1. Landing page – paginated newest recipes
# -------------------------------------------------
class RecipeLandingPageView(generics.ListAPIView):
    queryset = Recipe.objects.all().order_by("-created_at")
    serializer_class = RecipeListSerializer
    pagination_class = RecipePagination


# -------------------------------------------------
# 2. Category filtered list (ForeignKey)
# -------------------------------------------------
class RecipeByCategoryView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    pagination_class = RecipePagination

    def get_queryset(self):
        category_name = self.kwargs["category"]
        return Recipe.objects.filter(
            category__name__iexact=category_name
        ).order_by("-created_at")


# -------------------------------------------------
# 3. Search recipes by title
# -------------------------------------------------
class RecipeSearchView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    pagination_class = RecipePagination

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        return Recipe.objects.filter(
            title__icontains=query
        ).order_by("-created_at")


# -------------------------------------------------
# 4. Full detail page by ID
# -------------------------------------------------
class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    lookup_field = "id"
