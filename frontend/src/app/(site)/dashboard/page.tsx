import { Metadata } from "next";
import DashboardPage from "@/components/Dashboard";

export const metadata: Metadata = {
  title: "Dashboard - Semantra",
  description: "Analysez votre sitemap et optimisez votre maillage interne avec Semantra",
};

const Dashboard = () => {
  return <DashboardPage />;
};

export default Dashboard; 