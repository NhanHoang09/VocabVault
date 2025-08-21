'use client';

import React, { useEffect, useRef, useState } from 'react';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  color: string;
}

const AnimatedBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animationRef = useRef<number | undefined>(undefined);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isClient) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Create particles with deterministic seed for SSR compatibility
    const particles: Particle[] = [];
    const colors = [
      '#0077B6', // Primary
      '#00B4D8', // Secondary
      '#90E0EF', // Accent
      '#4CAF50', // Success
      '#FF6B6B', // Danger
      '#FF9800', // Warning
    ];

    // Use fixed seed values for consistent rendering
    const seedValues = [
      0.1, 0.3, 0.7, 0.2, 0.9, 0.4, 0.6, 0.8, 0.5, 0.1, 0.3, 0.7, 0.2, 0.9, 0.4,
      0.6, 0.8, 0.5, 0.1, 0.3, 0.7, 0.2, 0.9, 0.4, 0.6, 0.8, 0.5, 0.1, 0.3, 0.7,
      0.2, 0.9, 0.4, 0.6, 0.8, 0.5, 0.1, 0.3, 0.7, 0.2, 0.9, 0.4, 0.6, 0.8, 0.5,
      0.1, 0.3, 0.7, 0.2, 0.9,
    ];

    for (let i = 0; i < 50; i++) {
      const seed1 = seedValues[i % seedValues.length];
      const seed2 = seedValues[(i + 1) % seedValues.length];
      const seed3 = seedValues[(i + 2) % seedValues.length];
      const seed4 = seedValues[(i + 3) % seedValues.length];
      const seed5 = seedValues[(i + 4) % seedValues.length];

      particles.push({
        x: seed1 * canvas.width,
        y: seed2 * canvas.height,
        vx: (seed3 - 0.5) * 0.5,
        vy: (seed4 - 0.5) * 0.5,
        size: seed5 * 3 + 1,
        color: colors[Math.floor(seed1 * colors.length)],
      });
    }
    particlesRef.current = particles;

    // Animation loop
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update and draw particles
      particles.forEach(particle => {
        particle.x += particle.vx;
        particle.y += particle.vy;

        // Bounce off edges
        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

        // Draw particle
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();

        // Draw connections
        particles.forEach(otherParticle => {
          const dx = particle.x - otherParticle.x;
          const dy = particle.y - otherParticle.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(particle.x, particle.y);
            ctx.lineTo(otherParticle.x, otherParticle.y);
            ctx.strokeStyle = `rgba(255, 107, 157, ${0.1 * (1 - distance / 100)})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        });
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isClient]);

  if (!isClient) {
    return (
      <div
        className="fixed inset-0 pointer-events-none z-0"
        style={{
          background: 'linear-gradient(135deg, #0077B6 0%, #00B4D8 100%)',
        }}
      />
    );
  }

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0"
              style={{
          background: 'linear-gradient(135deg, #0077B6 0%, #00B4D8 100%)',
        }}
    />
  );
};

export default AnimatedBackground;
