'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import Link from 'next/link';
import Button from '@/components/ui/Button';
// import { registerSchema, type RegisterFormData } from '../schemas/auth.schema';
// import { useAuthStore } from '../store/auth.store';
// import { useToastNotification } from '@/hooks/useToastNotification';

// Temporary type for testing
interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export const RegisterForm: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  // const { register: registerUser } = useAuthStore();
  // const toast = useToastNotification();

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<RegisterFormData>({
    // resolver: zodResolver(registerSchema),
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    try {
      // await registerUser({
      //   email: data.email,
      //   password: data.password,
      //   username: data.username,
      // });
      console.log('Register data:', data);
      // Success toast will be shown by auth store
    } catch (error) {
      // Error toast will be shown by middleware
      console.error('Registration error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="mx-auto h-12 w-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-lg">VV</span>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Tạo tài khoản mới
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Hoặc{' '}
            <Link
              href="/login"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              đăng nhập nếu đã có tài khoản
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          <div className="space-y-4">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Tên người dùng
              </label>
              <input
                {...register('username')}
                type="text"
                id="username"
                placeholder="Nhập tên người dùng"
                autoComplete="username"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {errors.username && (
                <p className="text-sm text-red-600 mt-1">
                  {errors.username.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Email
              </label>
              <input
                {...register('email')}
                type="email"
                id="email"
                placeholder="Nhập email của bạn"
                autoComplete="email"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {errors.email && (
                <p className="text-sm text-red-600 mt-1">
                  {errors.email.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Mật khẩu
              </label>
              <input
                {...register('password')}
                type="password"
                id="password"
                placeholder="Nhập mật khẩu"
                autoComplete="new-password"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {errors.password && (
                <p className="text-sm text-red-600 mt-1">
                  {errors.password.message}
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Xác nhận mật khẩu
              </label>
              <input
                {...register('confirmPassword')}
                type="password"
                id="confirmPassword"
                placeholder="Nhập lại mật khẩu"
                autoComplete="new-password"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              {errors.confirmPassword && (
                <p className="text-sm text-red-600 mt-1">
                  {errors.confirmPassword.message}
                </p>
              )}
            </div>
          </div>

          {/* Password strength indicator */}
          {password && (
            <div className="space-y-2">
              <p className="text-sm text-gray-600">Độ mạnh mật khẩu:</p>
              <div className="flex space-x-1">
                <div
                  className={`h-2 flex-1 rounded ${
                    password.length >= 8 ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
                <div
                  className={`h-2 flex-1 rounded ${
                    /[A-Z]/.test(password) ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
                <div
                  className={`h-2 flex-1 rounded ${
                    /[a-z]/.test(password) ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
                <div
                  className={`h-2 flex-1 rounded ${
                    /\d/.test(password) ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
                <div
                  className={`h-2 flex-1 rounded ${
                    /[@$!%*?&]/.test(password) ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
              </div>
              <p className="text-xs text-gray-500">
                Mật khẩu phải có ít nhất 8 ký tự, bao gồm chữ hoa, chữ thường,
                số và ký tự đặc biệt
              </p>
            </div>
          )}

          <div className="flex items-center">
            <input
              id="agree-terms"
              name="agree-terms"
              type="checkbox"
              required
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label
              htmlFor="agree-terms"
              className="ml-2 block text-sm text-gray-900"
            >
              Tôi đồng ý với{' '}
              <Link
                href="/terms"
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                điều khoản sử dụng
              </Link>{' '}
              và{' '}
              <Link
                href="/privacy"
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                chính sách bảo mật
              </Link>
            </label>
          </div>

          <div>
            <Button type="submit" disabled={isLoading} className="w-full">
              {isLoading ? 'Đang tạo tài khoản...' : 'Tạo tài khoản'}
            </Button>
          </div>

          <div className="text-center">
            <Link
              href="/"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              ← Quay lại trang chủ
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};
