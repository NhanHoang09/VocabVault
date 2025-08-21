'use client';

import React from 'react';

const FloatingElements: React.FC = () => {
  const elements = [
    { emoji: '🌟', delay: 0, duration: 3, left: 10, top: 20 },
    { emoji: '💫', delay: 0.5, duration: 4, left: 80, top: 15 },
    { emoji: '✨', delay: 1, duration: 3.5, left: 60, top: 80 },
    { emoji: '🎈', delay: 1.5, duration: 4.5, left: 25, top: 60 },
    { emoji: '🎪', delay: 2, duration: 3, left: 75, top: 40 },
    { emoji: '🎨', delay: 2.5, duration: 4, left: 40, top: 10 },
    { emoji: '🎭', delay: 3, duration: 3.5, left: 90, top: 70 },
    { emoji: '🌈', delay: 3.5, duration: 4.5, left: 15, top: 85 },
  ];

  return (
    <div className="fixed inset-0 pointer-events-none z-10 overflow-hidden">
      {elements.map((element, index) => (
        <div
          key={index}
          className="absolute text-4xl animate-bounce"
          style={{
            left: `${element.left}%`,
            top: `${element.top}%`,
            animationDelay: `${element.delay}s`,
            animationDuration: `${element.duration}s`,
            opacity: 0.3,
          }}
        >
          {element.emoji}
        </div>
      ))}
    </div>
  );
};

export default FloatingElements;
