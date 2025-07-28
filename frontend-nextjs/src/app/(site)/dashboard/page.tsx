"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [sitemapUrl, setSitemapUrl] = useState("https://example.com/sitemap.xml");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState(0);

  // Rediriger si pas connecté
  if (status === "loading") {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (status === "unauthenticated") {
    router.push("/signin");
    return null;
  }

  const handleAnalysis = async () => {
    setIsAnalyzing(true);
    setProgress(0);

    // Simulation de progression
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsAnalyzing(false);
          router.push("/results");
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-black dark:text-white mb-2">
            Dashboard
          </h1>
          <p className="text-body-color dark:text-body-color-dark">
            Analysez votre sitemap et générez des suggestions de maillage interne
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Nouvelle Analyse */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-black dark:text-white mb-4">
              Nouvelle Analyse
            </h2>
            <p className="text-sm text-body-color dark:text-body-color-dark mb-6">
              Entrez l'URL de votre sitemap XML pour commencer l'analyse
            </p>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  URL du Sitemap
                </label>
                <input
                  type="url"
                  value={sitemapUrl}
                  onChange={(e) => setSitemapUrl(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                  placeholder="https://example.com/sitemap.xml"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-black dark:text-white">
                  Paramètres (optionnel)
                </label>
                <details className="group">
                  <summary className="cursor-pointer text-sm text-primary hover:text-primary/80">
                    Paramètres avancés...
                  </summary>
                  <div className="mt-4 space-y-4">
                    <div>
                      <label className="block text-xs text-body-color dark:text-body-color-dark mb-1">
                        Nombre maximum de pages
                      </label>
                      <input
                        type="number"
                        defaultValue={100}
                        className="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-body-color dark:text-body-color-dark mb-1">
                        Seuil de similarité
                      </label>
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.1"
                        defaultValue={0.7}
                        className="w-full"
                      />
                    </div>
                  </div>
                </details>
              </div>

              <button
                onClick={handleAnalysis}
                disabled={isAnalyzing}
                className="w-full bg-primary text-white py-3 px-6 rounded-md font-semibold hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition duration-300"
              >
                {isAnalyzing ? "Analyse en cours..." : "Lancer l'analyse"}
              </button>
            </div>
          </div>

          {/* Statut de l'Analyse */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-black dark:text-white mb-4">
              Statut de l'Analyse
            </h2>
            <p className="text-sm text-body-color dark:text-body-color-dark mb-6">
              Suivez l'avancement de votre analyse en temps réel
            </p>

            {isAnalyzing ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-body-color dark:text-body-color-dark">
                    Progression
                  </span>
                  <span className="text-sm font-semibold text-primary">
                    {progress}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                <div className="text-xs text-body-color dark:text-body-color-dark">
                  Traitement des pages... ({Math.floor(progress * 0.66)}/100)
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="w-16 h-16 mx-auto mb-4 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <p className="text-sm text-body-color dark:text-body-color-dark">
                  Aucune analyse en cours
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Analyses Récentes */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-black dark:text-white mb-4">
            Analyses Récentes
          </h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-700">
              <div>
                <p className="font-medium text-black dark:text-white">
                  example.com/sitemap.xml
                </p>
                <p className="text-sm text-body-color dark:text-body-color-dark">
                  Analyse terminée il y a 2 heures
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                  Terminé
                </span>
                <button className="text-primary hover:text-primary/80 text-sm font-medium">
                  Voir
                </button>
              </div>
            </div>
            <div className="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-700">
              <div>
                <p className="font-medium text-black dark:text-white">
                  blog.example.com/sitemap.xml
                </p>
                <p className="text-sm text-body-color dark:text-body-color-dark">
                  Analyse terminée il y a 1 jour
                </p>
              </div>
              <div className="flex items-center space-x-2">
                <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
                  Terminé
                </span>
                <button className="text-primary hover:text-primary/80 text-sm font-medium">
                  Voir
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 