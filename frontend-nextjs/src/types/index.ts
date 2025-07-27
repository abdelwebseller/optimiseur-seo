// Types pour l'application Optimiseur SEO

export interface SitemapAnalysis {
  id: string;
  sitemapUrl: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: number;
  createdAt: Date;
  completedAt?: Date;
  error?: string;
}

export interface InternalLinkSuggestion {
  id: string;
  sourcePage: string;
  anchor: string;
  targetPage: string;
  similarityScore: number;
  status: 'pending' | 'approved' | 'rejected';
  createdAt: Date;
}

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  company?: string;
  createdAt: Date;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface AnalysisSettings {
  similarityThreshold: number;
  maxSuggestions: number;
  openaiModel: string;
  customParameters?: Record<string, unknown>;
}

export interface DashboardStats {
  totalAnalyses: number;
  completedAnalyses: number;
  totalSuggestions: number;
  approvedSuggestions: number;
  averageSimilarityScore: number;
}

// Types pour les formulaires
export interface LoginForm {
  email: string;
  password: string;
  rememberMe: boolean;
}

export interface SignupForm {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  company?: string;
  acceptTerms: boolean;
  acceptNewsletter: boolean;
}

export interface SitemapForm {
  sitemapUrl: string;
  customParameters?: string;
}

// Types pour les filtres
export interface ResultsFilter {
  search: string;
  status: 'all' | 'pending' | 'approved' | 'rejected';
  minScore: number;
  maxScore: number;
  dateRange?: {
    start: Date;
    end: Date;
  };
}

// Types pour les notifications
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
} 