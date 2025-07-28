import { Metadata } from "next";
import SettingsPage from "@/components/Settings";

export const metadata: Metadata = {
  title: "Paramètres - Semantra",
  description: "Configurez vos paramètres d'analyse et vos clés API",
};

const Settings = () => {
  return <SettingsPage />;
};

export default Settings; 