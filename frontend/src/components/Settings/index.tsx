"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";

const SettingsPage = () => {
  const { data: session } = useSession();
  const [settings, setSettings] = useState({
    openaiApiKey: "",
    geminiApiKey: "",
    similarityThreshold: 0.7,
    maxSuggestions: 50,
    embeddingModel: "text-embedding-3-large",
    backendUrl: "http://localhost:8000",
    darkMode: false,
    autoApprove: false,
    emailNotifications: true,
  });

  const [isSaving, setIsSaving] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: type === "checkbox" ? (e.target as HTMLInputElement).checked : 
               type === "number" ? parseFloat(value) : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    
    try {
      // TODO: Sauvegarder les paramètres via l'API
      console.log("Sauvegarde des paramètres:", settings);
      await new Promise(resolve => setTimeout(resolve, 1000));
      alert("Paramètres sauvegardés avec succès !");
    } catch (error) {
      console.error("Erreur lors de la sauvegarde:", error);
      alert("Erreur lors de la sauvegarde des paramètres");
    } finally {
      setIsSaving(false);
    }
  };

  if (!session) {
    return (
      <section className="pt-16 lg:pt-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
              Connectez-vous pour accéder aux paramètres
            </h1>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="pt-16 lg:pt-20">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
            Paramètres
          </h1>
          <p className="mt-4 text-lg text-gray-600">
            Configurez vos clés API et préférences d'analyse
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Clés API */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Clés API</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="openaiApiKey" className="block text-sm font-medium text-gray-700 mb-2">
                  Clé API OpenAI
                </label>
                <input
                  type="password"
                  id="openaiApiKey"
                  name="openaiApiKey"
                  value={settings.openaiApiKey}
                  onChange={handleInputChange}
                  placeholder="sk-..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Utilisée pour l'optimisation des ancres et l'analyse sémantique
                </p>
              </div>

              <div>
                <label htmlFor="geminiApiKey" className="block text-sm font-medium text-gray-700 mb-2">
                  Clé API Google Gemini
                </label>
                <input
                  type="password"
                  id="geminiApiKey"
                  name="geminiApiKey"
                  value={settings.geminiApiKey}
                  onChange={handleInputChange}
                  placeholder="AIza..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="mt-1 text-sm text-gray-500">
                  Alternative à OpenAI pour l'optimisation des ancres
                </p>
              </div>
            </div>
          </div>

          {/* Paramètres d'analyse */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Paramètres d'analyse</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="similarityThreshold" className="block text-sm font-medium text-gray-700 mb-2">
                  Seuil de similarité (0.1 - 1.0)
                </label>
                <input
                  type="number"
                  id="similarityThreshold"
                  name="similarityThreshold"
                  min="0.1"
                  max="1.0"
                  step="0.1"
                  value={settings.similarityThreshold}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label htmlFor="maxSuggestions" className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre max de suggestions
                </label>
                <input
                  type="number"
                  id="maxSuggestions"
                  name="maxSuggestions"
                  min="1"
                  max="1000"
                  value={settings.maxSuggestions}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label htmlFor="embeddingModel" className="block text-sm font-medium text-gray-700 mb-2">
                  Modèle d'embedding
                </label>
                <select
                  id="embeddingModel"
                  name="embeddingModel"
                  value={settings.embeddingModel}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="text-embedding-3-small">text-embedding-3-small</option>
                  <option value="text-embedding-3-large">text-embedding-3-large</option>
                  <option value="text-embedding-ada-002">text-embedding-ada-002</option>
                </select>
              </div>

              <div>
                <label htmlFor="backendUrl" className="block text-sm font-medium text-gray-700 mb-2">
                  URL du backend
                </label>
                <input
                  type="url"
                  id="backendUrl"
                  name="backendUrl"
                  value={settings.backendUrl}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          {/* Préférences */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Préférences</h2>
            <div className="space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="darkMode"
                  name="darkMode"
                  checked={settings.darkMode}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="darkMode" className="ml-2 block text-sm text-gray-900">
                  Mode sombre
                </label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="autoApprove"
                  name="autoApprove"
                  checked={settings.autoApprove}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="autoApprove" className="ml-2 block text-sm text-gray-900">
                  Approuver automatiquement les suggestions avec un score élevé
                </label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="emailNotifications"
                  name="emailNotifications"
                  checked={settings.emailNotifications}
                  onChange={handleInputChange}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="emailNotifications" className="ml-2 block text-sm text-gray-900">
                  Notifications par email
                </label>
              </div>
            </div>
          </div>

          {/* Boutons d'action */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              onClick={() => setSettings({
                openaiApiKey: "",
                geminiApiKey: "",
                similarityThreshold: 0.7,
                maxSuggestions: 50,
                embeddingModel: "text-embedding-3-large",
                backendUrl: "http://localhost:8000",
                darkMode: false,
                autoApprove: false,
                emailNotifications: true,
              })}
              className="px-6 py-3 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Réinitialiser
            </button>
            <button
              type="submit"
              disabled={isSaving}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSaving ? "Sauvegarde..." : "Sauvegarder"}
            </button>
          </div>
        </form>
      </div>
    </section>
  );
};

export default SettingsPage; 