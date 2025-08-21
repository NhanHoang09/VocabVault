import { api } from '@/lib/api-client';
import { API_ENDPOINTS } from '@/config/constants';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  username: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
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
    created_at: string;
    updated_at: string | null;
  };
}

export const authApi = {
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>(
      API_ENDPOINTS.AUTH.LOGIN,
      data
    );
    return response.data;
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>(
      API_ENDPOINTS.AUTH.REGISTER,
      data
    );
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post(API_ENDPOINTS.AUTH.LOGOUT);
  },

  refreshToken: async (): Promise<AuthResponse> => {
    // ✅ Không cần refreshToken parameter - cookie sẽ tự động gửi
    const response = await api.post<AuthResponse>(API_ENDPOINTS.AUTH.REFRESH);
    return response.data;
  },

  verifyToken: async (): Promise<{ user: AuthResponse['user'] }> => {
    const response = await api.get<{ user: AuthResponse['user'] }>(
      API_ENDPOINTS.AUTH.VERIFY
    );
    return response.data;
  },
};
