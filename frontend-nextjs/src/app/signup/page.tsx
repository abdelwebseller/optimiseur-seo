"use client";

import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Button,
  Link,
  Divider,
  Checkbox,
} from "@heroui/react";
import { useState } from "react";

export default function Signup() {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
    company: "",
    acceptTerms: false,
    acceptNewsletter: false,
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (field: string, value: string | boolean) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      alert("Les mots de passe ne correspondent pas");
      return;
    }

    if (!formData.acceptTerms) {
      alert("Veuillez accepter les conditions d'utilisation");
      return;
    }

    setIsLoading(true);
    
    // Simulation d'inscription
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsLoading(false);
    
    // Redirection vers le dashboard
    window.location.href = "/dashboard";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-lg border-0 shadow-xl">
        <CardHeader className="text-center pb-0">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">SEO</span>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Créer un compte
          </h1>
          <p className="text-gray-600">
            Rejoignez Optimiseur SEO et améliorez votre référencement
          </p>
        </CardHeader>
        <CardBody className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Prénom
                </label>
                <Input
                  type="text"
                  placeholder="Votre prénom"
                  value={formData.firstName}
                  onChange={(e) => handleChange("firstName", e.target.value)}
                  required
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nom
                </label>
                <Input
                  type="text"
                  placeholder="Votre nom"
                  value={formData.lastName}
                  onChange={(e) => handleChange("lastName", e.target.value)}
                  required
                  className="w-full"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Adresse email
              </label>
              <Input
                type="email"
                placeholder="votre@email.com"
                value={formData.email}
                onChange={(e) => handleChange("email", e.target.value)}
                required
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nom de l'entreprise (optionnel)
              </label>
              <Input
                type="text"
                placeholder="Votre entreprise"
                value={formData.company}
                onChange={(e) => handleChange("company", e.target.value)}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Mot de passe
              </label>
              <Input
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => handleChange("password", e.target.value)}
                required
                className="w-full"
              />
              <p className="text-xs text-gray-500 mt-1">
                Au moins 8 caractères avec des lettres et des chiffres
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confirmer le mot de passe
              </label>
              <Input
                type="password"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={(e) => handleChange("confirmPassword", e.target.value)}
                required
                className="w-full"
              />
            </div>

            <div className="space-y-3">
              <Checkbox
                isSelected={formData.acceptTerms}
                onValueChange={(value) => handleChange("acceptTerms", value)}
                required
              >
                <span className="text-sm text-gray-600">
                  J'accepte les{" "}
                  <Link href="/terms" className="text-blue-600 hover:underline">
                    conditions d'utilisation
                  </Link>{" "}
                  et la{" "}
                  <Link href="/privacy" className="text-blue-600 hover:underline">
                    politique de confidentialité
                  </Link>
                </span>
              </Checkbox>

              <Checkbox
                isSelected={formData.acceptNewsletter}
                onValueChange={(value) => handleChange("acceptNewsletter", value)}
              >
                <span className="text-sm text-gray-600">
                  Je souhaite recevoir des newsletters et des mises à jour
                </span>
              </Checkbox>
            </div>

            <Button
              type="submit"
              color="primary"
              size="lg"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600"
              isLoading={isLoading}
            >
              Créer mon compte
            </Button>
          </form>

          <Divider />

          <div className="text-center">
            <p className="text-sm text-gray-600 mb-4">
              Vous avez déjà un compte ?
            </p>
            <Button
              as={Link}
              href="/login"
              variant="bordered"
              className="w-full"
            >
              Se connecter
            </Button>
          </div>

          <div className="text-center">
            <p className="text-xs text-gray-500">
              En créant un compte, vous acceptez nos{" "}
              <Link href="/terms" className="text-blue-600 hover:underline">
                conditions d'utilisation
              </Link>{" "}
              et notre{" "}
              <Link href="/privacy" className="text-blue-600 hover:underline">
                politique de confidentialité
              </Link>
            </p>
          </div>
        </CardBody>
      </Card>
    </div>
  );
} 