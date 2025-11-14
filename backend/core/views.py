from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

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
    """
    POST /api/recipes/create/
    Create a new recipe (requires authentication)
    """
    serializer_class = RecipeCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = RecipeCreateSerializer(
            data=request.data,
            context={'request': request}
        )
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
    
    # Normalize user input for exact matching
    user_input_normalized = user_input.lower().strip()
    user_ingredients = [ing.strip().lower() for ing in user_input_normalized.split(',')]
    
    # First, check for exact ingredient matches before calling AI
    exact_matches = []
    for recipe in recipes:
        recipe_ingredients = [
            ri.ingredient.name.lower().strip()
            for ri in recipe.recipe_ingredients.all()
        ]
        # Check if any user ingredient exactly matches any recipe ingredient
        for user_ing in user_ingredients:
            if user_ing in recipe_ingredients:
                exact_matches.append(recipe)
                break  # Found a match, no need to check other ingredients for this recipe
    
    # If we found exact matches, return the first one immediately with justification
    if exact_matches:
        best_match = exact_matches[0]
        serializer = RecipeListSerializer(best_match)
        
        # Create whimsical justification for exact match
        recipe_ingredients = [
            ri.ingredient.name for ri in best_match.recipe_ingredients.all()
        ]
        matched_ings = [ing for ing in user_ingredients if ing in [ri.lower().strip() for ri in recipe_ingredients]]
        
        if matched_ings:
            # Format matched ingredients nicely
            matched_display = ', '.join([ing.title() for ing in matched_ings])
            missing_ings = [ri for ri in recipe_ingredients if ri.lower().strip() not in user_ingredients]
            
            if missing_ings:
                missing_display = ', '.join(missing_ings[:3])  # Show first 3 missing
                if len(missing_ings) > 3:
                    missing_display += f", and {len(missing_ings) - 3} more thing{'s' if len(missing_ings) - 3 > 1 else ''}"
                justification = f"With your {matched_display}, you could make {best_match.title}! Check you have the right amounts, but then the only thing you'd need is {missing_display}."
            else:
                justification = f"Perfect match! With your {matched_display}, you have everything you need to make {best_match.title}. You're all set to create something delicious!"
        else:
            justification = f"Great news! You have the perfect ingredients to make {best_match.title}. Check you have the right amounts, and you're ready to cook!"
        
        return Response({
            'count': 1,
            'recipe': serializer.data,
            'justification': justification
        }, status=status.HTTP_200_OK)
    
    # No exact matches found, use AI to find best match
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
    prompt = f"""You are a whimsical recipe matching assistant. A user has these ingredients: "{user_input}"

Here are all available recipes:

{chr(10).join(recipes_text)}

Find the SINGLE best matching recipe based on the user's ingredients. 
Priority order:
1. EXACT ingredient match (if user ingredient appears exactly in recipe ingredients, this is the best match)
2. Direct ingredient matches (same ingredient name)
3. Similar ingredients or substitutes
4. Recipe category relevance

Return a JSON object with two fields:
1. "recipe_id": the single best matching recipe ID (just the number)
2. "justification": a whimsical, friendly message explaining why this recipe was chosen, in the style of:
   "With your [user ingredients], you could make [recipe name]! Check you have the right amounts, but then the only thing you'd need is [missing ingredients or encouragement]."
   
Make it warm, encouraging, and slightly playful. Reference the user's ingredients and what they'd need.

Example format:
{{
  "recipe_id": 23,
  "justification": "With your curry paste, you could make Vegetable Curry! Check you have the right amounts, but then the only thing you'd need is some fresh vegetables and a bit of time to let those flavors meld together."
}}

Return ONLY the JSON object, no other text."""
    
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
        
        # Try to parse as JSON object (with recipe_id and justification)
        try:
            ai_response = json.loads(response_text)
            
            # Handle both old format (array) and new format (object)
            if isinstance(ai_response, list):
                # Old format: just an array of IDs
                matched_ids = ai_response
                justification = None
            elif isinstance(ai_response, dict):
                # New format: object with recipe_id and justification
                matched_ids = [ai_response.get('recipe_id')]
                justification = ai_response.get('justification')
            else:
                raise ValueError(f"Unexpected response format: {type(ai_response)}")
                
        except json.JSONDecodeError:
            # Try to extract array from text (fallback for old format)
            array_match = re.search(r'\[[\d,\s]+\]', response_text)
            if array_match:
                matched_ids = json.loads(array_match.group(0))
                justification = None
            else:
                # Try to extract object
                object_match = re.search(r'\{[^}]+\}', response_text)
                if object_match:
                    try:
                        ai_response = json.loads(object_match.group(0))
                        matched_ids = [ai_response.get('recipe_id')]
                        justification = ai_response.get('justification')
                    except:
                        raise ValueError(f"Could not parse JSON from response: {response_text}")
                else:
                    raise ValueError(f"Could not parse JSON from response: {response_text}")
        
        # Validate that matched_ids is a list
        if not isinstance(matched_ids, list) or not matched_ids:
            raise ValueError(f"Expected non-empty list, got {matched_ids}")
        
        # Get the best matching recipe
        recipe_id = matched_ids[0]
        if recipe_id not in recipe_id_map:
            raise ValueError(f"Recipe ID {recipe_id} not found in available recipes")
        
        best_match = recipe_id_map[recipe_id]
        serializer = RecipeListSerializer(best_match)
        
        # Generate justification if not provided by AI
        if not justification:
            # Create a simple justification based on ingredients
            recipe_ingredients = [
                ri.ingredient.name for ri in best_match.recipe_ingredients.all()
            ]
            user_ing_list = [ing.strip() for ing in user_input.split(',')]
            matched_ings = [ing for ing in user_ing_list if any(ing.lower() in ri.lower() or ri.lower() in ing.lower() for ri in recipe_ingredients)]
            
            if matched_ings:
                justification = f"With your {', '.join(matched_ings)}, you could make {best_match.title}! Check you have the right amounts, but then you're all set to create something delicious."
            else:
                justification = f"You could make {best_match.title}! This recipe matches your ingredients and will be a great choice for your next meal."
        
        return Response({
            'count': 1,
            'recipe': serializer.data,
            'justification': justification
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