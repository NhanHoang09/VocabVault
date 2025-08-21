// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
} as const;

// Authentication
export const AUTH_CONFIG = {
  TOKEN_KEY: 'vocabvault_token',
  REFRESH_TOKEN_KEY: 'vocabvault_refresh_token',
  USER_KEY: 'vocabvault_user',
  TOKEN_EXPIRY: 24 * 60 * 60 * 1000, // 24 hours
} as const;

// Study Configuration
export const STUDY_CONFIG = {
  DAILY_GOAL_DEFAULT: 20,
  SESSION_LENGTH_DEFAULT: 15, // minutes
  REVIEW_INTERVALS: [1, 3, 7, 14, 30, 90], // days
  MASTERY_LEVELS: {
    NEW: 0,
    LEARNING: 1,
    REVIEWING: 2,
    MASTERED: 3,
    EXPERT: 4,
    PERFECT: 5,
  },
  DIFFICULTY_LEVELS: {
    BEGINNER: 'beginner',
    INTERMEDIATE: 'intermediate',
    ADVANCED: 'advanced',
  },
} as const;

// Gamification
export const GAMIFICATION_CONFIG = {
  XP_PER_WORD: 10,
  XP_PER_CORRECT_ANSWER: 5,
  XP_STREAK_BONUS: 2,
  LEVEL_XP_REQUIREMENT: 100,
  MAX_LEVEL: 100,
  ACHIEVEMENTS: {
    FIRST_WORD: 'first_word',
    STREAK_7_DAYS: 'streak_7_days',
    STREAK_30_DAYS: 'streak_30_days',
    MASTER_100_WORDS: 'master_100_words',
    PERFECT_SESSION: 'perfect_session',
  },
} as const;

// UI Configuration
export const UI_CONFIG = {
  ANIMATION_DURATION: 300,
  TOAST_DURATION: 3000,
  DEBOUNCE_DELAY: 300,
  INFINITE_SCROLL_THRESHOLD: 100,
  PAGINATION: {
    DEFAULT_PAGE_SIZE: 20,
    MAX_PAGE_SIZE: 100,
  },
} as const;

// Supported Languages
export const SUPPORTED_LANGUAGES = {
  EN: { code: 'en', name: 'English', flag: '🇺🇸' },
  VI: { code: 'vi', name: 'Tiếng Việt', flag: '🇻🇳' },
  JA: { code: 'ja', name: '日本語', flag: '🇯🇵' },
  KO: { code: 'ko', name: '한국어', flag: '🇰🇷' },
  ZH: { code: 'zh', name: '中文', flag: '🇨🇳' },
  FR: { code: 'fr', name: 'Français', flag: '🇫🇷' },
  DE: { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  ES: { code: 'es', name: 'Español', flag: '🇪🇸' },
} as const;

// Vocabulary Categories
export const VOCABULARY_CATEGORIES = {
  BASIC: 'basic',
  FOOD: 'food',
  TRAVEL: 'travel',
  BUSINESS: 'business',
  TECHNOLOGY: 'technology',
  HEALTH: 'health',
  EDUCATION: 'education',
  ENTERTAINMENT: 'entertainment',
  SPORTS: 'sports',
  FAMILY: 'family',
} as const;

// Part of Speech
export const PARTS_OF_SPEECH = {
  NOUN: 'noun',
  VERB: 'verb',
  ADJECTIVE: 'adjective',
  ADVERB: 'adverb',
  PRONOUN: 'pronoun',
  PREPOSITION: 'preposition',
  CONJUNCTION: 'conjunction',
  INTERJECTION: 'interjection',
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Kết nối mạng không ổn định. Vui lòng thử lại.',
  UNAUTHORIZED: 'Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.',
  FORBIDDEN: 'Bạn không có quyền truy cập tính năng này.',
  NOT_FOUND: 'Không tìm thấy dữ liệu yêu cầu.',
  VALIDATION_ERROR: 'Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.',
  SERVER_ERROR: 'Lỗi máy chủ. Vui lòng thử lại sau.',
  UNKNOWN_ERROR: 'Đã xảy ra lỗi không xác định.',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  LOGIN_SUCCESS: 'Đăng nhập thành công!',
  REGISTER_SUCCESS: 'Đăng ký thành công!',
  LOGOUT_SUCCESS: 'Đăng xuất thành công!',
  WORD_LEARNED: 'Từ vựng đã được học thành công!',
  PROGRESS_SAVED: 'Tiến độ đã được lưu!',
  SETTINGS_UPDATED: 'Cài đặt đã được cập nhật!',
  PROFILE_UPDATED: 'Hồ sơ đã được cập nhật!',
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  THEME: 'vocabvault_theme',
  LANGUAGE: 'vocabvault_language',
  SETTINGS: 'vocabvault_settings',
  STUDY_PROGRESS: 'vocabvault_study_progress',
  CACHED_WORDS: 'vocabvault_cached_words',
} as const;

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  STUDY: '/study',
  VOCABULARY: '/vocabulary',
  PROGRESS: '/progress',
  PROFILE: '/profile',
  SETTINGS: '/settings',
  DEMO: '/demo',
} as const;

// Breakpoints
export const BREAKPOINTS = {
  SM: 640,
  MD: 768,
  LG: 1024,
  XL: 1280,
  '2XL': 1536,
} as const;

// Z-Index Scale
export const Z_INDEX = {
  DROPDOWN: 1000,
  STICKY: 1020,
  FIXED: 1030,
  MODAL_BACKDROP: 1040,
  MODAL: 1050,
  POPOVER: 1060,
  TOOLTIP: 1070,
  TOAST: 1080,
} as const;
