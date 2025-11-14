/**
 * Design System Tokens
 * Warm Recipe Theme - Inspired by Tasty and AllRecipes
 * Colors: #FED1F6 (pink), #FFFFFF (white), #0A8961 (green), #0A0A0A (black), #066A4E (darker green)
 */

// ============================================
// Color Tokens - Warm Recipe Theme
// ============================================

export const colors = {
  // Primary - Warm Pink (#FED1F6)
  primary: {
    50: '#FFF5FC',
    100: '#FFE8F8',
    200: '#FED1F6', // Main primary
    300: '#FDB8F0',
    400: '#FC9FE9',
    500: '#FB86E2',
    600: '#FA6DDB',
    700: '#F954D4',
    800: '#F83BCD',
    900: '#F722C6',
  },

  // Backgrounds - White and Cream
  background: {
    primary: '#FFFFFF',    // Main background
    secondary: '#FFFBFE',   // Card backgrounds
    tertiary: '#FFF5FC',    // Subtle sections
    elevated: '#FFFFFF',   // Elevated surfaces
  },

  // Accents - Fresh Green (#0A8961)
  accent: {
    50: '#E6F5F1',
    100: '#CCEBE3',
    200: '#99D7C7',
    300: '#66C3AB',
    400: '#33AF8F',
    500: '#0A8961', // Main accent
    600: '#086E4E',
    700: '#066A4E', // Darker green
    800: '#05533D',
    900: '#033C2C',
  },

  // Text Colors
  text: {
    primary: '#0A0A0A',    // Main text (black)
    secondary: '#4A4A4A',  // Secondary text
    tertiary: '#8A8A8A',   // Tertiary text
    inverse: '#FFFFFF',    // White text
    disabled: '#CCCCCC',   // Disabled text
  },

  // Neutrals
  neutral: {
    50: '#FAFAFA',
    100: '#F5F5F5',
    200: '#E8E8E8',
    300: '#D9D9D9',
    400: '#BFBFBF',
    500: '#8C8C8C',
    600: '#595959',
    700: '#434343',
    800: '#262626',
    900: '#0A0A0A',
  },

  // Semantic Colors
  semantic: {
    success: '#0A8961',
    warning: '#FFB800',
    error: '#FF4D4F',
    info: '#1890FF',
  },
} as const

// ============================================
// Spacing Scale
// ============================================

export const spacing = {
  0: '0',
  1: '0.25rem',   // 4px
  2: '0.5rem',    // 8px
  3: '0.75rem',   // 12px
  4: '1rem',      // 16px
  5: '1.25rem',   // 20px
  6: '1.5rem',    // 24px
  8: '2rem',      // 32px
  10: '2.5rem',   // 40px
  12: '3rem',     // 48px
  16: '4rem',     // 64px
  20: '5rem',     // 80px
  24: '6rem',     // 96px
  32: '8rem',     // 128px
} as const

// ============================================
// Typography
// ============================================

export const typography = {
  fontFamily: {
    sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
    serif: ['Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
    mono: ['Menlo', 'Monaco', 'Consolas', '"Liberation Mono"', '"Courier New"', 'monospace'],
  },
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
    '5xl': '3rem',     // 48px
  },
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },
  lineHeight: {
    none: '1',
    tight: '1.25',
    snug: '1.375',
    normal: '1.5',
    relaxed: '1.625',
    loose: '2',
  },
} as const

// ============================================
// Border Radius
// ============================================

export const radius = {
  none: '0',
  sm: '0.25rem',   // 4px
  base: '0.5rem',  // 8px
  md: '0.75rem',   // 12px
  lg: '1rem',      // 16px
  xl: '1.5rem',    // 24px
  '2xl': '2rem',   // 32px
  full: '9999px',
} as const

// ============================================
// Shadows
// ============================================

export const shadows = {
  sm: '0 1px 2px 0 rgba(10, 10, 10, 0.05)',
  base: '0 1px 3px 0 rgba(10, 10, 10, 0.1), 0 1px 2px 0 rgba(10, 10, 10, 0.06)',
  md: '0 4px 6px -1px rgba(10, 10, 10, 0.1), 0 2px 4px -1px rgba(10, 10, 10, 0.06)',
  lg: '0 10px 15px -3px rgba(10, 10, 10, 0.1), 0 4px 6px -2px rgba(10, 10, 10, 0.05)',
  xl: '0 20px 25px -5px rgba(10, 10, 10, 0.1), 0 10px 10px -5px rgba(10, 10, 10, 0.04)',
  '2xl': '0 25px 50px -12px rgba(10, 10, 10, 0.25)',
  inner: 'inset 0 2px 4px 0 rgba(10, 10, 10, 0.06)',
  none: 'none',
} as const

// ============================================
// Animation Tokens
// ============================================

export const animations = {
  duration: {
    fast: '150ms',
    base: '200ms',
    slow: '300ms',
    slower: '500ms',
  },
  easing: {
    linear: 'linear',
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
  },
  transitions: {
    default: 'all 200ms cubic-bezier(0.4, 0, 0.2, 1)',
    colors: 'color 200ms ease, background-color 200ms ease, border-color 200ms ease',
    transform: 'transform 200ms cubic-bezier(0.4, 0, 0.2, 1)',
    opacity: 'opacity 200ms ease',
  },
} as const

// ============================================
// Breakpoints (for responsive design)
// ============================================

export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
} as const

// ============================================
// Z-Index Scale
// ============================================

export const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
} as const
