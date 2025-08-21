import React, { useState } from 'react';
import Button from '@/components/ui/Button';
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from '@/components/ui/data-display';
import { useToastNotification } from '@/hooks/useToastNotification';
// import { api } from '@/lib/api';

export const ErrorHandlingExample: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const toast = useToastNotification();

  const testSuccessToast = () => {
    toast.success('This is a success message!');
  };

  const testErrorToast = () => {
    toast.error('This is an error message!');
  };

  const testWarningToast = () => {
    toast.warning('This is a warning message!');
  };

  const testInfoToast = () => {
    toast.info('This is an info message!');
  };

  const testApiError = async () => {
    setLoading(true);
    try {
      // await api.get('/api/nonexistent-endpoint');
      console.log('API error test - endpoint not found');
    } catch (error) {
      // Error toast will be shown automatically by middleware
      console.log('API error caught:', error);
    } finally {
      setLoading(false);
    }
  };

  const testApiErrorWithSkipToast = async () => {
    setLoading(true);
    try {
      // await api.get('/api/nonexistent-endpoint', { skipToast: true });
      console.log('API error test with skip toast');
    } catch (error) {
      // No toast will be shown
      console.log('API error caught (no toast):', error);
    } finally {
      setLoading(false);
    }
  };

  const testValidationError = async () => {
    setLoading(true);
    try {
      // await api.post('/api/validation-test', { invalid: 'data' });
      console.log('Validation error test');
    } catch (error) {
      // Validation error toast will be shown automatically
      console.log('Validation error caught:', error);
    } finally {
      setLoading(false);
    }
  };

  const testNetworkError = async () => {
    setLoading(true);
    try {
      // await api.get('http://invalid-url-that-does-not-exist.com');
      console.log('Network error test');
    } catch (error) {
      // Network error toast will be shown automatically
      console.log('Network error caught:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Toast Notification Examples</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Button onClick={testSuccessToast} variant="primary">
              Success Toast
            </Button>
            <Button onClick={testErrorToast} variant="outline">
              Error Toast
            </Button>
            <Button onClick={testWarningToast} variant="outline">
              Warning Toast
            </Button>
            <Button onClick={testInfoToast} variant="outline">
              Info Toast
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>API Error Handling Examples</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 gap-4">
            <Button
              onClick={testApiError}
              disabled={loading}
              className="w-full"
            >
              {loading ? 'Testing...' : 'Test API Error (404)'}
            </Button>

            <Button
              onClick={testApiErrorWithSkipToast}
              disabled={loading}
              variant="outline"
              className="w-full"
            >
              {loading ? 'Testing...' : 'Test API Error (Skip Toast)'}
            </Button>

            <Button
              onClick={testValidationError}
              disabled={loading}
              variant="outline"
              className="w-full"
            >
              {loading ? 'Testing...' : 'Test Validation Error (400)'}
            </Button>

            <Button
              onClick={testNetworkError}
              disabled={loading}
              variant="outline"
              className="w-full"
            >
              {loading ? 'Testing...' : 'Test Network Error'}
            </Button>
          </div>

          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <h4 className="font-medium mb-2">How it works:</h4>
            <ul className="text-sm space-y-1 text-gray-600">
              <li>• API errors are automatically caught by middleware</li>
              <li>• Toast notifications are shown with appropriate messages</li>
              <li>
                • Use <code>skipToast: true</code> to disable automatic toasts
              </li>
              <li>• Different error types show different toast styles</li>
              <li>
                • Network errors, validation errors, and server errors are
                handled
              </li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
