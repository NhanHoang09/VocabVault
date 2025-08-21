'use client';

import { useEffect } from 'react';
import { useAuthStore } from '@/features/auth/store/auth.store';

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { initializeAuth, isLoading } = useAuthStore();

  useEffect(() => {
    // Initialize auth state khi app khởi động
    initializeAuth();
  }, [initializeAuth]);

  return <>{children}</>;
};
