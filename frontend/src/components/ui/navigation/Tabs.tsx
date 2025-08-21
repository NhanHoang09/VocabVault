import React from 'react';
import { cn } from '@/lib/utils';

interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
  disabled?: boolean;
}

interface TabsProps {
  tabs: Tab[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
  variant?: 'default' | 'pills' | 'underline';
  className?: string;
}

export const Tabs: React.FC<TabsProps> = ({
  tabs,
  activeTab,
  onTabChange,
  variant = 'default',
  className,
}) => {
  const tabListClasses = {
    default: 'flex border-b border-gray-200',
    pills: 'flex space-x-1 bg-gray-100 p-1 rounded-lg',
    underline: 'flex border-b border-gray-200',
  };

  const tabClasses = {
    default:
      'px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:text-gray-700 hover:border-gray-300',
    pills: 'px-3 py-2 text-sm font-medium rounded-md',
    underline:
      'px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:text-gray-700 hover:border-gray-300',
  };

  const activeTabClasses = {
    default: 'border-blue-500 text-blue-600',
    pills: 'bg-white text-gray-900 shadow-sm',
    underline: 'border-blue-500 text-blue-600',
  };

  const disabledTabClasses = 'opacity-50 cursor-not-allowed';

  return (
    <div className={className}>
      <div className={tabListClasses[variant]}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => !tab.disabled && onTabChange(tab.id)}
            className={cn(
              tabClasses[variant],
              activeTab === tab.id && activeTabClasses[variant],
              tab.disabled && disabledTabClasses,
              'transition-colors duration-200'
            )}
            disabled={tab.disabled}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="mt-4">
        {tabs.find(tab => tab.id === activeTab)?.content}
      </div>
    </div>
  );
};
