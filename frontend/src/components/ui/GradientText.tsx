'use client';

import React from 'react';

interface GradientTextProps {
  children: React.ReactNode;
  className?: string;
  gradient?: string;
}

const GradientText: React.FC<GradientTextProps> = ({ 
  children, 
  className = '',
  gradient = 'from-pink-500 via-purple-500 to-indigo-500'
}) => {
  return (
    <span className={`bg-gradient-to-r ${gradient} bg-clip-text text-transparent ${className}`}>
      {children}
    </span>
  );
};

export default GradientText;
