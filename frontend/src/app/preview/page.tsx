import { DemoHeader, DemoFeatures, DemoCTA } from '@/features/demo';

export default function PreviewPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <DemoHeader />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Preview VocabVault
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Khám phá các tính năng mạnh mẽ của ứng dụng học từ vựng thông minh
          </p>
        </div>

        <DemoFeatures />
        <DemoCTA />
      </main>
    </div>
  );
}
