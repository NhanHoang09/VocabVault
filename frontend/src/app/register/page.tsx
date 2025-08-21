import Link from 'next/link';

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
      <div className="max-w-md w-full mx-4">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-white font-bold text-lg">VV</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">Đăng ký</h1>
            <p className="text-gray-600 mt-2">
              Tạo tài khoản mới để bắt đầu học từ vựng
            </p>
          </div>

          <form className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="firstName"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Họ
                </label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Họ"
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="lastName"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Tên
                </label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Tên"
                  required
                />
              </div>
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="your@email.com"
                required
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Mật khẩu
              </label>
              <input
                type="password"
                id="password"
                name="password"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
                required
              />
            </div>

            <div>
              <label
                htmlFor="confirmPassword"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Xác nhận mật khẩu
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="••••••••"
                required
              />
            </div>

            <div>
              <label
                htmlFor="language"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Ngôn ngữ mục tiêu
              </label>
              <select
                id="language"
                name="language"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Chọn ngôn ngữ</option>
                <option value="en">Tiếng Anh</option>
                <option value="ja">Tiếng Nhật</option>
                <option value="ko">Tiếng Hàn</option>
                <option value="zh">Tiếng Trung</option>
                <option value="fr">Tiếng Pháp</option>
                <option value="de">Tiếng Đức</option>
                <option value="es">Tiếng Tây Ban Nha</option>
              </select>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="terms"
                name="terms"
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                required
              />
              <label htmlFor="terms" className="ml-2 text-sm text-gray-600">
                Tôi đồng ý với{' '}
                <Link
                  href="/terms"
                  className="text-blue-600 hover:text-blue-500"
                >
                  Điều khoản sử dụng
                </Link>{' '}
                và{' '}
                <Link
                  href="/privacy"
                  className="text-blue-600 hover:text-blue-500"
                >
                  Chính sách bảo mật
                </Link>
              </label>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-2 px-4 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              Tạo tài khoản
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Đã có tài khoản?{' '}
              <Link
                href="/login"
                className="text-blue-600 hover:text-blue-500 font-medium"
              >
                Đăng nhập
              </Link>
            </p>
          </div>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Hoặc</span>
              </div>
            </div>

            <div className="mt-6">
              <button
                type="button"
                className="w-full flex justify-center items-center px-4 py-2 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
              >
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                Đăng ký với Google
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
