import { ApiResponse, SitemapAnalysis, InternalLinkSuggestion, AnalysisSettings } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    };

    try {
      const response = await fetch(url, defaultOptions);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Une erreur est survenue');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Erreur réseau',
      };
    }
  }

  // Analyser un sitemap
  async processSitemap(sitemapUrl: string, settings?: AnalysisSettings): Promise<ApiResponse<SitemapAnalysis>> {
    return this.request<SitemapAnalysis>('/process-sitemap', {
      method: 'POST',
      body: JSON.stringify({
        sitemap_url: sitemapUrl,
        settings,
      }),
    });
  }

  // Obtenir le statut d'une analyse
  async getAnalysisStatus(analysisId: string): Promise<ApiResponse<SitemapAnalysis>> {
    return this.request<SitemapAnalysis>(`/status/${analysisId}`);
  }

  // Obtenir les résultats d'une analyse
  async getAnalysisResults(analysisId: string): Promise<ApiResponse<InternalLinkSuggestion[]>> {
    return this.request<InternalLinkSuggestion[]>(`/results/${analysisId}`);
  }

  // Exporter les résultats en CSV
  async exportResults(analysisId: string, format: 'csv' | 'json' = 'csv'): Promise<ApiResponse<string>> {
    return this.request<string>(`/download/${analysisId}?format=${format}`);
  }

  // Approuver une suggestion
  async approveSuggestion(suggestionId: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/suggestions/${suggestionId}/approve`, {
      method: 'POST',
    });
  }

  // Rejeter une suggestion
  async rejectSuggestion(suggestionId: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/suggestions/${suggestionId}/reject`, {
      method: 'POST',
    });
  }

  // Obtenir les statistiques du dashboard
  async getDashboardStats(): Promise<ApiResponse<unknown>> {
    return this.request<unknown>('/dashboard/stats');
  }

  // Obtenir l'historique des analyses
  async getAnalysisHistory(): Promise<ApiResponse<SitemapAnalysis[]>> {
    return this.request<SitemapAnalysis[]>('/analyses/history');
  }

  // Sauvegarder les paramètres
  async saveSettings(settings: AnalysisSettings): Promise<ApiResponse<void>> {
    return this.request<void>('/settings', {
      method: 'POST',
      body: JSON.stringify(settings),
    });
  }

  // Obtenir les paramètres
  async getSettings(): Promise<ApiResponse<AnalysisSettings>> {
    return this.request<AnalysisSettings>('/settings');
  }
}

// Instance singleton
export const apiService = new ApiService();

// Fonctions utilitaires pour les appels API
export const api = {
  // Analyser un sitemap
  processSitemap: (sitemapUrl: string, settings?: AnalysisSettings) =>
    apiService.processSitemap(sitemapUrl, settings),

  // Obtenir le statut
  getStatus: (analysisId: string) => apiService.getAnalysisStatus(analysisId),

  // Obtenir les résultats
  getResults: (analysisId: string) => apiService.getAnalysisResults(analysisId),

  // Exporter
  export: (analysisId: string, format: 'csv' | 'json' = 'csv') =>
    apiService.exportResults(analysisId, format),

  // Actions sur les suggestions
  approveSuggestion: (suggestionId: string) => apiService.approveSuggestion(suggestionId),
  rejectSuggestion: (suggestionId: string) => apiService.rejectSuggestion(suggestionId),

  // Dashboard
  getStats: () => apiService.getDashboardStats(),
  getHistory: () => apiService.getAnalysisHistory(),

  // Paramètres
  saveSettings: (settings: AnalysisSettings) => apiService.saveSettings(settings),
  getSettings: () => apiService.getSettings(),
}; 