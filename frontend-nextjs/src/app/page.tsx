import ScrollUp from "@/components/Common/ScrollUp";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Optimiseur SEO - Analyse de Maillage Interne",
  description: "Outil d'analyse et d'optimisation du maillage interne pour améliorer votre SEO. Analysez votre sitemap et générez des suggestions de liens internes optimisés.",
};

export default function Home() {
  return (
    <main>
      <ScrollUp />
      
      {/* Hero Section */}
      <section className="relative z-10 overflow-hidden pt-16 md:pt-[120px] 2xl:pt-[150px]">
        <div className="container">
          <div className="-mx-4 flex flex-wrap">
            <div className="w-full px-4">
              <div className="mx-auto max-w-[800px] text-center mb-16">
                <h1 className="mb-5 text-3xl font-bold leading-tight text-black dark:text-white sm:text-4xl sm:leading-tight md:text-5xl md:leading-tight">
                  Optimisez votre{" "}
                  <span className="text-primary">Maillage Interne</span>
                </h1>
                <p className="mb-12 text-base !leading-relaxed text-body-color dark:text-body-color-dark sm:text-lg md:text-xl">
                  Analysez votre sitemap et générez des suggestions de liens internes optimisés 
                  pour améliorer votre SEO et l'expérience utilisateur.
                </p>
                <div className="flex flex-col items-center justify-center space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
                  <a
                    href="/dashboard"
                    className="rounded-md bg-primary py-4 px-8 text-base font-semibold text-white duration-300 ease-in-out hover:bg-primary/80 hover:shadow-signUp"
                  >
                    Commencer l'Analyse
                  </a>
                  <a
                    href="/about"
                    className="inline-block rounded-md border border-transparent bg-transparent py-4 px-8 text-base font-semibold text-primary duration-300 ease-in-out hover:bg-primary hover:text-white"
                  >
                    En savoir plus
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative z-10 py-16 md:py-[120px]">
        <div className="container">
          <div className="-mx-4 flex flex-wrap">
            <div className="w-full px-4">
              <div className="mx-auto max-w-[620px] text-center mb-16">
                <h2 className="mb-4 text-3xl font-bold !leading-tight text-black dark:text-white sm:text-4xl md:text-[45px]">
                  Fonctionnalités Principales
                </h2>
                <p className="text-lg !leading-relaxed text-body-color dark:text-body-color-dark">
                  Tout ce dont vous avez besoin pour optimiser votre maillage interne
                </p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {/* Feature 1 */}
            <div className="w-full">
              <div className="wow fadeInUp group mb-9" data-wow-delay=".1s">
                <div className="mb-8 flex h-[70px] w-[70px] items-center justify-center rounded-md bg-primary bg-opacity-10 text-primary">
                  <svg className="h-9 w-9" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </div>
                <h3 className="mb-4 text-xl font-bold text-black dark:text-white sm:text-2xl lg:text-xl xl:text-2xl">
                  Analyse Automatique
                </h3>
                <p className="text-base !leading-relaxed text-body-color dark:text-body-color-dark">
                  Analysez automatiquement votre sitemap et découvrez les opportunités d'amélioration de votre maillage interne.
                </p>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="w-full">
              <div className="wow fadeInUp group mb-9" data-wow-delay=".15s">
                <div className="mb-8 flex h-[70px] w-[70px] items-center justify-center rounded-md bg-primary bg-opacity-10 text-primary">
                  <svg className="h-9 w-9" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                  </svg>
                </div>
                <h3 className="mb-4 text-xl font-bold text-black dark:text-white sm:text-2xl lg:text-xl xl:text-2xl">
                  Suggestions IA
                </h3>
                <p className="text-base !leading-relaxed text-body-color dark:text-body-color-dark">
                  Obtenez des suggestions intelligentes de liens internes générées par l'IA pour optimiser votre SEO.
                </p>
              </div>
            </div>

            {/* Feature 3 */}
            <div className="w-full">
              <div className="wow fadeInUp group mb-9" data-wow-delay=".2s">
                <div className="mb-8 flex h-[70px] w-[70px] items-center justify-center rounded-md bg-primary bg-opacity-10 text-primary">
                  <svg className="h-9 w-9" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <h3 className="mb-4 text-xl font-bold text-black dark:text-white sm:text-2xl lg:text-xl xl:text-2xl">
                  Export Facile
                </h3>
                <p className="text-base !leading-relaxed text-body-color dark:text-body-color-dark">
                  Exportez vos résultats en CSV ou Excel pour les partager avec votre équipe ou les intégrer dans vos outils.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 overflow-hidden bg-primary py-16 md:py-[120px]">
        <div className="container">
          <div className="-mx-4 flex flex-wrap items-center">
            <div className="w-full px-4 lg:w-1/2">
              <div className="max-w-[470px]">
                <div className="mb-9">
                  <h3 className="mb-4 text-3xl font-bold !leading-tight text-white sm:text-4xl md:text-[45px]">
                    Prêt à optimiser votre SEO ?
                  </h3>
                  <p className="text-base !leading-relaxed text-[#F3F4FE] md:text-lg">
                    Commencez dès maintenant votre analyse de maillage interne et améliorez votre référencement naturel.
                  </p>
                </div>
                <div className="flex flex-col space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0">
                  <a
                    href="/dashboard"
                    className="inline-flex items-center justify-center rounded-md bg-white py-4 px-8 text-center text-base font-semibold text-primary transition duration-300 ease-in-out hover:bg-gray-100"
                  >
                    Commencer Gratuitement
                  </a>
                  <a
                    href="/contact"
                    className="inline-flex items-center justify-center rounded-md border border-white py-4 px-8 text-center text-base font-semibold text-white transition duration-300 ease-in-out hover:bg-white hover:text-primary"
                  >
                    Nous Contacter
                  </a>
                </div>
              </div>
            </div>
            <div className="w-full px-4 lg:w-1/2">
              <div className="lg:ml-auto lg:text-right">
                <div className="relative z-10 inline-block">
                  <img
                    src="/images/hero/hero-image.svg"
                    alt="hero"
                    className="dark:hidden"
                  />
                  <img
                    src="/images/hero/hero-image-dark.svg"
                    alt="hero"
                    className="hidden dark:block"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
