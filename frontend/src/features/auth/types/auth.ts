export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  total_points: number;
  level: number;
  experience_points: number;
  study_streak_days: number;
  longest_streak: number;
  last_study_date: string | null;
  total_study_time_minutes: number;
  total_cards_studied: number;
  total_correct_answers: number;
  total_incorrect_answers: number;
  average_accuracy: number;
  study_preferences: Record<string, any>;
  notification_settings: Record<string, any>;
  privacy_settings: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
}

export interface AuthState {
  user: User | null;
  accessToken: string | null; // ✅ Chỉ lưu trong RAM
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  username: string;
}

export interface AuthError {
  message: string;
  field?: string;
  code?: string;
}
