/**
 * Vue Router Configuration
 */

import { createRouter, createWebHistory } from 'vue-router'
import RecipeListPage from '@/pages/RecipeListPage.vue'
import RecipeDetailPage from '@/pages/RecipeDetailPage.vue'
import RecipeCreatePage from '@/pages/RecipeCreatePage.vue'

const routes = [
  {
    path: '/',
    redirect: '/recipes',
  },
  {
    path: '/recipes',
    name: 'RecipeList',
    component: RecipeListPage,
  },
  {
    path: '/recipes/create',
    name: 'RecipeCreate',
    component: RecipeCreatePage,
  },
  {
    path: '/recipes/:id',
    name: 'RecipeDetail',
    component: RecipeDetailPage,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

