export const colors = {
  // Primary colors
  primary: {
    50: '#E0F7FA',   // Background
    100: '#B2EBF2',
    200: '#80DEEA',
    300: '#4DD0E1',
    400: '#26C6DA',
    500: '#00B4D8',  // Secondary
    600: '#00ACC1',
    700: '#0097A7',
    800: '#00838F',
    900: '#006064',
    950: '#0077B6',  // Primary
  },
  
  // Text colors
  text: {
    primary: '#023E8A',    // Text chính
    secondary: '#555555',  // Text phụ
    light: '#FFFFFF',      // Text trên nền tối
    muted: '#6B7280',      // Text mờ
  },
  
  // Background colors
  background: {
    primary: '#E0F7FA',    // Background chính
    secondary: '#FFFFFF',  // Surface
    dark: '#023E8A',       // Background tối
  },
  
  // Status colors
  status: {
    success: '#4CAF50',    // Success
    danger: '#FF6B6B',     // Danger / Alert
    warning: '#FF9800',    // Warning
    info: '#00B4D8',       // Info
  },
  
  // Accent colors
  accent: {
    primary: '#90E0EF',    // Accent chính
    secondary: '#00B4D8',  // Accent phụ
    light: '#E0F7FA',      // Accent nhạt
  },
  
  // Semantic colors
  semantic: {
    primary: '#0077B6',    // Primary
    secondary: '#00B4D8',  // Secondary
    accent: '#90E0EF',     // Accent
    background: '#E0F7FA', // Background
    surface: '#FFFFFF',    // Surface
    textPrimary: '#023E8A', // Text chính
    textSecondary: '#555555', // Text phụ
    danger: '#FF6B6B',     // Danger
    success: '#4CAF50',    // Success
  }
} as const;

export type ColorScheme = typeof colors;
