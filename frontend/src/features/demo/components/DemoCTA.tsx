import Link from 'next/link';

export const DemoCTA: React.FC = () => {
  return (
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
  );
};
