# Vocabulary Vault Frontend

A modern, feature-rich vocabulary learning application built with Next.js, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Modern Tech Stack**: Next.js 15, TypeScript, Tailwind CSS
- **UI Components**: Radix UI primitives with custom styling
- **State Management**: Zustand for lightweight state management
- **Form Handling**: React Hook Form with Zod validation
- **API Integration**: Axios with interceptors and error handling
- **Testing**: Jest and React Testing Library
- **Code Quality**: ESLint, Prettier, and Husky hooks
- **Bundle Analysis**: Webpack bundle analyzer
- **Animations**: Framer Motion and CSS animations

## 📦 Dependencies

### Core Dependencies

- **Next.js 15.5.0** - React framework
- **React 19.1.0** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework

### UI & Components

- **Radix UI** - Accessible component primitives
- **Lucide React** - Icon library
- **Class Variance Authority** - Component variant management
- **Tailwind Merge** - Class name merging utility

### State & Data

- **Zustand** - State management
- **React Query** - Server state management
- **Axios** - HTTP client
- **React Hook Form** - Form handling
- **Zod** - Schema validation

### Utilities

- **Day.js** - Date manipulation
- **React Spring** - Animation library
- **React Hot Toast** - Toast notifications

### Development Tools

- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Jest** - Testing framework
- **Husky** - Git hooks
- **Lint Staged** - Pre-commit hooks

## 🛠️ Setup

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Set up environment variables**:

   ```bash
   cp .env.example .env.local
   ```

   Update the values in `.env.local` with your configuration.

3. **Start development server**:

   ```bash
   npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📜 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Run TypeScript type checking
- `npm run code-quality` - Run all quality checks
- `npm run fix-all` - Fix all code issues
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Run tests with coverage
- `npm run analyze` - Analyze bundle size

## 🏗️ Project Structure

```
src/
├── app/                 # Next.js App Router pages
├── components/          # Reusable UI components
│   ├── ui/             # Base UI components
│   └── forms/          # Form components
├── lib/                # Utility functions and configurations
│   ├── api.ts          # API client configuration
│   ├── store.ts        # Zustand stores
│   └── utils.ts        # Utility functions
├── hooks/              # Custom React hooks
├── types/              # TypeScript type definitions
└── styles/             # Global styles and CSS modules
```

## 🎨 Styling

The project uses Tailwind CSS with a custom design system:

- **Color System**: CSS custom properties for theming
- **Typography**: Custom font families and sizing
- **Spacing**: Consistent spacing scale
- **Animations**: Custom keyframes and transitions
- **Components**: Radix UI primitives with Tailwind styling

## 🔧 Configuration Files

- **`next.config.ts`** - Next.js configuration
- **`tailwind.config.ts`** - Tailwind CSS configuration
- **`.eslintrc.json`** - ESLint rules
- **`.prettierrc`** - Prettier formatting rules
- **`jest.config.js`** - Jest testing configuration
- **`tsconfig.json`** - TypeScript configuration

## 🧪 Testing

The project includes comprehensive testing setup:

- **Unit Tests**: Jest with React Testing Library
- **Component Tests**: Isolated component testing
- **Integration Tests**: API integration testing
- **Mocking**: Next.js router and API mocks

## 📱 Features

### Authentication

- JWT-based authentication
- Persistent login state
- Protected routes
- Auto-logout on token expiry

### Vocabulary Management

- Add, edit, and delete vocabulary
- Categorization and tagging
- Search and filtering
- Import/export functionality

### Learning Features

- Flashcard system
- Spaced repetition
- Progress tracking
- Study sessions

### Analytics

- Learning statistics
- Progress visualization
- Performance metrics
- Study insights

### Gamification

- Achievement system
- Leaderboards
- Streaks and badges
- Points and levels

### AI Integration

- Smart suggestions
- Context explanations
- Adaptive learning
- Personalized content

## 🚀 Deployment

The application can be deployed to various platforms:

- **Vercel** (recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Docker containers**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `npm run code-quality`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
