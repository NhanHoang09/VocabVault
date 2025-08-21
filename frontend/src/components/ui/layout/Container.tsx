import React from 'react';
import { cn } from '@/lib/utils';

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

export const Container: React.FC<ContainerProps> = ({
  children,
  className,
  maxWidth = 'lg',
  padding = 'md',
  ...props
}) => {
  const maxWidthClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    full: 'max-w-full',
  };

  const paddingClasses = {
    none: '',
    sm: 'px-4',
    md: 'px-6',
    lg: 'px-8',
  };

  return (
    <div
      className={cn(
        'mx-auto',
        maxWidthClasses[maxWidth],
        paddingClasses[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
