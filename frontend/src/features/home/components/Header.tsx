import Link from 'next/link';
import { GradientText, GlassCard } from '@/components/ui';

export const Header: React.FC = () => {
  return (
    <header className="relative z-30">
      <GlassCard className="mx-4 mt-4 mb-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3 group">
              <div className="w-12 h-12 bg-gradient-to-r from-primary-950 to-primary-500 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300">
                <span className="text-white font-black text-lg">🎯</span>
              </div>
              <h1 className="text-2xl font-black">
                <GradientText gradient="from-primary-950 to-primary-500">
                  VocabVault
                </GradientText>
              </h1>
            </div>
            
            <nav className="hidden md:flex space-x-6">
              <Link
                href="/login"
                className="group relative px-6 py-3 rounded-xl font-semibold text-white/90 hover:text-white transition-all duration-300 hover:bg-white/20"
              >
                <span className="relative z-10">🔐 Đăng nhập</span>
                <div className="absolute inset-0 bg-white/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </Link>
              
              <Link
                href="/register"
                className="group relative bg-gradient-to-r from-primary-950 to-primary-500 px-6 py-3 rounded-xl font-semibold text-white hover:shadow-lg transition-all duration-300 transform hover:scale-105"
              >
                <span className="relative z-10">🚀 Đăng ký</span>
                <div className="absolute inset-0 bg-gradient-to-r from-primary-500 to-primary-950 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </Link>
            </nav>
          </div>
        </div>
      </GlassCard>
    </header>
  );
};
