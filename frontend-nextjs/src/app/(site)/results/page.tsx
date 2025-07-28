"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

// Types pour les données
interface Suggestion {
  id: string;
  sourcePage: string;
  targetPage: string;
  anchorText: string;
  score: number;
  status: "pending" | "approved" | "rejected";
  createdAt: string;
}

export default function Results() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [filter, setFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  // Données mockées
  const mockSuggestions: Suggestion[] = [
    {
      id: "1",
      sourcePage: "https://example.com/guide-seo",
      targetPage: "https://example.com/optimisation-mots-cles",
      anchorText: "optimisation des mots-clés",
      score: 0.85,
      status: "pending",
      createdAt: "2024-01-15T10:30:00Z"
    },
    {
      id: "2",
      sourcePage: "https://example.com/backlinks",
      targetPage: "https://example.com/strategie-backlinks",
      anchorText: "stratégie de backlinks",
      score: 0.92,
      status: "approved",
      createdAt: "2024-01-15T10:30:00Z"
    },
    {
      id: "3",
      sourcePage: "https://example.com/content-marketing",
      targetPage: "https://example.com/creation-contenu",
      anchorText: "création de contenu",
      score: 0.78,
      status: "rejected",
      createdAt: "2024-01-15T10:30:00Z"
    }
  ];

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

  // Filtrer les suggestions
  const filteredSuggestions = mockSuggestions.filter(suggestion => {
    const matchesFilter = filter === "all" || suggestion.status === filter;
    const matchesSearch = suggestion.anchorText.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         suggestion.sourcePage.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         suggestion.targetPage.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const handleStatusChange = (id: string, newStatus: "approved" | "rejected") => {
    // Ici on mettrait à jour le statut via API
    console.log(`Changing suggestion ${id} to ${newStatus}`);
  };

  const handleExport = () => {
    // Ici on exporterait les données
    console.log("Exporting data...");
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-black dark:text-white mb-2">
                Résultats de l'Analyse
              </h1>
              <p className="text-body-color dark:text-body-color-dark">
                Suggestions de maillage interne générées par l'IA
              </p>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={handleExport}
                className="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary/80 transition duration-300"
              >
                Exporter CSV
              </button>
              <button
                onClick={() => router.push("/dashboard")}
                className="border border-primary text-primary px-6 py-2 rounded-md hover:bg-primary hover:text-white transition duration-300"
              >
                Nouvelle Analyse
              </button>
            </div>
          </div>

          {/* Statistiques */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                  <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-body-color dark:text-body-color-dark">Total</p>
                  <p className="text-2xl font-bold text-black dark:text-white">{mockSuggestions.length}</p>
                </div>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
                  <svg className="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-body-color dark:text-body-color-dark">En attente</p>
                  <p className="text-2xl font-bold text-black dark:text-white">
                    {mockSuggestions.filter(s => s.status === "pending").length}
                  </p>
                </div>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                  <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-body-color dark:text-body-color-dark">Approuvé</p>
                  <p className="text-2xl font-bold text-black dark:text-white">
                    {mockSuggestions.filter(s => s.status === "approved").length}
                  </p>
                </div>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
              <div className="flex items-center">
                <div className="p-2 bg-red-100 dark:bg-red-900 rounded-lg">
                  <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-body-color dark:text-body-color-dark">Rejeté</p>
                  <p className="text-2xl font-bold text-black dark:text-white">
                    {mockSuggestions.filter(s => s.status === "rejected").length}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Filtres et recherche */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1">
              <input
                type="text"
                placeholder="Rechercher dans les suggestions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>
            <div className="flex space-x-2">
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="all">Tous les statuts</option>
                <option value="pending">En attente</option>
                <option value="approved">Approuvé</option>
                <option value="rejected">Rejeté</option>
              </select>
            </div>
          </div>
        </div>

        {/* Tableau des résultats */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Page Source
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Page Cible
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Ancre
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredSuggestions.map((suggestion) => (
                  <tr key={suggestion.id} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-black dark:text-white">
                      <div className="max-w-xs truncate" title={suggestion.sourcePage}>
                        {suggestion.sourcePage}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-black dark:text-white">
                      <div className="max-w-xs truncate" title={suggestion.targetPage}>
                        {suggestion.targetPage}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-black dark:text-white">
                      {suggestion.anchorText}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-black dark:text-white">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        suggestion.score >= 0.8 ? 'bg-green-100 text-green-800' :
                        suggestion.score >= 0.6 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {(suggestion.score * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        suggestion.status === 'approved' ? 'bg-green-100 text-green-800' :
                        suggestion.status === 'rejected' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {suggestion.status === 'approved' ? 'Approuvé' :
                         suggestion.status === 'rejected' ? 'Rejeté' : 'En attente'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-black dark:text-white">
                      <div className="flex space-x-2">
                        {suggestion.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleStatusChange(suggestion.id, 'approved')}
                              className="text-green-600 hover:text-green-900 text-xs font-medium"
                            >
                              Approuver
                            </button>
                            <button
                              onClick={() => handleStatusChange(suggestion.id, 'rejected')}
                              className="text-red-600 hover:text-red-900 text-xs font-medium"
                            >
                              Rejeter
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {filteredSuggestions.length === 0 && (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">Aucune suggestion trouvée</h3>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Essayez de modifier vos filtres ou votre recherche.
            </p>
          </div>
        )}
      </div>
    </div>
  );
} 