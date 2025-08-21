import React, { createContext, useContext, useState, useCallback } from 'react';
import { Toast } from '@/components/ui/feedback/Toast';
// import { setToastFunction } from '@/lib/api';

interface ToastNotification {
  id: string;
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
}

interface ToastContextType {
  showToast: (notification: Omit<ToastNotification, 'id'>) => void;
  removeToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

interface ToastProviderProps {
  children: React.ReactNode;
}

export const ToastProvider: React.FC<ToastProviderProps> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastNotification[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const showToast = useCallback(
    (notification: Omit<ToastNotification, 'id'>) => {
      const id = Math.random().toString(36).substr(2, 9);
      const newToast: ToastNotification = {
        id,
        ...notification,
      };

      setToasts(prev => [...prev, newToast]);

      // Auto remove toast after duration
      if (notification.duration !== 0) {
        setTimeout(() => {
          removeToast(id);
        }, notification.duration || 5000);
      }
    },
    [removeToast]
  );

  // Set the toast function for API middleware
  React.useEffect(() => {
    // setToastFunction(showToast);
    console.log('Toast function set');
  }, [showToast]);

  return (
    <ToastContext.Provider value={{ showToast, removeToast }}>
      {children}

      {/* Toast Container */}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            message={toast.message}
            type={toast.type}
            onClose={() => removeToast(toast.id)}
            duration={0} // We handle duration manually
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
};
