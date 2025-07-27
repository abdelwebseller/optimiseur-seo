"use client";

import { useState, useCallback } from 'react';
import { Notification } from '@/types';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface UseNotificationReturn {
  notifications: Notification[];
  addNotification: (type: NotificationType, title: string, message: string) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

export const useNotification = (): UseNotificationReturn => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  }, []);

  const addNotification = useCallback((type: NotificationType, title: string, message: string) => {
    const newNotification: Notification = {
      id: Date.now().toString(),
      type,
      title,
      message,
      timestamp: new Date(),
      read: false,
    };

    setNotifications(prev => [newNotification, ...prev]);

    // Auto-remove success and info notifications after 5 seconds
    if (type === 'success' || type === 'info') {
      setTimeout(() => {
        removeNotification(newNotification.id);
      }, 5000);
    }
  }, [removeNotification]);

  const clearNotifications = useCallback(() => {
    setNotifications([]);
  }, []);

  return {
    notifications,
    addNotification,
    removeNotification,
    clearNotifications,
  };
};

// Hook pour les notifications de succès
export const useSuccessNotification = () => {
  const { addNotification } = useNotification();
  
  return useCallback((message: string) => {
    addNotification('success', 'Succès', message);
  }, [addNotification]);
};

// Hook pour les notifications d'erreur
export const useErrorNotification = () => {
  const { addNotification } = useNotification();
  
  return useCallback((message: string) => {
    addNotification('error', 'Erreur', message);
  }, [addNotification]);
};

// Hook pour les notifications d'avertissement
export const useWarningNotification = () => {
  const { addNotification } = useNotification();
  
  return useCallback((message: string) => {
    addNotification('warning', 'Attention', message);
  }, [addNotification]);
};

// Hook pour les notifications d'information
export const useInfoNotification = () => {
  const { addNotification } = useNotification();
  
  return useCallback((message: string) => {
    addNotification('info', 'Information', message);
  }, [addNotification]);
}; 