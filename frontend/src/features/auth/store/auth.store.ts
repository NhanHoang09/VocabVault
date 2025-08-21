import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthState, AuthTokens } from '../types/auth';
import { authApi, LoginRequest, RegisterRequest } from '../api/auth.api';
import { STORAGE_KEYS } from '@/config/constants';
// import { showSuccessToast, showWarningToast } from '@/lib/api';

interface AuthStore extends AuthState {
  // Actions
  login: (credentials: LoginRequest) => Promise<void>;
  register: (credentials: RegisterRequest) => Promise<void>;
  logout: () => void;
  setAccessToken: (token: string) => void;
  clearAccessToken: () => void;
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  refreshAuth: () => Promise<void>;
  initializeAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      accessToken: null, // ✅ Chỉ trong RAM
      isAuthenticated: false,
      isLoading: true, // ✅ Bắt đầu với loading = true để check auth
      error: null,

      // Actions
      login: async (credentials: LoginRequest) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.login(credentials);

          // ✅ Chỉ lưu access token vào RAM, KHÔNG lưu vào localStorage
          // ✅ Refresh token được lưu trong HttpOnly cookie bởi backend

          // Convert response user to User type
          const user: User = {
            ...response.user,
            createdAt: response.user.created_at,
            updatedAt: response.user.updated_at || new Date().toISOString(),
          };

          set({
            user,
            accessToken: response.access_token, // ✅ Lưu access token vào RAM
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });

          console.log('Successfully logged in!');
        } catch (error: any) {
          const errorMessage = error.response?.data?.message || 'Login failed';
          set({
            isLoading: false,
            error: errorMessage,
          });

          throw error;
        }
      },

      setAccessToken: (token: string) => set({ accessToken: token }),
      clearAccessToken: () => set({ accessToken: null }),

      register: async (credentials: RegisterRequest) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authApi.register(credentials);

          // ✅ Chỉ lưu access token vào RAM, KHÔNG lưu vào localStorage
          // ✅ Refresh token được lưu trong HttpOnly cookie bởi backend

          // Convert response user to User type
          const user: User = {
            ...response.user,
            createdAt: response.user.created_at,
            updatedAt: response.user.updated_at || new Date().toISOString(),
          };

          set({
            user,
            accessToken: response.access_token, // ✅ Lưu access token vào RAM
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });

          // Show success toast
          // showSuccessToast('Account created successfully!');
          console.log('Account created successfully!');
        } catch (error: any) {
          const errorMessage =
            error.response?.data?.message || 'Registration failed';
          set({
            isLoading: false,
            error: errorMessage,
          });

          // Error toast will be shown by middleware
          throw error;
        }
      },

      logout: async () => {
        try {
          // ✅ Gọi logout API để clear refresh token cookie
          await authApi.logout();
        } catch (error) {
          console.error('Logout error:', error);
        } finally {
          // ✅ Clear access token khỏi RAM
          set({
            user: null,
            accessToken: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }

        console.log('Successfully logged out!');
      },

      setUser: (user: User | null) => {
        set({ user, isAuthenticated: !!user });
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      setError: (error: string | null) => {
        set({ error });
      },

      clearError: () => {
        set({ error: null });
      },

      refreshAuth: async () => {
        try {
          // ✅ Gọi refresh endpoint (cookie sẽ tự động gửi)
          const response = await authApi.refreshToken();

          // ✅ Update access token trong RAM
          const user: User = {
            ...response.user,
            createdAt: response.user.created_at,
            updatedAt: response.user.updated_at || new Date().toISOString(),
          };

          set({
            accessToken: response.access_token,
            user,
            isAuthenticated: true,
          });
        } catch (error) {
          // ✅ Refresh failed - logout user
          get().logout();
        }
      },

      initializeAuth: async () => {
        try {
          // ✅ Gọi refresh endpoint để check xem có refresh token không
          const response = await authApi.refreshToken();

          // ✅ Update access token trong RAM
          const user: User = {
            ...response.user,
            createdAt: response.user.created_at,
            updatedAt: response.user.updated_at || new Date().toISOString(),
          };

          set({
            accessToken: response.access_token,
            user,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          // ✅ Không có refresh token hoặc token expired - set loading = false
          set({
            user: null,
            accessToken: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: state => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
