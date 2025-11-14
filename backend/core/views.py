from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view

from .models import Recipe, Category
from .serializers import (
    RecipeListSerializer,
    RecipeDetailSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecipeCreateSerializer, RecipeCreatedResponseSerializer

import google.generativeai as genai
import os
import json
import re



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

class RecipeCreateView(generics.CreateAPIView):
    serializer_class = RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = RecipeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        response_data = RecipeCreatedResponseSerializer(recipe).data
        return Response(response_data, status=status.HTTP_201_CREATED)


# -------------------------------------------------
# AI Recipe Matching endpoint using Google Gemini
# -------------------------------------------------
@api_view(['POST'])
def ai_recipe_match(request):
    """
    Match user ingredient input to recipes using Google AI Studio (Gemini)
    
    Request body: {"ingredients": "chicken, tomatoes, pasta"}
    Returns: List of matching recipes ordered by relevance
    """
    user_input = request.data.get('ingredients', '').strip()
    
    if not user_input:
        return Response(
            {'error': 'Please provide ingredients'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get API key from environment
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key or api_key == 'YOUR_KEY_HERE':
        return Response(
            {'error': 'Google AI API key not configured'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Configure Gemini API
    try:
        genai.configure(api_key=api_key)
        # Try to get client info to verify API key works
        try:
            # This will help us see what's available
            test_models = list(genai.list_models())
            if test_models:
                # Log available models for debugging
                available_model_names = [m.name for m in test_models]
            else:
                # If list_models returns empty, try direct model access
                pass
        except Exception:
            # If list_models fails, we'll try direct model access anyway
            pass
    except Exception as e:
        return Response(
            {'error': f'Failed to configure Gemini API: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Fetch all recipes with their ingredients
    try:
        recipes = Recipe.objects.select_related('category', 'skill_level').prefetch_related(
            'recipe_ingredients__ingredient'
        ).all()
        
        if not recipes.exists():
            return Response(
                {'error': 'No recipes found'},
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {'error': f'Failed to fetch recipes: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Format recipes for Gemini prompt
    recipes_text = []
    recipe_id_map = {}
    
    for recipe in recipes:
        ingredients_list = [
            f"{ri.ingredient.name} ({ri.quantity})" 
            for ri in recipe.recipe_ingredients.all()
        ]
        
        recipe_info = f"""Recipe ID: {recipe.id}
Title: {recipe.title}
Category: {recipe.category.name if recipe.category else 'N/A'}
Ingredients: {', '.join(ingredients_list) if ingredients_list else 'N/A'}
Description: {recipe.description[:200] if recipe.description else 'N/A'}
"""
        recipes_text.append(recipe_info)
        recipe_id_map[recipe.id] = recipe
    
    # Create prompt for Gemini
    prompt = f"""You are a recipe matching assistant. A user has these ingredients: "{user_input}"

Here are all available recipes:

{chr(10).join(recipes_text)}

Based on the user's ingredients, rank the recipes from most relevant to least relevant. 
Consider:
- Direct ingredient matches
- Similar ingredients or substitutes
- Recipe category relevance
- Overall compatibility

Return ONLY a JSON array of recipe IDs in order of relevance (most relevant first).
Format: [1, 5, 3, 7, ...]

Do not include any explanation, just the JSON array."""
    
    try:
        # Call Gemini API - try different approaches based on API version
        # The error suggests v1beta API, so models might be named differently
        
        response = None
        last_error = None
        
        # First, try to get available models if possible
        try:
            available_models = list(genai.list_models())
            if available_models:
                # Use the first model that supports generateContent
                for model_info in available_models:
                    if hasattr(model_info, 'supported_generation_methods') and 'generateContent' in model_info.supported_generation_methods:
                        model_name = model_info.name
                        # Remove 'models/' prefix if present
                        if '/' in model_name:
                            model_name = model_name.split('/')[-1]
                        try:
                            model = genai.GenerativeModel(model_name)
                            response = model.generate_content(prompt)
                            break
                        except Exception as e:
                            last_error = str(e)
                            continue
        except Exception as e:
            # If list_models fails, continue to direct model access
            last_error = str(e)
        
        # If no model found from list, try common model names directly
        if response is None:
            # Try different model name formats
            model_names_to_try = [
                'gemini-1.5-flash-latest',  # Latest format
                'gemini-1.5-pro-latest',
                'gemini-1.5-flash',
                'gemini-1.5-pro',
                'gemini-pro',
                # Try with full path
                'models/gemini-1.5-flash-latest',
                'models/gemini-1.5-pro-latest',
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro',
                'models/gemini-pro',
            ]
            
            for model_name in model_names_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    break  # Success, exit loop
                except Exception as e:
                    last_error = str(e)
                    continue  # Try next model
        
        if response is None:
            # Provide helpful error message
            error_msg = (
                f"Could not find a working Gemini model. "
                f"Last error: {last_error}. "
                f"\n\nTroubleshooting steps:\n"
                f"1. Verify your API key at https://aistudio.google.com/app/apikey\n"
                f"2. Make sure the API key has 'Generative Language API' enabled\n"
                f"3. Check if your API key has any restrictions\n"
                f"4. Try creating a new API key\n"
                f"5. Ensure you're using the correct API key (not Vertex AI key)"
            )
            raise ValueError(error_msg)
        
        # Parse JSON response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if '```' in response_text:
            # Extract content between code blocks
            match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
            if match:
                response_text = match.group(1).strip()
        
        # Try to parse as JSON
        try:
            matched_ids = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract array from text
            array_match = re.search(r'\[[\d,\s]+\]', response_text)
            if array_match:
                matched_ids = json.loads(array_match.group(0))
            else:
                raise ValueError(f"Could not parse JSON from response: {response_text}")
        
        # Validate that matched_ids is a list
        if not isinstance(matched_ids, list):
            raise ValueError(f"Expected list, got {type(matched_ids)}")
        
        # Get recipes in matched order, preserving only valid IDs
        matched_recipes = []
        for rid in matched_ids:
            if rid in recipe_id_map:
                matched_recipes.append(recipe_id_map[rid])
        
        # If no matches found, return all recipes in original order
        if not matched_recipes:
            matched_recipes = list(recipes)
        
        # Serialize results
        serializer = RecipeListSerializer(matched_recipes, many=True)
        
        return Response({
            'count': len(matched_recipes),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError as e:
        return Response(
            {'error': f'Failed to parse AI response as JSON: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'AI matching failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )