"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function Settings() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [isSaving, setIsSaving] = useState(false);

  // États pour les paramètres
  const [settings, setSettings] = useState({
    openaiApiKey: "",
    similarityThreshold: 0.7,
    maxSuggestions: 50,
    darkMode: false,
    autoApprove: false,
    emailNotifications: true,
    embeddingModel: "text-embedding-ada-002",
    customJsonParams: "{}",
    backendApiUrl: "http://localhost:8000"
  });

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

  const handleSave = async () => {
    setIsSaving(true);
    // Simulation de sauvegarde
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsSaving(false);
    // Ici on sauvegarderait les paramètres via API
    console.log("Saving settings:", settings);
  };

  const handleReset = () => {
    setSettings({
      openaiApiKey: "",
      similarityThreshold: 0.7,
      maxSuggestions: 50,
      darkMode: false,
      autoApprove: false,
      emailNotifications: true,
      embeddingModel: "text-embedding-ada-002",
      customJsonParams: "{}",
      backendApiUrl: "http://localhost:8000"
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-black dark:text-white mb-2">
            Paramètres
          </h1>
          <p className="text-body-color dark:text-body-color-dark">
            Configurez votre application d'optimisation SEO
          </p>
        </div>

        <div className="space-y-8">
          {/* Configuration API */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-black dark:text-white mb-4">
              Configuration API
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  Clé API OpenAI
                </label>
                <input
                  type="password"
                  value={settings.openaiApiKey}
                  onChange={(e) => setSettings({...settings, openaiApiKey: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                  placeholder="sk-..."
                />
                <p className="text-xs text-body-color dark:text-body-color-dark mt-1">
                  Utilisée pour la génération d'embeddings et les suggestions IA
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  Seuil de similarité
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={settings.similarityThreshold}
                    onChange={(e) => setSettings({...settings, similarityThreshold: parseFloat(e.target.value)})}
                    className="flex-1"
                  />
                  <span className="text-sm text-black dark:text-white min-w-[3rem]">
                    {(settings.similarityThreshold * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-xs text-body-color dark:text-body-color-dark mt-1">
                  Seuil minimum pour considérer deux pages comme similaires
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  Nombre maximum de suggestions
                </label>
                <input
                  type="number"
                  min="1"
                  max="200"
                  value={settings.maxSuggestions}
                  onChange={(e) => setSettings({...settings, maxSuggestions: parseInt(e.target.value)})}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                />
              </div>
            </div>
          </div>

          {/* Préférences Utilisateur */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-black dark:text-white mb-4">
              Préférences
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-black dark:text-white">
                    Mode sombre
                  </label>
                  <p className="text-xs text-body-color dark:text-body-color-dark">
                    Activer le thème sombre pour l'interface
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.darkMode}
                    onChange={(e) => setSettings({...settings, darkMode: e.target.checked})}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary/20 dark:peer-focus:ring-primary/80 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-black dark:text-white">
                    Auto-approbation
                  </label>
                  <p className="text-xs text-body-color dark:text-body-color-dark">
                    Approuver automatiquement les suggestions avec un score élevé
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.autoApprove}
                    onChange={(e) => setSettings({...settings, autoApprove: e.target.checked})}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary/20 dark:peer-focus:ring-primary/80 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
                </label>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium text-black dark:text-white">
                    Notifications par email
                  </label>
                  <p className="text-xs text-body-color dark:text-body-color-dark">
                    Recevoir des notifications par email lors de la fin d'analyse
                  </p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.emailNotifications}
                    onChange={(e) => setSettings({...settings, emailNotifications: e.target.checked})}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary/20 dark:peer-focus:ring-primary/80 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
                </label>
              </div>
            </div>
          </div>

          {/* Configuration Avancée */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-black dark:text-white mb-4">
              Configuration Avancée
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  Modèle d'embedding
                </label>
                <select
                  value={settings.embeddingModel}
                  onChange={(e) => setSettings({...settings, embeddingModel: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  <option value="text-embedding-ada-002">text-embedding-ada-002</option>
                  <option value="text-embedding-3-small">text-embedding-3-small</option>
                  <option value="text-embedding-3-large">text-embedding-3-large</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  URL de l'API backend
                </label>
                <input
                  type="url"
                  value={settings.backendApiUrl}
                  onChange={(e) => setSettings({...settings, backendApiUrl: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
                  placeholder="http://localhost:8000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-black dark:text-white mb-2">
                  Paramètres personnalisés (JSON)
                </label>
                <textarea
                  value={settings.customJsonParams}
                  onChange={(e) => setSettings({...settings, customJsonParams: e.target.value})}
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white font-mono text-sm"
                  placeholder='{"custom_param": "value"}'
                />
                <p className="text-xs text-body-color dark:text-body-color-dark mt-1">
                  Paramètres JSON personnalisés pour l'API
                </p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-4">
            <button
              onClick={handleReset}
              className="px-6 py-2 border border-gray-300 dark:border-gray-600 text-black dark:text-white rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition duration-300"
            >
              Réinitialiser
            </button>
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/80 disabled:opacity-50 disabled:cursor-not-allowed transition duration-300"
            >
              {isSaving ? "Sauvegarde..." : "Sauvegarder"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 