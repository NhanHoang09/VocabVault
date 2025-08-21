'use client';

import { useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/features/auth/store/auth.store';
import { ROUTES } from '@/constants';
import {
  User,
  LoginCredentials,
  RegisterCredentials,
} from '@/features/auth/types/auth';

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterCredentials) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

export function useAuth(): UseAuthReturn {
  const router = useRouter();

  // ✅ Sử dụng Zustand store
  const {
    user,
    isLoading,
    isAuthenticated,
    login: storeLogin,
    register: storeRegister,
    logout: storeLogout,
    setUser,
  } = useAuthStore();

  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        await storeLogin(credentials);
        router.push(ROUTES.DASHBOARD);
      } catch (error) {
        throw error;
      }
    },
    [storeLogin, router]
  );

  const register = useCallback(
    async (data: RegisterCredentials) => {
      try {
        await storeRegister(data);
        router.push(ROUTES.DASHBOARD);
      } catch (error) {
        throw error;
      }
    },
    [storeRegister, router]
  );

  const logout = useCallback(async () => {
    try {
      await storeLogout();
      router.push(ROUTES.HOME);
    } catch (error) {
      console.error('Logout error:', error);
      router.push(ROUTES.HOME);
    }
  }, [storeLogout, router]);

  const updateUser = useCallback(
    (userData: Partial<User>) => {
      if (user) {
        const updatedUser = { ...user, ...userData };
        setUser(updatedUser);
      }
    },
    [user, setUser]
  );

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
  };
}
