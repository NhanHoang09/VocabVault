import Link from 'next/link';

interface DemoHeaderProps {
  title?: string;
}

export const DemoHeader: React.FC<DemoHeaderProps> = ({ title = 'VocabVault Preview' }) => {
  return (
    <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">VV</span>
            </div>
            <h1 className="text-xl font-bold text-gray-900">
              {title}
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
  );
};
