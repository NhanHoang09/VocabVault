import React from 'react';
import { useFormContext } from 'react-hook-form';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  name: string;
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ name, label, error, className, ...props }, ref) => {
    const { register, formState } = useFormContext();
    const fieldError = formState.errors[name]?.message as string;
    const hasError = !!error || !!fieldError;

    return (
      <div className="space-y-2">
        {label && (
          <label
            htmlFor={name}
            className="block text-sm font-medium text-gray-700"
          >
            {label}
          </label>
        )}
        <input
          {...register(name)}
          {...props}
          ref={ref}
          className={cn(
            'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
            hasError && 'border-red-500 focus-visible:ring-red-500',
            className
          )}
        />
        {(error || fieldError) && (
          <p className="text-sm text-red-600">{error || fieldError}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
