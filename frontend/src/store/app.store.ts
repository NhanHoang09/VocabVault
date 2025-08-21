import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  username: string;
  avatar?: string;
}

interface AppState {
  // User state
  user: User | null;
  isAuthenticated: boolean;

  // UI state
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  loading: boolean;

  // Study state
  currentStudySession: any | null;
  studyProgress: Record<string, any>;

  // Actions
  setUser: (user: User | null) => void;
  setAuthenticated: (isAuthenticated: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
  toggleSidebar: () => void;
  setLoading: (loading: boolean) => void;
  setCurrentStudySession: (session: any | null) => void;
  updateStudyProgress: (key: string, progress: any) => void;
  logout: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      theme: 'light',
      sidebarOpen: false,
      loading: false,
      currentStudySession: null,
      studyProgress: {},

      // Actions
      setUser: user => set({ user, isAuthenticated: !!user }),

      setAuthenticated: isAuthenticated => set({ isAuthenticated }),

      setTheme: theme => set({ theme }),

      toggleSidebar: () => set(state => ({ sidebarOpen: !state.sidebarOpen })),

      setLoading: loading => set({ loading }),

      setCurrentStudySession: session => set({ currentStudySession: session }),

      updateStudyProgress: (key, progress) =>
        set(state => ({
          studyProgress: {
            ...state.studyProgress,
            [key]: progress,
          },
        })),

      logout: () =>
        set({
          user: null,
          isAuthenticated: false,
          currentStudySession: null,
          studyProgress: {},
        }),
    }),
    {
      name: 'app-storage',
      partialize: state => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        theme: state.theme,
        studyProgress: state.studyProgress,
      }),
    }
  )
);
