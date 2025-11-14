# My Pocket Spice - Recipe Management Application

A modern, type-safe Vue 3 recipe management application built with TypeScript, featuring a warm design system and full OpenAPI schema integration.

## Features

- ✅ **Type-Safe API Client** - Generated from OpenAPI schema
- ✅ **Design System** - Complete token-based design system with warm recipe theme
- ✅ **Recipe List Page** - Paginated grid with search and filtering
- ✅ **Recipe Detail Page** - Full recipe view with ingredients and instructions
- ✅ **Mock Mode** - Switchable mock data for development
- ✅ **Responsive Design** - Mobile-first responsive layout
- ✅ **Accessibility** - ARIA labels and keyboard navigation support

## Project Structure

```
src/
├── api/
│   ├── client/          # Typed API client
│   │   ├── index.ts     # Main API client
│   │   ├── http.ts      # HTTP client wrapper
│   │   └── mock-data.ts # Mock data matching schema
│   ├── config.ts        # API configuration
│   └── types/           # TypeScript types from OpenAPI schema
│       └── index.ts
├── components/
│   ├── ui/              # Shared UI components
│   │   ├── Button.vue
│   │   ├── Card.vue
│   │   ├── Input.vue
│   │   ├── Badge.vue
│   │   └── Container.vue
│   ├── RecipeCard.vue   # Recipe card component
│   └── HeroSection.vue  # Hero section with search
├── composables/
│   └── useRecipes.ts    # Recipe data fetching composables
├── design-system/
│   ├── tokens.ts        # Design tokens (colors, spacing, etc.)
│   └── global.css       # Global styles
├── pages/
│   ├── RecipeListPage.vue   # Recipe list page
│   └── RecipeDetailPage.vue # Recipe detail page
├── router/
│   └── index.ts         # Vue Router configuration
├── App.vue              # Root component
└── main.ts              # Application entry point
```

## Design System

The application uses a comprehensive design system with semantic tokens:

- **Colors**: Warm orange/coral primary, cream backgrounds, fresh green accents, MyPocketSkill blue branding
- **Spacing**: Consistent 4px-based scale
- **Typography**: System font stack with semantic sizes
- **Shadows**: Layered elevation system
- **Animations**: Smooth transitions and interactions

All components use design tokens - no hardcoded values.

## API Integration

The API client is fully typed based on the OpenAPI schema (`schema.yaml`):

- `GET /api/recipes/` - Paginated recipe list
- `GET /api/recipes/{id}/` - Recipe detail
- `GET /api/recipes/category/{category}/` - Filter by category
- `GET /api/recipes/search/` - Search recipes
- `POST /api/recipes/create/` - Create recipe

## Configuration

Create a `.env` file in the project root:

```env
VUE_APP_API_URL=https://my-pocket-spice-backend.onrender.com/api
VUE_APP_USE_MOCK=false
```

Set `VUE_APP_USE_MOCK=true` to use mock data instead of the API.

## Development

```bash
# Install dependencies
npm install

# Serve with hot reload
npm run serve

# Build for production
npm run build

# Type check
npm run type-check

# Lint
npm run lint
```

## TypeScript

The project is fully typed with TypeScript. Types are generated from the OpenAPI schema to ensure type safety across the application.

## Browser Support

Modern browsers with ES2020 support. Uses Vue 3 Composition API with `<script setup>` syntax.

## License

Private project
