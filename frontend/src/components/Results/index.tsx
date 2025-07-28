"use client";

import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";

interface Suggestion {
  id: string;
  sourcePage: string;
  targetPage: string;
  anchorText: string;
  score: number;
  status: "pending" | "approved" | "rejected";
  reasoning: string;
}

const ResultsPage = () => {
  const { data: session } = useSession();
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [filter, setFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  // Données de démonstration
  useEffect(() => {
    const mockSuggestions: Suggestion[] = [
      {
        id: "1",
        sourcePage: "https://example.com/guide-seo",
        targetPage: "https://example.com/optimisation-mots-cles",
        anchorText: "optimisation des mots-clés",
        score: 0.92,
        status: "pending",
        reasoning: "Fort lien sémantique entre le contenu des deux pages"
      },
      {
        id: "2",
        sourcePage: "https://example.com/guide-seo",
        targetPage: "https://example.com/backlinks",
        anchorText: "stratégie de backlinks",
        score: 0.87,
        status: "approved",
        reasoning: "Contenu complémentaire sur les liens externes"
      },
      {
        id: "3",
        sourcePage: "https://example.com/optimisation-mots-cles",
        targetPage: "https://example.com/analyse-competition",
        anchorText: "analyse de la concurrence",
        score: 0.78,
        status: "rejected",
        reasoning: "Lien pertinent mais score insuffisant"
      }
    ];

    setTimeout(() => {
      setSuggestions(mockSuggestions);
      setIsLoading(false);
    }, 1000);
  }, []);

  const filteredSuggestions = suggestions.filter(suggestion => {
    const matchesFilter = filter === "all" || suggestion.status === filter;
    const matchesSearch = suggestion.anchorText.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         suggestion.sourcePage.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         suggestion.targetPage.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const handleStatusChange = (id: string, newStatus: "approved" | "rejected") => {
    setSuggestions(prev => prev.map(s => s.id === id ? { ...s, status: newStatus } : s));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved": return "bg-green-100 text-green-800";
      case "rejected": return "bg-red-100 text-red-800";
      default: return "bg-yellow-100 text-yellow-800";
    }
  };

  if (!session) {
    return (
      <section className="pt-16 lg:pt-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
              Connectez-vous pour voir les résultats
            </h1>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="pt-16 lg:pt-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
            Suggestions de Maillage Interne
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            {suggestions.length} suggestions trouvées pour votre site
          </p>
        </div>

        {/* Filtres et recherche */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Rechercher dans les suggestions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">Tous les statuts</option>
            <option value="pending">En attente</option>
            <option value="approved">Approuvés</option>
            <option value="rejected">Rejetés</option>
          </select>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement des suggestions...</p>
          </div>
        ) : (
          <div className="bg-white shadow-lg rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Suggestion
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Statut
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredSuggestions.map((suggestion) => (
                    <tr key={suggestion.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="space-y-2">
                          <div className="text-sm font-medium text-gray-900">
                            <strong>Ancre :</strong> {suggestion.anchorText}
                          </div>
                          <div className="text-sm text-gray-500">
                            <strong>De :</strong> {suggestion.sourcePage}
                          </div>
                          <div className="text-sm text-gray-500">
                            <strong>Vers :</strong> {suggestion.targetPage}
                          </div>
                          <div className="text-xs text-gray-400">
                            {suggestion.reasoning}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {(suggestion.score * 100).toFixed(1)}%
                        </div>
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full"
                            style={{ width: `${suggestion.score * 100}%` }}
                          ></div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(suggestion.status)}`}>
                          {suggestion.status === "pending" && "En attente"}
                          {suggestion.status === "approved" && "Approuvé"}
                          {suggestion.status === "rejected" && "Rejeté"}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        {suggestion.status === "pending" && (
                          <div className="space-x-2">
                            <button
                              onClick={() => handleStatusChange(suggestion.id, "approved")}
                              className="text-green-600 hover:text-green-900"
                            >
                              Approuver
                            </button>
                            <button
                              onClick={() => handleStatusChange(suggestion.id, "rejected")}
                              className="text-red-600 hover:text-red-900"
                            >
                              Rejeter
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {!isLoading && filteredSuggestions.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">Aucune suggestion trouvée</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default ResultsPage; 