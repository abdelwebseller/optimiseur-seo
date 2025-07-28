import { Menu } from "@/types/menu";

const menuData: Menu[] = [
  {
    id: 1,
    title: "Accueil",
    path: "/",
    newTab: false,
  },
  {
    id: 2,
    title: "Dashboard",
    path: "/dashboard",
    newTab: false,
  },
  {
    id: 3,
    title: "Résultats",
    path: "/results",
    newTab: false,
  },
  {
    id: 4,
    title: "Paramètres",
    path: "/settings",
    newTab: false,
  },
  {
    id: 5,
    title: "À propos",
    path: "/about",
    newTab: false,
  },
  {
    id: 6,
    title: "Contact",
    path: "/contact",
    newTab: false,
  },
  {
    id: 7,
    title: "Blog",
    path: "/blogs",
    newTab: false,
  },
  {
    id: 8,
    title: "Pages",
    newTab: false,
    submenu: [
      {
        id: 81,
        title: "Dashboard",
        path: "/dashboard",
        newTab: false,
      },
      {
        id: 82,
        title: "Résultats",
        path: "/results",
        newTab: false,
      },
      {
        id: 83,
        title: "Paramètres",
        path: "/settings",
        newTab: false,
      },
      {
        id: 84,
        title: "À propos",
        path: "/about",
        newTab: false,
      },
      {
        id: 85,
        title: "Contact",
        path: "/contact",
        newTab: false,
      },
      {
        id: 86,
        title: "Blog",
        path: "/blogs",
        newTab: false,
      },
      {
        id: 87,
        title: "Inscription",
        path: "/signup",
        newTab: false,
      },
      {
        id: 88,
        title: "Connexion",
        path: "/signin",
        newTab: false,
      },
      {
        id: 89,
        title: "Erreur",
        path: "/error",
        newTab: false,
      },
    ],
  },
];
export default menuData;
