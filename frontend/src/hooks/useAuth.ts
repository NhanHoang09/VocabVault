'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { User, LoginCredentials, RegisterData, AuthResponse } from '@/types';
import { AUTH_CONFIG, ROUTES } from '@/constants';
import { api } from '@/lib/api';

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem(AUTH_CONFIG.TOKEN_KEY);
        const userData = localStorage.getItem(AUTH_CONFIG.USER_KEY);

        if (token && userData) {
          const user = JSON.parse(userData);
          setUser(user);

          // Verify token with backend
          await api.get('/auth/verify');
        }
      } catch (error) {
        // Token is invalid, clear storage
        localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
        localStorage.removeItem(AUTH_CONFIG.USER_KEY);
        localStorage.removeItem(AUTH_CONFIG.REFRESH_TOKEN_KEY);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        setIsLoading(true);
        const response = await api.post<AuthResponse>(
          '/auth/login',
          credentials
        );

        const { user, token, refreshToken } = response.data;

        // Store auth data
        localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
        localStorage.setItem(AUTH_CONFIG.REFRESH_TOKEN_KEY, refreshToken);
        localStorage.setItem(AUTH_CONFIG.USER_KEY, JSON.stringify(user));

        setUser(user);
        router.push(ROUTES.DASHBOARD);
      } catch (error) {
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const register = useCallback(
    async (data: RegisterData) => {
      try {
        setIsLoading(true);
        const response = await api.post<AuthResponse>('/auth/register', data);

        const { user, token, refreshToken } = response.data;

        // Store auth data
        localStorage.setItem(AUTH_CONFIG.TOKEN_KEY, token);
        localStorage.setItem(AUTH_CONFIG.REFRESH_TOKEN_KEY, refreshToken);
        localStorage.setItem(AUTH_CONFIG.USER_KEY, JSON.stringify(user));

        setUser(user);
        router.push(ROUTES.DASHBOARD);
      } catch (error) {
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const logout = useCallback(() => {
    // Clear auth data
    localStorage.removeItem(AUTH_CONFIG.TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.REFRESH_TOKEN_KEY);
    localStorage.removeItem(AUTH_CONFIG.USER_KEY);

    setUser(null);
    router.push(ROUTES.HOME);
  }, [router]);

  const updateUser = useCallback(
    (userData: Partial<User>) => {
      if (user) {
        const updatedUser = { ...user, ...userData };
        setUser(updatedUser);
        localStorage.setItem(AUTH_CONFIG.USER_KEY, JSON.stringify(updatedUser));
      }
    },
    [user]
  );

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    updateUser,
  };
}
