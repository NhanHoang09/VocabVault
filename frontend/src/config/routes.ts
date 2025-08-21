export const routes = {
  // Public routes
  home: '/',
  login: '/login',
  register: '/register',
  about: '/about',
  contact: '/contact',

  // Auth routes
  auth: {
    login: '/login',
    register: '/register',
    forgotPassword: '/forgot-password',
    resetPassword: '/reset-password',
    verifyEmail: '/verify-email',
  },

  // Dashboard routes
  dashboard: {
    root: '/dashboard',
    overview: '/dashboard/overview',
    profile: '/dashboard/profile',
    settings: '/dashboard/settings',
  },

  // Study routes
  study: {
    root: '/study',
    session: '/study/session',
    review: '/study/review',
    progress: '/study/progress',
    analytics: '/study/analytics',
  },

  // Flashcard routes
  flashcards: {
    root: '/flashcards',
    create: '/flashcards/create',
    edit: (id: string) => `/flashcards/${id}/edit`,
    view: (id: string) => `/flashcards/${id}`,
    study: (id: string) => `/flashcards/${id}/study`,
  },

  // Gamification routes
  gamification: {
    root: '/gamification',
    badges: '/gamification/badges',
    leaderboard: '/gamification/leaderboard',
    achievements: '/gamification/achievements',
    challenges: '/gamification/challenges',
  },

  // AI Tutor routes
  ai: {
    root: '/ai-tutor',
    chat: '/ai-tutor/chat',
    lessons: '/ai-tutor/lessons',
    practice: '/ai-tutor/practice',
  },

  // Social routes
  social: {
    root: '/social',
    friends: '/social/friends',
    groups: '/social/groups',
    discussions: '/social/discussions',
  },

  // Admin routes
  admin: {
    root: '/admin',
    users: '/admin/users',
    content: '/admin/content',
    analytics: '/admin/analytics',
  },
} as const;

// Route guards
export const routeGuards = {
  public: [
    routes.home,
    routes.login,
    routes.register,
    routes.about,
    routes.contact,
  ],
  authenticated: [
    routes.dashboard.root,
    routes.study.root,
    routes.flashcards.root,
    routes.gamification.root,
    routes.ai.root,
    routes.social.root,
  ],
  admin: [routes.admin.root],
} as const;
