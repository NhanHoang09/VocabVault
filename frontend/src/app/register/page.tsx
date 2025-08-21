import { RegisterForm } from '@/features/auth';
import { PublicRoute } from '@/components/auth';
import { AnimatedBackground, FloatingElements } from '@/components/ui';

export default function RegisterPage() {
  return (
    <PublicRoute>
      <div className="min-h-screen relative overflow-hidden">
        <AnimatedBackground />
        <FloatingElements />
        <div className="relative z-20">
          <RegisterForm />
        </div>
      </div>
    </PublicRoute>
  );
}
