import Navigation from "@/components/Navigation";
import {
  Card,
  CardBody,
  CardHeader,
  Button,
  Link,
} from "@heroui/react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
            Optimiseur SEO
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Maillage interne intelligent alimenté par l&apos;IA. Analysez votre sitemap, 
            générez des embeddings et découvrez les meilleures opportunités de liens internes.
          </p>
          <div className="flex gap-4 justify-center">
            <Button
              as={Link}
              href="/dashboard"
              color="primary"
              size="lg"
              className="bg-gradient-to-r from-blue-500 to-purple-600"
            >
              Commencer l'analyse
            </Button>
            <Button
              as={Link}
              href="/results"
              variant="bordered"
              size="lg"
            >
              Voir les résultats
            </Button>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <Card className="border-0 shadow-lg">
            <CardHeader className="pb-0">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold">Analyse de Sitemap</h3>
            </CardHeader>
            <CardBody>
              <p className="text-gray-600">
                Importez votre sitemap XML et laissez notre IA analyser automatiquement 
                la structure de votre site web.
              </p>
            </CardBody>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader className="pb-0">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold">Embeddings IA</h3>
            </CardHeader>
            <CardBody>
              <p className="text-gray-600">
                                 Génération automatique d&apos;embeddings via OpenAI pour comprendre 
                 le contenu sémantique de vos pages.
              </p>
            </CardBody>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader className="pb-0">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold">Suggestions Intelligentes</h3>
            </CardHeader>
            <CardBody>
              <p className="text-gray-600">
                Recevez des suggestions de liens internes optimisés basées sur 
                la similarité sémantique entre vos pages.
              </p>
            </CardBody>
          </Card>
        </div>

        {/* Stats Section */}
        <Card className="border-0 shadow-lg mb-16">
          <CardBody>
            <div className="grid md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="text-3xl font-bold text-blue-600 mb-2">1000+</div>
                <div className="text-gray-600">Sitemaps analysés</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-purple-600 mb-2">50K+</div>
                <div className="text-gray-600">Liens générés</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-green-600 mb-2">95%</div>
                <div className="text-gray-600">Précision IA</div>
              </div>
              <div>
                <div className="text-3xl font-bold text-orange-600 mb-2">24/7</div>
                <div className="text-gray-600">Disponibilité</div>
              </div>
            </div>
          </CardBody>
        </Card>

        {/* CTA Section */}
        <div className="text-center">
          <Card className="border-0 shadow-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            <CardBody className="py-12">
              <h2 className="text-3xl font-bold mb-4">
                Prêt à optimiser votre SEO ?
              </h2>
              <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
                Rejoignez des centaines de webmasters qui utilisent déjà notre 
                outil pour améliorer leur maillage interne et leur référencement.
              </p>
              <Button
                as={Link}
                href="/dashboard"
                color="primary"
                size="lg"
                variant="solid"
                className="bg-white text-blue-600 hover:bg-gray-100"
              >
                Commencer maintenant
              </Button>
            </CardBody>
          </Card>
        </div>
      </main>
    </div>
  );
}
