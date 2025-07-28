"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

const DashboardPage = () => {
  const { data: session } = useSession();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    sitemapUrl: "",
    maxUrls: 1000,
    crawlSpeed: "normal",
    userAgent: "Semantra Bot 1.0",
    includeSubdomains: false,
    filterPattern: "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!session) {
      router.push("/signin");
      return;
    }

    setIsLoading(true);
    try {
      // TODO: Appel API vers le backend
      console.log("Démarrage de l'analyse:", formData);
      // Simuler un délai
      await new Promise(resolve => setTimeout(resolve, 2000));
      router.push("/results");
    } catch (error) {
      console.error("Erreur lors de l'analyse:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === "checkbox" ? (e.target as HTMLInputElement).checked : value
    }));
  };

  if (!session) {
    return (
      <section className="pt-16 lg:pt-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
              Connectez-vous pour accéder au dashboard
            </h1>
            <p className="mt-4 text-lg text-gray-600">
              Vous devez être connecté pour analyser votre sitemap
            </p>
            <button
              onClick={() => router.push("/signin")}
              className="mt-6 inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Se connecter
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="pt-16 lg:pt-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
            Analyse SEO - Semantra
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Analysez votre sitemap et optimisez votre maillage interne
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="space-y-6 bg-white p-8 rounded-lg shadow-lg">
            <div>
              <label htmlFor="sitemapUrl" className="block text-sm font-medium text-gray-700 mb-2">
                URL du Sitemap *
              </label>
              <input
                type="url"
                id="sitemapUrl"
                name="sitemapUrl"
                required
                value={formData.sitemapUrl}
                onChange={handleInputChange}
                placeholder="https://example.com/sitemap.xml"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="maxUrls" className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre max d'URLs
                </label>
                <input
                  type="number"
                  id="maxUrls"
                  name="maxUrls"
                  min="1"
                  max="100000"
                  value={formData.maxUrls}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label htmlFor="crawlSpeed" className="block text-sm font-medium text-gray-700 mb-2">
                  Vitesse de crawl
                </label>
                <select
                  id="crawlSpeed"
                  name="crawlSpeed"
                  value={formData.crawlSpeed}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="slow">Lente</option>
                  <option value="normal">Normale</option>
                  <option value="fast">Rapide</option>
                </select>
              </div>
            </div>

            <div>
              <label htmlFor="userAgent" className="block text-sm font-medium text-gray-700 mb-2">
                User Agent
              </label>
              <input
                type="text"
                id="userAgent"
                name="userAgent"
                value={formData.userAgent}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                id="includeSubdomains"
                name="includeSubdomains"
                checked={formData.includeSubdomains}
                onChange={handleInputChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="includeSubdomains" className="ml-2 block text-sm text-gray-900">
                Inclure les sous-domaines
              </label>
            </div>

            <div>
              <label htmlFor="filterPattern" className="block text-sm font-medium text-gray-700 mb-2">
                Filtre Regex (optionnel)
              </label>
              <textarea
                id="filterPattern"
                name="filterPattern"
                value={formData.filterPattern}
                onChange={handleInputChange}
                placeholder="^https://example.com/blog/.*"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="mt-1 text-sm text-gray-500">
                Utilisez une expression régulière pour filtrer les URLs
              </p>
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyse en cours...
                  </>
                ) : (
                  "Démarrer l'analyse"
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
};

export default DashboardPage; 