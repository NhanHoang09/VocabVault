'use client';

import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import Header from '@/components/layout/Header';
import Button from '@/components/ui/Button';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { AnimatedBackground, FloatingElements, GradientText, GlassCard } from '@/components/ui';

const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <ProtectedRoute>
      <div className="min-h-screen relative overflow-hidden">
        <AnimatedBackground />
        <FloatingElements />
        <div className="relative z-20">
          <Header />

          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Welcome Section */}
            <GlassCard className="p-8 mb-8">
              <div className="text-center">
                <div className="text-6xl mb-4 animate-bounce">🎉</div>
                <h1 className="text-4xl font-black mb-4">
                  <GradientText gradient="from-primary-950 to-primary-500">
                    Chào mừng trở lại, {user?.username}!
                  </GradientText>
                </h1>
                <p className="text-xl text-white/90">
                  Đây là trang Dashboard của bạn. Bạn đã đăng nhập thành công! ✨
                </p>
              </div>
            </GlassCard>

            {/* Auth Info Card */}
            <GlassCard className="p-6 mb-8">
              <h2 className="text-xl font-semibold text-white mb-4">
                🔐 Thông tin xác thực
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-white/70">Trạng thái</p>
                  <p className="text-success-500 font-semibold">✅ Đã đăng nhập</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-white/70">Username</p>
                  <p className="text-white font-semibold">{user?.username}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-white/70">Email</p>
                  <p className="text-white font-semibold">{user?.email}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-white/70">User ID</p>
                  <p className="text-white font-semibold">{user?.id}</p>
                </div>
              </div>
            </GlassCard>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <GlassCard className="p-6 hover:scale-105 transition-transform duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-primary-950 to-primary-500 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-white text-xl">📚</span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Học từ vựng
                </h3>
                <p className="text-white/80 text-sm mb-4">
                  Bắt đầu học từ vựng mới hoặc ôn tập
                </p>
                <Button className="w-full bg-gradient-to-r from-primary-950 to-primary-500 text-white">
                  Bắt đầu học
                </Button>
              </GlassCard>

              <GlassCard className="p-6 hover:scale-105 transition-transform duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-success-500 to-secondary-500 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-white text-xl">📊</span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Xem tiến độ
                </h3>
                <p className="text-white/80 text-sm mb-4">
                  Theo dõi tiến độ học tập của bạn
                </p>
                <Button className="w-full bg-gradient-to-r from-success-500 to-secondary-500 text-white">
                  Xem tiến độ
                </Button>
              </GlassCard>

              <GlassCard className="p-6 hover:scale-105 transition-transform duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-accent-500 to-primary-500 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-white text-xl">🏆</span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Thành tích
                </h3>
                <p className="text-white/80 text-sm mb-4">
                  Xem thành tích và huy hiệu
                </p>
                <Button className="w-full bg-gradient-to-r from-accent-500 to-primary-500 text-white">
                  Xem thành tích
                </Button>
              </GlassCard>

              <GlassCard className="p-6 hover:scale-105 transition-transform duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-warning-500 to-danger-500 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-white text-xl">⚙️</span>
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  Cài đặt
                </h3>
                <p className="text-white/80 text-sm mb-4">
                  Tùy chỉnh cài đặt tài khoản
                </p>
                <Button className="w-full bg-gradient-to-r from-warning-500 to-danger-500 text-white">
                  Cài đặt
                </Button>
              </GlassCard>
            </div>

            {/* Test Section */}
            <GlassCard className="p-6">
              <h2 className="text-xl font-semibold text-white mb-4">
                🔍 Thông tin Token (Test)
              </h2>
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-white/70 mb-2">
                    Access Token Status:
                  </p>
                  <div className="bg-white/10 rounded p-3">
                    <p className="text-sm text-white">
                      ✅ Token được lưu trong RAM (Zustand store)
                    </p>
                    <p className="text-sm text-white/80 mt-1">
                      Không thể truy cập từ localStorage (bảo mật cao)
                    </p>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium text-white/70 mb-2">
                    Refresh Token Status:
                  </p>
                  <div className="bg-white/10 rounded p-3">
                    <p className="text-sm text-white">
                      ✅ Token được lưu trong HttpOnly cookie
                    </p>
                    <p className="text-sm text-white/80 mt-1">
                      Không thể truy cập từ JavaScript (chống XSS)
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                     <Button
                     onClick={() => logout()}
                     className="bg-gradient-to-r from-danger-500 to-danger-600 text-white hover:from-danger-600 hover:to-danger-500"
                   >
                     🚪 Đăng xuất
                   </Button>

                   <Button
                     onClick={() => {
                       const { useAuthStore } = require('@/features/auth/store/auth.store');
                       const token = useAuthStore.getState().accessToken;
                       console.log('Access Token:', token ? '✅ Có token' : '❌ Không có token');
                       alert(token ? '✅ Access token có sẵn trong RAM' : '❌ Không có access token');
                     }}
                     className="bg-gradient-to-r from-primary-950 to-primary-500 text-white"
                   >
                     🔍 Kiểm tra Token
                   </Button>

                   <Button
                     onClick={() => {
                       const localToken = localStorage.getItem('access_token');
                       console.log('LocalStorage Token:', localToken);
                       alert(localToken ? '❌ Token có trong localStorage (không an toàn)' : '✅ Token không có trong localStorage (an toàn)');
                     }}
                     className="bg-gradient-to-r from-warning-500 to-warning-600 text-white"
                   >
                     🔒 Kiểm tra localStorage
                   </Button>
                </div>
              </div>
            </GlassCard>
          </main>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;
