
# MyPocketSpice

A full‑stack recipe management app with AI‑powered ingredient matching.

- **Backend**: Django 5 + Django REST Framework, JWT auth, AI ingredient matching via Google Gemini  
- **Frontend**: Vue 3 + TypeScript, design system, type‑safe API client  
- **Hosting**: Backend on Render, frontend on Netlify (or any static host)

---

## Monorepo Structure

```text
my_pocket_spice/
├── backend/                 # Django backend (API, models, AI, auth)
└── frontend/
    └── my-pocket-spice/     # Vue 3 frontend
```

---

## Backend (Django API)

### Tech Stack

- Django 5.2
- Django REST Framework
- drf‑spectacular (OpenAPI schema + Swagger UI)
- djangorestframework‑simplejwt (JWT auth)
- google‑generativeai (Gemini)
- python‑dotenv

### API Overview

**Base URL (production)**  
`https://my-pocket-spice-backend.onrender.com/api`

Key endpoints:

- **Recipes**
  - `GET /api/recipes/` – Paginated recipe list (landing)
  - `GET /api/recipes/{id}/` – Recipe detail
  - `GET /api/recipes/category/{category}/` – Filter by category name (e.g. `Italian`, `Asian`)
  - `GET /api/recipes/search/?q=term` – Search by title
  - `POST /api/recipes/create/` – Create a full recipe (auth required)

- **Authentication**
  - `POST /api/auth/register/` – Sign up
  - `POST /api/auth/login/` – Sign in (returns access + refresh tokens)
  - `POST /api/auth/logout/` – Logout (blacklists refresh token)
  - `GET /api/auth/me/` – Current user info

- **AI**
  - `POST /api/recipes/ai-match/`
    - Body:
      ```json
      { "ingredients": "chicken, tomatoes, pasta" }
      ```
    - Behaviour:
      - Prefers **exact ingredient matches** (no AI call if there’s a direct match).
      - Otherwise calls Gemini and returns:
        ```json
        {
          "count": 1,
          "recipe": { /* RecipeList */ },
          "justification": "With your eggs and herbs..."
        }
        ```

### API Docs

The backend exposes an OpenAPI schema and docs via drf‑spectacular:

- `GET /api/schema/` – OpenAPI 3 schema (JSON)
- `GET /api/docs/` – Swagger UI
- `GET /api/redoc/` – Redoc documentation

You can plug the schema into tools like Postman, Stoplight, or code generators.

---

## Database Schema (Core Models)

### Recipe

```text
Recipe
- id: AutoField
- title: CharField(500)
- category: ForeignKey(Category, null=True, blank=True, PROTECT)
- description: TextField
- preparation_duration: IntegerField
- servings: IntegerField(null=True, blank=True)
- skill_level: ForeignKey(SkillLevel, null=True, blank=True, SET_NULL)
- author: ForeignKey(User, null=True, blank=True, SET_NULL)
- created_at: DateTimeField(auto_now_add=True)
```

### Category

```text
Category
- id: AutoField
- name: CharField(unique=True)
```

### SkillLevel

```text
SkillLevel
- id: AutoField
- level: CharField (e.g. "low", "medium")
```

### Ingredient

```text
Ingredient
- id: AutoField
- name: CharField
```

### RecipeIngredient

```text
RecipeIngredient
- id: AutoField
- recipe: ForeignKey(Recipe, related_name="recipe_ingredients")
- ingredient: ForeignKey(Ingredient)
- quantity: CharField (e.g. "2 cups", "100g")
```

### Instruction

```text
Instruction
- id: AutoField
- recipe: ForeignKey(Recipe, related_name="instructions")
- step_number: IntegerField
- content: TextField
```

---

## AI Approach

The AI endpoint uses a **hybrid strategy** combining deterministic matching and generative AI.

### 1. Exact Match Pre‑Filter (no AI call)

1. Normalize user input into ingredient tokens (e.g. `"curry paste, garlic"` → `["curry paste", "garlic"]`).
2. For each recipe, normalize its ingredient names from `RecipeIngredient`.
3. If any user ingredient exactly matches any recipe ingredient for a recipe, that recipe is considered an **exact match**.
4. If exact matches exist, the endpoint returns the top match immediately with a whimsical justification, e.g.:

   > “With your curry paste, you could make Vegetable Curry! Check you have the right amounts, but then the only thing you’d need is X.”

This gives fast, reliable behaviour for obvious cases without using tokens or AI.

### 2. Gemini Fallback

If there are **no** exact matches:

- Build a concise prompt listing:
  - User ingredients
  - Candidate recipes (id, title, category, skill level, ingredient summaries)
- Ask Gemini to respond strictly with JSON:

  ```json
  { "recipe_id": 23, "justification": "..." }
  ```

- Parse the JSON, fetch the chosen recipe, and return it plus the justification.
- Defensive parsing and error handling ensure that malformed responses don’t crash the API.

### 3. Error Handling

- Validates that `GOOGLE_AI_API_KEY` is configured.
- Handles model errors (404 for model name, missing permissions) with clear error messages.
- Provides detailed diagnostics and an optional `test_gemini_api.py` helper script.

---

## Frontend (Vue 3)

Located in `frontend/my-pocket-spice/`.

### Tech Stack

- Vue 3 (Composition API, `<script setup>`)
- TypeScript
- Vue Router 4
- Design system with semantic tokens
- Typed API client & composables

### Structure (high‑level)

```text
src/
  api/
    config.ts          # Base URL, mock mode
    types/             # Types from OpenAPI schema
    client/            # HTTP + typed API client
  components/
    HeroSection.vue
    RecipeCard.vue
    CategoryFilter.vue
    AIIngredientModal.vue
    AILoadingState.vue
    LoginModal.vue
    ui/                # Button, Input, Card, Badge, Container
  composables/
    useAuth.ts
    useRecipes.ts
  pages/
    RecipeListPage.vue
    RecipeDetailPage.vue
    RecipeCreatePage.vue
  design-system/
    tokens.ts
    global.css
  router/
    index.ts
  App.vue
  main.ts
```

### Key Frontend Features

- **Recipe browsing**
  - Hero with search.
  - Category pills (All, Italian, Asian, Vegetarian, Seafood, Dessert, Breakfast, My Recipes).
  - Paginated grid (9 recipes per page).

- **Recipe detail**
  - Category, skill level, prep time, servings.
  - Ingredients and step‑by‑step instructions.
  - AI justification block when navigated via AI suggestion (“Based on the ingredients you provided…”).

- **Create recipe**
  - Auth‑gated – only signed‑in users can create recipes.
  - Fields:
    - Title
    - Description
    - Category (mapped to backend `Category`)
    - Difficulty (mapped to backend `SkillLevel` via `skill_level_id`)
    - Preparation time
    - Servings
    - Dynamic ingredients list `{ name, quantity }`
    - Dynamic instructions list `{ step_number, content }`
  - Aligned with the backend `RecipeCreateSerializer`.

- **Auth UX**
  - Header shows:
    - When signed out: **Sign In** / **Sign Up** buttons (modal).
    - When signed in: username + **Logout** and **+ Create Recipe**.
  - JWT tokens stored in `localStorage`, attached via `Authorization: Bearer …` in the HTTP client.

- **AI UX**
  - “Not sure what to cook?” CTA in the hero.
  - AI ingredient modal for entering free‑text ingredients.
  - Branded loading state while AI is “thinking”.
  - Redirects to recommended recipe with AI explanation shown on the detail page.

---

## Security & Configuration

> These configurations harden the app without changing core business logic.

### Backend Environment

Use environment variables in production. In `backend/.env` (not committed):

```env
DJANGO_SECRET_KEY=your-production-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=my-pocket-spice-backend.onrender.com
GOOGLE_AI_API_KEY=your-gemini-key
```

The settings module reads these values (see below).

### Django Settings (Highlights)

- `DEBUG` is **True by default**, but should be `False` in production.
- `ALLOWED_HOSTS` includes `my-pocket-spice-backend.onrender.com` plus local dev hosts.
- JWT settings (`SIMPLE_JWT`) handle token lifetimes, rotation, and blacklisting.

For CORS in production, you should eventually restrict origins to your frontend domain (currently the project allows all origins for simplicity while developing).

---

## Linting

### Backend (Django)

Install dev tools:

```bash
cd backend
pip install flake8 black
```

Run:

```bash
flake8
black .
```

### Frontend (Vue)

From `frontend/my-pocket-spice/`:

```bash
npm run lint
npm run type-check
```

These commands use ESLint + TypeScript to enforce consistent code style and catch type issues.

---

## Testing

### Backend Tests

Basic tests live in `backend/core/tests.py` and cover:

- Listing recipes (`GET /api/recipes/`).
- Fetching a recipe detail (`GET /api/recipes/{id}/`).
- Basic AI endpoint validation for missing input.

Run:

```bash
cd backend
python manage.py test
```

### Frontend

This project relies primarily on type checking and linting for frontend safety. You can add component‑level tests later using Vitest or Jest if needed.

---

## Deployment

### Backend – Render.com

1. **Root Directory**: `backend`
2. **Build Command**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Start Command**:

   ```bash
   gunicorn config.wsgi:application
   ```

4. **Environment vars** (in Render dashboard):

   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=my-pocket-spice-backend.onrender.com`
   - `GOOGLE_AI_API_KEY`

5. **Migrations**: either via a Pre‑deploy command or manually:

   ```bash
   python manage.py migrate
   ```

### Frontend – Netlify

1. **Base directory**: `frontend/my-pocket-spice`
2. **Build command**:

   ```bash
   npm run build
   ```

3. **Publish directory**: `dist`
4. **Environment vars** (optional, base URL is already set to the Render backend):

   - `VUE_APP_API_URL=https://my-pocket-spice-backend.onrender.com/api`
   - `VUE_APP_USE_MOCK=false`

After deployment, the frontend calls the Render backend directly for all API operations.

---

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend/my-pocket-spice
npm install
npm run serve
```

The Vue app will run on `http://localhost:8080` and talk to the backend on Render by default.


