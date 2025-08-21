'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/constants';
import Button from '@/components/ui/Button';

interface HeaderProps {
  variant?: 'default' | 'transparent';
  showAuth?: boolean;
}

const Header: React.FC<HeaderProps> = ({
  variant = 'default',
  showAuth = true,
}) => {
  const { user, isAuthenticated, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const headerClasses =
    variant === 'transparent'
      ? 'bg-transparent'
      : 'bg-white/80 backdrop-blur-sm border-b border-gray-200';

  return (
    <header className={`${headerClasses} sticky top-0 z-40`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link href={ROUTES.HOME} className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">VV</span>
            </div>
            <h1 className="text-xl font-bold text-gray-900">VocabVault</h1>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {isAuthenticated ? (
              <>
                <Link
                  href={ROUTES.DASHBOARD}
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  href={ROUTES.STUDY}
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Học tập
                </Link>
                <Link
                  href={ROUTES.VOCABULARY}
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Từ vựng
                </Link>
                <Link
                  href={ROUTES.PROGRESS}
                  className="text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Tiến độ
                </Link>

                {/* User Menu */}
                <div className="relative group">
                  <button className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold text-sm">
                        {user?.firstName?.[0] || 'U'}
                      </span>
                    </div>
                    <span className="hidden lg:block">{user?.firstName}</span>
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>

                  {/* Dropdown Menu */}
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                    <div className="py-2">
                      <Link
                        href={ROUTES.PROFILE}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Hồ sơ
                      </Link>
                      <Link
                        href={ROUTES.SETTINGS}
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Cài đặt
                      </Link>
                      <hr className="my-2" />
                      <button
                        onClick={logout}
                        className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                      >
                        Đăng xuất
                      </button>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              showAuth && (
                <div className="flex items-center space-x-4">
                  <Link href={ROUTES.LOGIN}>
                    <Button variant="ghost" size="sm">
                      Đăng nhập
                    </Button>
                  </Link>
                  <Link href={ROUTES.REGISTER}>
                    <Button variant="primary" size="sm">
                      Đăng ký
                    </Button>
                  </Link>
                </div>
              )
            )}
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 text-gray-600 hover:text-gray-900"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            {isAuthenticated ? (
              <div className="space-y-4">
                <Link
                  href={ROUTES.DASHBOARD}
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
                <Link
                  href={ROUTES.STUDY}
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Học tập
                </Link>
                <Link
                  href={ROUTES.VOCABULARY}
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Từ vựng
                </Link>
                <Link
                  href={ROUTES.PROGRESS}
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Tiến độ
                </Link>
                <hr className="my-4" />
                <Link
                  href={ROUTES.PROFILE}
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Hồ sơ
                </Link>
                <Link
                  href={ROUTES.SETTINGS}
                  className="block text-gray-600 hover:text-gray-900"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Cài đặt
                </Link>
                <button
                  onClick={() => {
                    logout();
                    setIsMobileMenuOpen(false);
                  }}
                  className="block w-full text-left text-red-600 hover:text-red-700"
                >
                  Đăng xuất
                </button>
              </div>
            ) : (
              showAuth && (
                <div className="space-y-4">
                  <Link
                    href={ROUTES.LOGIN}
                    className="block text-gray-600 hover:text-gray-900"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Đăng nhập
                  </Link>
                  <Link
                    href={ROUTES.REGISTER}
                    className="block text-gray-600 hover:text-gray-900"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Đăng ký
                  </Link>
                </div>
              )
            )}
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
