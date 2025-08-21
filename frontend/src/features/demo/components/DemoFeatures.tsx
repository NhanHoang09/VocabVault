import Link from 'next/link';

export const DemoFeatures: React.FC = () => {
  const features = [
    {
      icon: (
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
      ),
      title: 'Flashcard Tương tác',
      description: 'Học từ vựng qua flashcard với hình ảnh, âm thanh và ví dụ thực tế.',
      bgColor: 'bg-blue-100',
      buttonColor: 'bg-blue-600 hover:bg-blue-700',
      buttonText: 'Thử ngay',
      demo: (
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
      ),
    },
    {
      icon: (
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
      ),
      title: 'AI Thông minh',
      description: 'Hệ thống AI phân tích và điều chỉnh nội dung học tập phù hợp với bạn.',
      bgColor: 'bg-purple-100',
      buttonColor: 'bg-purple-600 hover:bg-purple-700',
      buttonText: 'Khám phá AI',
      demo: (
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
      ),
    },
    {
      icon: (
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
      ),
      title: 'Theo dõi Tiến độ',
      description: 'Xem thống kê chi tiết về quá trình học tập và cải thiện hiệu quả.',
      bgColor: 'bg-green-100',
      buttonColor: 'bg-green-600 hover:bg-green-700',
      buttonText: 'Xem thống kê',
      demo: (
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
      ),
    },
  ];

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
      {features.map((feature, index) => (
        <div key={index} className="bg-white rounded-xl shadow-lg p-6 border border-gray-100">
          <div className={`w-12 h-12 ${feature.bgColor} rounded-lg flex items-center justify-center mb-4`}>
            {feature.icon}
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {feature.title}
          </h3>
          <p className="text-gray-600 mb-4">
            {feature.description}
          </p>
          {feature.demo}
          <button className={`w-full ${feature.buttonColor} text-white py-2 rounded-lg transition-colors`}>
            {feature.buttonText}
          </button>
        </div>
      ))}
    </div>
  );
};
