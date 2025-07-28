import { Metadata } from "next";
import ResultsPage from "@/components/Results";

export const metadata: Metadata = {
  title: "Résultats - Semantra",
  description: "Consultez les suggestions de maillage interne générées par Semantra",
};

const Results = () => {
  return <ResultsPage />;
};

export default Results; 