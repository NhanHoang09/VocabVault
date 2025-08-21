// API Constants
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    LOGOUT: '/api/v1/auth/logout',
    REFRESH: '/api/v1/auth/refresh',
    VERIFY: '/api/v1/auth/me',
  },
  USER: {
    PROFILE: '/users/profile',
    UPDATE: '/users/update',
    DELETE: '/users/delete',
  },
  FLASHCARDS: {
    LISTS: '/flashcards/lists',
    CARDS: '/flashcards/cards',
    STUDY_SESSIONS: '/flashcards/study-sessions',
  },
  STUDY: {
    SESSIONS: '/study/sessions',
    PROGRESS: '/study/progress',
    ANALYTICS: '/study/analytics',
  },
  GAMIFICATION: {
    BADGES: '/gamification/badges',
    LEADERBOARD: '/gamification/leaderboard',
    ACHIEVEMENTS: '/gamification/achievements',
  },
  AI: {
    CHAT: '/ai/chat',
    LESSONS: '/ai/lessons',
    PRACTICE: '/ai/practice',
  },
} as const;

// HTTP Status Codes
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
} as const;

// Study Constants
export const STUDY_CONSTANTS = {
  DIFFICULTY_LEVELS: {
    EASY: 'easy',
    MEDIUM: 'medium',
    HARD: 'hard',
  },
  STUDY_MODES: {
    FLASHCARD: 'flashcard',
    QUIZ: 'quiz',
    SPELLING: 'spelling',
    LISTENING: 'listening',
  },
  SESSION_TYPES: {
    NEW: 'new',
    REVIEW: 'review',
    MIXED: 'mixed',
  },
} as const;

// UI Constants
export const UI_CONSTANTS = {
  ANIMATION_DURATION: {
    FAST: 150,
    NORMAL: 300,
    SLOW: 500,
  },
  BREAKPOINTS: {
    MOBILE: 640,
    TABLET: 768,
    DESKTOP: 1024,
    LARGE_DESKTOP: 1280,
  },
  Z_INDEX: {
    DROPDOWN: 1000,
    STICKY: 1020,
    FIXED: 1030,
    MODAL_BACKDROP: 1040,
    MODAL: 1050,
    POPOVER: 1060,
    TOOLTIP: 1070,
  },
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'user_data',
  THEME: 'theme',
  STUDY_PROGRESS: 'study_progress',
  SETTINGS: 'settings',
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  FORBIDDEN: 'Access denied.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  SERVER_ERROR: 'Something went wrong. Please try again later.',
  UNKNOWN_ERROR: 'An unknown error occurred.',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Successfully logged in!',
  REGISTER_SUCCESS: 'Account created successfully!',
  LOGOUT_SUCCESS: 'Successfully logged out!',
  SAVE_SUCCESS: 'Changes saved successfully!',
  DELETE_SUCCESS: 'Item deleted successfully!',
  STUDY_COMPLETE: 'Study session completed!',
} as const;

// Validation Rules
export const VALIDATION_RULES = {
  PASSWORD: {
    MIN_LENGTH: 8,
    REQUIRE_UPPERCASE: true,
    REQUIRE_LOWERCASE: true,
    REQUIRE_NUMBER: true,
    REQUIRE_SPECIAL: true,
  },
  USERNAME: {
    MIN_LENGTH: 3,
    MAX_LENGTH: 20,
    PATTERN: /^[a-zA-Z0-9_]+$/,
  },
  EMAIL: {
    PATTERN: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  },
} as const;
