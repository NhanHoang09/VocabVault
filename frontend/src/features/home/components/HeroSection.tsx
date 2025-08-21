import Link from 'next/link';
import { GradientText, GlassCard } from '@/components/ui';

export const HeroSection: React.FC = () => {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
      <div className="text-center relative">
        {/* Animated emoji */}
        <div className="absolute -top-10 left-1/2 transform -translate-x-1/2 text-8xl animate-bounce">
          🚀
        </div>
        
        <GlassCard className="p-12 mb-8">
          <h1 className="text-5xl md:text-7xl font-black mb-6 leading-tight">
            <GradientText gradient="from-primary-950 via-primary-500 to-secondary-500">
              Học từ vựng
            </GradientText>
            <br />
            <span className="text-white">
              thông minh
            </span>
            <span className="text-6xl ml-4 animate-pulse">✨</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-4xl mx-auto leading-relaxed">
            VocabVault giúp bạn học từ vựng hiệu quả với{' '}
            <GradientText gradient="from-accent-500 to-secondary-500">
              AI thông minh
            </GradientText>
            , hệ thống flashcard tương tác và theo dõi tiến độ chi tiết.
          </p>

          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-8">
            <Link
              href="/register"
              className="group relative bg-gradient-to-r from-primary-950 to-primary-500 text-white px-10 py-5 rounded-2xl font-bold text-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-110 hover:rotate-1"
            >
              <span className="relative z-10">🎯 Bắt đầu miễn phí</span>
              <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-primary-950 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </Link>
            
            <Link
              href="/preview"
              className="group bg-white/20 backdrop-blur-md border-2 border-white/30 text-white px-10 py-5 rounded-2xl font-bold text-lg hover:bg-white/30 transition-all duration-300 transform hover:scale-105"
            >
              👀 Xem preview
            </Link>
          </div>
        </GlassCard>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <GlassCard className="p-6 text-center">
            <div className="text-4xl mb-2">🎓</div>
            <div className="text-2xl font-bold text-white mb-2">10,000+</div>
            <div className="text-white/80">Học viên đã tham gia</div>
          </GlassCard>
          
          <GlassCard className="p-6 text-center">
            <div className="text-4xl mb-2">📚</div>
            <div className="text-2xl font-bold text-white mb-2">50,000+</div>
            <div className="text-white/80">Từ vựng đã học</div>
          </GlassCard>
          
          <GlassCard className="p-6 text-center">
            <div className="text-4xl mb-2">⭐</div>
            <div className="text-2xl font-bold text-white mb-2">4.9/5</div>
            <div className="text-white/80">Đánh giá từ người dùng</div>
          </GlassCard>
        </div>
      </div>
    </main>
  );
};
