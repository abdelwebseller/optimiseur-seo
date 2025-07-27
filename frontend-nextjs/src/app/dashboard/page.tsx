"use client";

import Navigation from "@/components/Navigation";
import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Button,
  Textarea,
  Progress,
  Chip,
  Alert,
} from "@heroui/react";
import { useState } from "react";

export default function Dashboard() {
  const [sitemapUrl, setSitemapUrl] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sitemapUrl.trim()) {
      setError("Veuillez saisir une URL de sitemap valide");
      return;
    }

    setIsProcessing(true);
    setError("");
    setProgress(0);
    setStatus("Démarrage de l'analyse...");

    // Simulation du processus d'analyse
    const steps = [
      "Téléchargement du sitemap...",
      "Extraction des URLs...",
      "Génération des embeddings...",
      "Calcul des similarités...",
      "Génération des suggestions...",
      "Finalisation..."
    ];

    for (let i = 0; i < steps.length; i++) {
      setStatus(steps[i]);
      setProgress(((i + 1) / steps.length) * 100);
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    setIsProcessing(false);
    setStatus("Analyse terminée !");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Dashboard
            </h1>
            <p className="text-lg text-gray-600">
              Analysez votre sitemap et générez des suggestions de maillage interne
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Formulaire d'upload */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <h2 className="text-2xl font-semibold">Nouvelle Analyse</h2>
                <p className="text-gray-600">
                                     Entrez l&apos;URL de votre sitemap XML pour commencer l&apos;analyse
                </p>
              </CardHeader>
              <CardBody>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      URL du Sitemap
                    </label>
                    <Input
                      type="url"
                      placeholder="https://example.com/sitemap.xml"
                      value={sitemapUrl}
                      onChange={(e) => setSitemapUrl(e.target.value)}
                      isDisabled={isProcessing}
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Paramètres (optionnel)
                    </label>
                    <Textarea
                      placeholder="Paramètres avancés..."
                      className="w-full"
                      isDisabled={isProcessing}
                    />
                  </div>

                  {error && (
                    <Alert color="danger" className="mb-4">
                      {error}
                    </Alert>
                  )}

                  <Button
                    type="submit"
                    color="primary"
                    size="lg"
                    className="w-full bg-gradient-to-r from-blue-500 to-purple-600"
                    isDisabled={isProcessing}
                  >
                    {isProcessing ? "Analyse en cours..." : "Lancer l'analyse"}
                  </Button>
                </form>
              </CardBody>
            </Card>

            {/* Statut de l'analyse */}
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <h2 className="text-2xl font-semibold">Statut de l'Analyse</h2>
                <p className="text-gray-600">
                  Suivez l'avancement de votre analyse en temps réel
                </p>
              </CardHeader>
              <CardBody>
                {isProcessing ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">
                        Progression
                      </span>
                      <Chip color="primary" variant="flat">
                        {Math.round(progress)}%
                      </Chip>
                    </div>
                    <Progress
                      value={progress}
                      color="primary"
                      className="w-full"
                    />
                    <p className="text-sm text-gray-600">{status}</p>
                  </div>
                ) : progress > 0 ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">
                        Progression
                      </span>
                      <Chip color="success" variant="flat">
                        Terminé
                      </Chip>
                    </div>
                    <Progress
                      value={100}
                      color="success"
                      className="w-full"
                    />
                    <p className="text-sm text-green-600">{status}</p>
                    <Button
                      as="a"
                      href="/results"
                      color="primary"
                      className="w-full"
                    >
                      Voir les résultats
                    </Button>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <p className="text-gray-500">
                      Aucune analyse en cours
                    </p>
                  </div>
                )}
              </CardBody>
            </Card>
          </div>

          {/* Historique des analyses */}
          <Card className="border-0 shadow-lg mt-8">
            <CardHeader>
              <h2 className="text-2xl font-semibold">Analyses Récentes</h2>
            </CardHeader>
            <CardBody>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h3 className="font-medium">example.com/sitemap.xml</h3>
                    <p className="text-sm text-gray-600">Analyse terminée il y a 2 heures</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Chip color="success" variant="flat" size="sm">
                      Terminé
                    </Chip>
                    <Button size="sm" variant="bordered">
                      Voir
                    </Button>
                  </div>
                </div>
                
                <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <h3 className="font-medium">blog.example.com/sitemap.xml</h3>
                    <p className="text-sm text-gray-600">Analyse terminée il y a 1 jour</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Chip color="success" variant="flat" size="sm">
                      Terminé
                    </Chip>
                    <Button size="sm" variant="bordered">
                      Voir
                    </Button>
                  </div>
                </div>
              </div>
            </CardBody>
          </Card>
        </div>
      </main>
    </div>
  );
} 