from rest_framework import generics
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
