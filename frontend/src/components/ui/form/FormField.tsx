import React from 'react';
import { useFormContext } from 'react-hook-form';
import { cn } from '@/lib/utils';

interface FormFieldProps {
  name: string;
  label?: string;
  error?: string;
  children: React.ReactNode;
  className?: string;
}

export const FormField: React.FC<FormFieldProps> = ({
  name,
  label,
  error,
  children,
  className,
}) => {
  const { formState } = useFormContext();
  const fieldError = formState.errors[name]?.message as string;

  return (
    <div className={cn('space-y-2', className)}>
      {label && (
        <label
          htmlFor={name}
          className="block text-sm font-medium text-gray-700"
        >
          {label}
        </label>
      )}
      {children}
      {(error || fieldError) && (
        <p className="text-sm text-red-600">{error || fieldError}</p>
      )}
    </div>
  );
};
