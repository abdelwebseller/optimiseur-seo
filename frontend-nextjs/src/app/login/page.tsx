"use client";

import {
  Card,
  CardBody,
  CardHeader,
  Input,
  Button,
  Link,
  Divider,
} from "@heroui/react";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulation de connexion
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsLoading(false);
    
    // Redirection vers le dashboard
    window.location.href = "/dashboard";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md border-0 shadow-xl">
        <CardHeader className="text-center pb-0">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">SEO</span>
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Connexion
          </h1>
          <p className="text-gray-600">
            Accédez à votre compte Optimiseur SEO
          </p>
        </CardHeader>
        <CardBody className="space-y-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Adresse email
              </label>
              <Input
                type="email"
                placeholder="votre@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
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
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full"
              />
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                <span className="ml-2 text-sm text-gray-600">Se souvenir de moi</span>
              </label>
              <Link href="/forgot-password" className="text-sm text-blue-600 hover:underline">
                Mot de passe oublié ?
              </Link>
            </div>

            <Button
              type="submit"
              color="primary"
              size="lg"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600"
              isLoading={isLoading}
            >
              Se connecter
            </Button>
          </form>

          <Divider />

          <div className="text-center">
            <p className="text-sm text-gray-600 mb-4">
              Pas encore de compte ?
            </p>
            <Button
              as={Link}
              href="/signup"
              variant="bordered"
              className="w-full"
            >
              Créer un compte
            </Button>
          </div>

          <div className="text-center">
            <p className="text-xs text-gray-500">
              En vous connectant, vous acceptez nos{" "}
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