// User related types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  avatar?: string;
  targetLanguage: string;
  nativeLanguage: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserProfile extends User {
  totalWordsLearned: number;
  currentStreak: number;
  longestStreak: number;
  level: number;
  experience: number;
}

// Authentication types
export interface LoginCredentials {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterData {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  targetLanguage: string;
  termsAccepted: boolean;
}

export interface AuthResponse {
  user: User;
  token: string;
  refreshToken: string;
}

// Vocabulary related types
export interface Vocabulary {
  id: string;
  word: string;
  translation: string;
  pronunciation: string;
  partOfSpeech: string;
  definition: string;
  example: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  category: string;
  tags: string[];
  imageUrl?: string;
  audioUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Flashcard extends Vocabulary {
  isLearned: boolean;
  lastReviewed: Date;
  nextReview: Date;
  reviewCount: number;
  masteryLevel: number; // 0-5
}

// Study session types
export interface StudySession {
  id: string;
  userId: string;
  startTime: Date;
  endTime?: Date;
  duration: number; // in minutes
  wordsStudied: number;
  correctAnswers: number;
  incorrectAnswers: number;
  sessionType: 'flashcard' | 'quiz' | 'writing' | 'listening';
}

// Progress tracking types
export interface ProgressStats {
  totalWordsLearned: number;
  currentStreak: number;
  longestStreak: number;
  totalStudyTime: number; // in minutes
  accuracyRate: number; // percentage
  level: number;
  experience: number;
  experienceToNextLevel: number;
}

// AI related types
export interface AIRecommendation {
  wordId: string;
  reason: string;
  priority: 'high' | 'medium' | 'low';
  difficultyAdjustment?: number;
}

export interface LearningPath {
  id: string;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedDuration: number; // in days
  words: string[];
  prerequisites?: string[];
}

// Gamification types
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  isUnlocked: boolean;
  unlockedAt?: Date;
  progress: number; // 0-100
  target: number;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: 'study' | 'streak' | 'mastery' | 'social';
  isEarned: boolean;
  earnedAt?: Date;
}

// Social features types
export interface StudyGroup {
  id: string;
  name: string;
  description: string;
  members: User[];
  maxMembers: number;
  isPrivate: boolean;
  createdAt: Date;
}

export interface LeaderboardEntry {
  userId: string;
  username: string;
  avatar?: string;
  score: number;
  rank: number;
  totalWordsLearned: number;
  currentStreak: number;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Form types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'select' | 'textarea' | 'checkbox';
  required: boolean;
  placeholder?: string;
  options?: { value: string; label: string }[];
  validation?: {
    minLength?: number;
    maxLength?: number;
    pattern?: string;
    custom?: (value: any) => boolean | string;
  };
}

// UI Component types
export interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

// Theme types
export interface Theme {
  name: string;
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
    error: string;
    success: string;
    warning: string;
  };
}

// Settings types
export interface UserSettings {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  notifications: {
    email: boolean;
    push: boolean;
    reminder: boolean;
    reminderTime: string;
  };
  studyPreferences: {
    dailyGoal: number;
    sessionLength: number;
    difficulty: 'easy' | 'medium' | 'hard';
    autoPlayAudio: boolean;
  };
}
