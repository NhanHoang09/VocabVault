export const appConfig = {
  name: 'My Vocabulary Vault',
  description: 'A comprehensive vocabulary learning platform',
  version: '1.0.0',

  // API Configuration
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    timeout: 10000,
  },

  // Study Configuration
  study: {
    defaultSessionDuration: 25 * 60 * 1000, // 25 minutes
    breakDuration: 5 * 60 * 1000, // 5 minutes
    maxCardsPerSession: 50,
    reviewInterval: {
      easy: 7 * 24 * 60 * 60 * 1000, // 7 days
      medium: 3 * 24 * 60 * 60 * 1000, // 3 days
      hard: 1 * 24 * 60 * 60 * 1000, // 1 day
    },
  },

  // Gamification Configuration
  gamification: {
    pointsPerCorrectAnswer: 10,
    pointsPerStreak: 5,
    bonusPoints: {
      perfectSession: 50,
      dailyGoal: 100,
      weeklyGoal: 500,
    },
  },

  // UI Configuration
  ui: {
    theme: {
      primary: '#3B82F6',
      secondary: '#10B981',
      accent: '#F59E0B',
      danger: '#EF4444',
      success: '#10B981',
      warning: '#F59E0B',
      info: '#3B82F6',
    },
    breakpoints: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
  },

  // Feature flags
  features: {
    aiTutor: true,
    gamification: true,
    socialFeatures: true,
    advancedAnalytics: true,
    offlineMode: false,
  },
} as const;
