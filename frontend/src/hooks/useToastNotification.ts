import { useToast } from '@/components/providers/ToastProvider';

export const useToastNotification = () => {
  const { showToast } = useToast();

  const success = (message: string, duration = 3000) => {
    showToast({
      message,
      type: 'success',
      duration,
    });
  };

  const error = (message: string, duration = 5000) => {
    showToast({
      message,
      type: 'error',
      duration,
    });
  };

  const warning = (message: string, duration = 4000) => {
    showToast({
      message,
      type: 'warning',
      duration,
    });
  };

  const info = (message: string, duration = 3000) => {
    showToast({
      message,
      type: 'info',
      duration,
    });
  };

  return {
    success,
    error,
    warning,
    info,
  };
};
