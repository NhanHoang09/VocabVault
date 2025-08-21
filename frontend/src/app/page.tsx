import { Header, HeroSection, FeaturesGrid, Footer } from '@/features/home';
import { AnimatedBackground, FloatingElements } from '@/components/ui';

export default function Home() {
  return (
    <div className="min-h-screen relative overflow-hidden">
      <AnimatedBackground />
      <FloatingElements />
      <div className="relative z-20">
        <Header />
        <HeroSection />
        <FeaturesGrid />
        <Footer />
      </div>
    </div>
  );
}
