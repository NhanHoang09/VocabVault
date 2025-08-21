import Link from 'next/link';

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">VV</span>
              </div>
              <h1 className="text-xl font-bold text-gray-900">
                VocabVault Demo
              </h1>
            </div>
            <Link
              href="/"
              className="text-gray-600 hover:text-gray-900 transition-colors"
            >
              ← Quay lại trang chủ
            </Link>
          </div>
        </div>
      </header>

      {/* Demo Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Trải nghiệm VocabVault
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Khám phá các tính năng mạnh mẽ của ứng dụng học từ vựng thông minh
          </p>
        </div>

        {/* Demo Features */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {/* Flashcard Demo */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Flashcard Tương tác
            </h3>
            <p className="text-gray-600 mb-4">
              Học từ vựng qua flashcard với hình ảnh, âm thanh và ví dụ thực tế.
            </p>
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-2">
                  Serendipity
                </div>
                <div className="text-sm text-gray-600 mb-2">
                  /ˌserənˈdɪpəti/
                </div>
                <div className="text-gray-700">Sự tình cờ may mắn</div>
              </div>
            </div>
            <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors">
              Thử ngay
            </button>
          </div>

          {/* AI Learning Demo */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-purple-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              AI Thông minh
            </h3>
            <p className="text-gray-600 mb-4">
              Hệ thống AI phân tích và điều chỉnh nội dung học tập phù hợp với
              bạn.
            </p>
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="text-sm text-gray-600 mb-2">
                AI đang phân tích...
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Độ khó phù hợp:</span>
                  <span className="text-green-600">85%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Tần suất ôn tập:</span>
                  <span className="text-blue-600">Tối ưu</span>
                </div>
              </div>
            </div>
            <button className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition-colors">
              Khám phá AI
            </button>
          </div>

          {/* Progress Tracking Demo */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Theo dõi Tiến độ
            </h3>
            <p className="text-gray-600 mb-4">
              Xem thống kê chi tiết về quá trình học tập và cải thiện hiệu quả.
            </p>
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span>Từ đã học:</span>
                  <span className="font-semibold">1,247</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Chuỗi ngày:</span>
                  <span className="font-semibold text-green-600">15 ngày</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full"
                    style={{ width: '75%' }}
                  ></div>
                </div>
              </div>
            </div>
            <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors">
              Xem thống kê
            </button>
          </div>
        </div>

        {/* CTA Section */}
        <div className="text-center bg-white rounded-xl shadow-lg p-8 border border-gray-100">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Sẵn sàng bắt đầu?
          </h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Tạo tài khoản miễn phí và bắt đầu hành trình học từ vựng thông minh
            ngay hôm nay!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg font-semibold hover:shadow-lg transition-all duration-200 transform hover:scale-105"
            >
              Đăng ký miễn phí
            </Link>
            <Link
              href="/login"
              className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-lg font-semibold hover:border-gray-400 transition-colors"
            >
              Đăng nhập
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
