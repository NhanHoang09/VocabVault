'use client';

import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  blur?: 'sm' | 'md' | 'lg';
}

const GlassCard: React.FC<GlassCardProps> = ({ 
  children, 
  className = '',
  blur = 'md'
}) => {
  const blurClasses = {
    sm: 'backdrop-blur-sm',
    md: 'backdrop-blur-md',
    lg: 'backdrop-blur-lg',
  };

  return (
    <div className={`
      bg-white/10 
      ${blurClasses[blur]}
      border border-white/20 
      rounded-2xl 
      shadow-2xl 
      backdrop-saturate-150
      ${className}
    `}>
      {children}
    </div>
  );
};

export default GlassCard;
