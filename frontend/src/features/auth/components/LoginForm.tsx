'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Link from 'next/link';
import Button from '@/components/ui/Button';
import { useAuth } from '@/hooks/useAuth';
import { LoginCredentials } from '../types/auth';
import { loginSchema, type LoginFormData } from '../schemas/auth.schema';
import { GradientText, GlassCard } from '@/components/ui';

export const LoginForm: React.FC = () => {
  const { login, isLoading } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data);
      // ✅ Login thành công - useAuth hook sẽ handle redirect
    } catch (error) {
      console.error('Login error:', error);
      // ✅ Error handling sẽ được manage bởi auth store
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <GlassCard className="max-w-md w-full p-8">
        <div className="text-center mb-8">
          <div className="mx-auto h-16 w-16 bg-gradient-to-r from-primary-950 to-primary-500 rounded-2xl flex items-center justify-center shadow-lg mb-6 animate-pulse">
            <span className="text-white font-black text-2xl">🔐</span>
          </div>
          <h2 className="text-3xl font-black mb-2">
            <GradientText gradient="from-primary-950 to-primary-500">
              Đăng nhập
            </GradientText>
          </h2>
          <p className="text-white/80">
            Hoặc{' '}
            <Link
              href="/register"
              className="font-semibold text-accent-500 hover:text-accent-400 transition-colors"
            >
              đăng ký tài khoản mới ✨
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-semibold text-white mb-2"
              >
                📧 Email
              </label>
              <input
                {...register('email')}
                type="email"
                id="email"
                placeholder="Nhập email của bạn"
                autoComplete="email"
                className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
              />
              {errors.email && (
                <p className="text-sm text-pink-300 mt-1">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-semibold text-white mb-2"
              >
                🔒 Mật khẩu
              </label>
              <input
                {...register('password')}
                type="password"
                id="password"
                placeholder="Nhập mật khẩu"
                autoComplete="current-password"
                className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-300"
              />
              {errors.password && (
                <p className="text-sm text-pink-300 mt-1">
                  {errors.password.message}
                </p>
              )}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-primary-500 focus:ring-primary-500 border-white/30 rounded bg-white/20"
              />
              <label
                htmlFor="remember-me"
                className="ml-2 block text-sm text-white/80"
              >
                Ghi nhớ đăng nhập
              </label>
            </div>

            <div className="text-sm">
              <Link
                href="/forgot-password"
                className="font-medium text-accent-500 hover:text-accent-400 transition-colors"
              >
                Quên mật khẩu?
              </Link>
            </div>
          </div>

          <div>
            <Button 
              type="submit" 
              disabled={isLoading} 
              className="w-full bg-gradient-to-r from-primary-950 to-primary-500 hover:from-primary-500 hover:to-primary-950 text-white font-bold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-105"
            >
              {isLoading ? '🔄 Đang đăng nhập...' : '🚀 Đăng nhập'}
            </Button>
          </div>

          <div className="text-center">
            <Link
              href="/"
              className="font-medium text-accent-500 hover:text-accent-400 transition-colors"
            >
              ← Quay lại trang chủ
            </Link>
          </div>
        </form>
      </GlassCard>
    </div>
  );
};
