"""
Diagnostic script to test Google Gemini API configuration
Run this to debug API key and model availability issues
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai package not installed")
    print("Run: pip install google-generativeai")
    sys.exit(1)

# Get API key
api_key = os.getenv('GOOGLE_AI_API_KEY')

if not api_key or api_key == 'YOUR_KEY_HERE':
    print("ERROR: GOOGLE_AI_API_KEY not found in .env file")
    print("Please add: GOOGLE_AI_API_KEY=your_actual_key")
    sys.exit(1)

print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
print(f"✓ API Key length: {len(api_key)} characters\n")

# Configure API
try:
    genai.configure(api_key=api_key)
    print("✓ API configured successfully\n")
except Exception as e:
    print(f"✗ Failed to configure API: {e}")
    sys.exit(1)

# Try to list models
print("Attempting to list available models...")
try:
    models = list(genai.list_models())
    print(f"✓ Found {len(models)} models:\n")
    for model in models:
        methods = getattr(model, 'supported_generation_methods', [])
        print(f"  - {model.name}")
        if methods:
            print(f"    Methods: {', '.join(methods)}")
        print()
except Exception as e:
    print(f"✗ Failed to list models: {e}\n")
    models = []

# Try to use models directly
print("Testing model access...\n")
test_models = [
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro-latest',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro',
]

success = False
for model_name in test_models:
    try:
        print(f"Trying: {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello in one word")
        print(f"✓ SUCCESS with {model_name}!")
        print(f"  Response: {response.text}\n")
        success = True
        break
    except Exception as e:
        print(f"✗ Failed: {str(e)[:100]}\n")
        continue

if not success:
    print("\n" + "="*60)
    print("TROUBLESHOOTING:")
    print("="*60)
    print("1. Verify your API key at: https://aistudio.google.com/app/apikey")
    print("2. Make sure you're using a 'Generative Language API' key (not Vertex AI)")
    print("3. Check that the API key has no restrictions")
    print("4. Try creating a new API key")
    print("5. Ensure the google-generativeai package is up to date:")
    print("   pip install --upgrade google-generativeai")
    print("\nIf models list is empty, your API key might not have")
    print("permission to list models, but direct access might still work.")

