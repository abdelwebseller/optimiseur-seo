"use client";

import Navigation from "@/components/Navigation";
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Button,
  Switch,
  Select,
  SelectItem,
  Textarea,
  Divider,
} from "@heroui/react";
import { useState } from "react";

export default function Settings() {
  const [openaiKey, setOpenaiKey] = useState("");
  const [similarityThreshold, setSimilarityThreshold] = useState("0.8");
  const [maxSuggestions, setMaxSuggestions] = useState("50");
  const [autoApprove, setAutoApprove] = useState(false);
  const [emailNotifications, setEmailNotifications] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  const handleSave = () => {
    // Logique de sauvegarde des paramètres
    console.log("Paramètres sauvegardés");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Paramètres
            </h1>
            <p className="text-lg text-gray-600">
              Configurez votre application Optimiseur SEO
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Configuration API */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <h2 className="text-2xl font-semibold">Configuration API</h2>
                <p className="text-gray-600">
                  Paramètres de connexion aux services externes
                </p>
              </CardHeader>
              <CardBody className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Clé API OpenAI
                  </label>
                  <Input
                    type="password"
                    placeholder="sk-..."
                    value={openaiKey}
                    onChange={(e) => setOpenaiKey(e.target.value)}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Utilisée pour la génération d'embeddings et l'analyse sémantique
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Seuil de similarité minimum
                  </label>
                                  <Select
                  placeholder="Sélectionner un seuil"
                  selectedKeys={[similarityThreshold]}
                  onSelectionChange={(keys) => setSimilarityThreshold(Array.from(keys)[0] as string)}
                  className="w-full"
                >
                  <SelectItem key="0.7">0.7 - Très permissif</SelectItem>
                  <SelectItem key="0.8">0.8 - Recommandé</SelectItem>
                  <SelectItem key="0.9">0.9 - Strict</SelectItem>
                  <SelectItem key="0.95">0.95 - Très strict</SelectItem>
                </Select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre maximum de suggestions
                  </label>
                  <Input
                    type="number"
                    placeholder="50"
                    value={maxSuggestions}
                    onChange={(e) => setMaxSuggestions(e.target.value)}
                    className="w-full"
                  />
                </div>
              </CardBody>
            </Card>

            {/* Préférences utilisateur */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <h2 className="text-2xl font-semibold">Préférences</h2>
                <p className="text-gray-600">
                  Personnalisez votre expérience utilisateur
                </p>
              </CardHeader>
              <CardBody className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Mode sombre</h3>
                    <p className="text-sm text-gray-600">Activer le thème sombre</p>
                  </div>
                  <Switch
                    isSelected={darkMode}
                    onValueChange={setDarkMode}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Approbation automatique</h3>
                    <p className="text-sm text-gray-600">Approuver automatiquement les suggestions avec un score élevé</p>
                  </div>
                  <Switch
                    isSelected={autoApprove}
                    onValueChange={setAutoApprove}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium">Notifications par email</h3>
                    <p className="text-sm text-gray-600">Recevoir des notifications par email</p>
                  </div>
                  <Switch
                    isSelected={emailNotifications}
                    onValueChange={setEmailNotifications}
                  />
                </div>
              </CardBody>
            </Card>
          </div>

          {/* Configuration avancée */}
          <Card className="border-0 shadow-lg mt-8">
            <CardHeader>
              <h2 className="text-2xl font-semibold">Configuration Avancée</h2>
              <p className="text-gray-600">
                Paramètres techniques pour les utilisateurs expérimentés
              </p>
            </CardHeader>
            <CardBody className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Modèle d'embedding
                </label>
                <Select
                  placeholder="Sélectionner un modèle"
                  className="w-full"
                  defaultSelectedKeys={["text-embedding-ada-002"]}
                >
                  <SelectItem key="text-embedding-ada-002">
                    text-embedding-ada-002 (Recommandé)
                  </SelectItem>
                  <SelectItem key="text-embedding-3-small">
                    text-embedding-3-small (Plus rapide)
                  </SelectItem>
                  <SelectItem key="text-embedding-3-large">
                    text-embedding-3-large (Plus précis)
                  </SelectItem>
                </Select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Paramètres personnalisés (JSON)
                </label>
                <Textarea
                  placeholder='{"max_tokens": 1000, "temperature": 0.7}'
                  className="w-full"
                  minRows={3}
                />
                <p className="text-xs text-gray-500 mt-1">
                  Configuration JSON personnalisée pour l'API OpenAI
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  URL de l'API backend
                </label>
                <Input
                  type="url"
                  placeholder="http://localhost:8000"
                  className="w-full"
                />
                <p className="text-xs text-gray-500 mt-1">
                  URL de votre serveur backend (optionnel)
                </p>
              </div>
            </CardBody>
          </Card>

          {/* Actions */}
          <div className="flex justify-end gap-4 mt-8">
            <Button
              variant="bordered"
              color="danger"
            >
              Réinitialiser
            </Button>
            <Button
              color="primary"
              onClick={handleSave}
              className="bg-gradient-to-r from-blue-500 to-purple-600"
            >
              Sauvegarder
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
} 