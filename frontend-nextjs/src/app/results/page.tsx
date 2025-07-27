"use client";

import Navigation from "@/components/Navigation";
import {
  Card,
  CardBody,
  CardHeader,
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  Button,
  Input,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Chip,
  Pagination,
  Select,
  SelectItem,
} from "@heroui/react";
import { useState } from "react";

// Données de démonstration
const mockData = [
  {
    id: 1,
    sourcePage: "https://example.com/guide-seo",
    anchor: "optimisation référencement",
    targetPage: "https://example.com/techniques-seo",
    similarityScore: 0.95,
    status: "approved"
  },
  {
    id: 2,
    sourcePage: "https://example.com/blog/marketing-digital",
    anchor: "stratégies marketing",
    targetPage: "https://example.com/strategies-marketing",
    similarityScore: 0.87,
    status: "pending"
  },
  {
    id: 3,
    sourcePage: "https://example.com/services/consulting",
    anchor: "conseil expert",
    targetPage: "https://example.com/experts-consulting",
    similarityScore: 0.92,
    status: "approved"
  },
  {
    id: 4,
    sourcePage: "https://example.com/contact",
    anchor: "nous contacter",
    targetPage: "https://example.com/equipe",
    similarityScore: 0.78,
    status: "rejected"
  },
  {
    id: 5,
    sourcePage: "https://example.com/produits/logiciel-seo",
    anchor: "outil SEO avancé",
    targetPage: "https://example.com/outils-seo",
    similarityScore: 0.89,
    status: "approved"
  }
];

export default function Results() {
  const [filterValue, setFilterValue] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [page, setPage] = useState(1);
  const rowsPerPage = 10;

  const filteredData = mockData.filter((item) => {
    const matchesSearch = item.sourcePage.toLowerCase().includes(filterValue.toLowerCase()) ||
                         item.targetPage.toLowerCase().includes(filterValue.toLowerCase()) ||
                         item.anchor.toLowerCase().includes(filterValue.toLowerCase());
    
    const matchesStatus = statusFilter === "all" || item.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  const pages = Math.ceil(filteredData.length / rowsPerPage);
  const items = filteredData.slice((page - 1) * rowsPerPage, page * rowsPerPage);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved":
        return "success";
      case "pending":
        return "warning";
      case "rejected":
        return "danger";
      default:
        return "default";
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case "approved":
        return "Approuvé";
      case "pending":
        return "En attente";
      case "rejected":
        return "Rejeté";
      default:
        return status;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Navigation />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                Résultats de l'Analyse
              </h1>
              <p className="text-lg text-gray-600">
                Suggestions de maillage interne générées par l'IA
              </p>
            </div>
            <div className="flex gap-2">
              <Button
                color="primary"
                variant="bordered"
                startContent={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                }
              >
                Exporter CSV
              </Button>
              <Button
                color="primary"
                startContent={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                }
              >
                Nouvelle Analyse
              </Button>
            </div>
          </div>

          {/* Filtres */}
          <Card className="border-0 shadow-lg mb-6">
            <CardBody>
              <div className="flex flex-col md:flex-row gap-4">
                <Input
                  placeholder="Rechercher dans les résultats..."
                  value={filterValue}
                  onChange={(e) => setFilterValue(e.target.value)}
                  className="flex-1"
                  startContent={
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  }
                />
                <Select
                  placeholder="Statut"
                  selectedKeys={[statusFilter]}
                  onSelectionChange={(keys) => setStatusFilter(Array.from(keys)[0] as string)}
                  className="w-full md:w-48"
                >
                  <SelectItem key="all">Tous les statuts</SelectItem>
                  <SelectItem key="approved">Approuvé</SelectItem>
                  <SelectItem key="pending">En attente</SelectItem>
                  <SelectItem key="rejected">Rejeté</SelectItem>
                </Select>
              </div>
            </CardBody>
          </Card>

          {/* Statistiques */}
          <div className="grid md:grid-cols-4 gap-4 mb-6">
            <Card className="border-0 shadow-lg">
              <CardBody className="text-center">
                <div className="text-2xl font-bold text-blue-600">{mockData.length}</div>
                <div className="text-sm text-gray-600">Total des suggestions</div>
              </CardBody>
            </Card>
            <Card className="border-0 shadow-lg">
              <CardBody className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {mockData.filter(item => item.status === "approved").length}
                </div>
                <div className="text-sm text-gray-600">Approuvées</div>
              </CardBody>
            </Card>
            <Card className="border-0 shadow-lg">
              <CardBody className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {mockData.filter(item => item.status === "pending").length}
                </div>
                <div className="text-sm text-gray-600">En attente</div>
              </CardBody>
            </Card>
            <Card className="border-0 shadow-lg">
              <CardBody className="text-center">
                <div className="text-2xl font-bold text-red-600">
                  {mockData.filter(item => item.status === "rejected").length}
                </div>
                <div className="text-sm text-gray-600">Rejetées</div>
              </CardBody>
            </Card>
          </div>

          {/* Tableau des résultats */}
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <h2 className="text-2xl font-semibold">Suggestions de Maillage Interne</h2>
            </CardHeader>
            <CardBody>
              <Table aria-label="Suggestions de maillage interne">
                <TableHeader>
                  <TableColumn>PAGE SOURCE</TableColumn>
                  <TableColumn>ANCRE GÉNÉRÉE</TableColumn>
                  <TableColumn>PAGE CIBLE</TableColumn>
                  <TableColumn>SCORE</TableColumn>
                  <TableColumn>STATUT</TableColumn>
                  <TableColumn>ACTIONS</TableColumn>
                </TableHeader>
                <TableBody emptyContent="Aucune suggestion trouvée">
                  {items.map((item) => (
                    <TableRow key={item.id}>
                      <TableCell>
                        <div className="max-w-xs truncate">
                          <a href={item.sourcePage} className="text-blue-600 hover:underline">
                            {item.sourcePage}
                          </a>
                        </div>
                      </TableCell>
                      <TableCell>
                        <span className="font-medium">{item.anchor}</span>
                      </TableCell>
                      <TableCell>
                        <div className="max-w-xs truncate">
                          <a href={item.targetPage} className="text-blue-600 hover:underline">
                            {item.targetPage}
                          </a>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Chip
                          color={item.similarityScore > 0.9 ? "success" : item.similarityScore > 0.8 ? "warning" : "danger"}
                          variant="flat"
                        >
                          {(item.similarityScore * 100).toFixed(0)}%
                        </Chip>
                      </TableCell>
                      <TableCell>
                        <Chip
                          color={getStatusColor(item.status)}
                          variant="flat"
                        >
                          {getStatusText(item.status)}
                        </Chip>
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Button size="sm" variant="bordered">
                            Approuver
                          </Button>
                          <Button size="sm" color="danger" variant="bordered">
                            Rejeter
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              
              {pages > 1 && (
                <div className="flex justify-center mt-4">
                  <Pagination
                    total={pages}
                    page={page}
                    onChange={setPage}
                    showControls
                  />
                </div>
              )}
            </CardBody>
          </Card>
        </div>
      </main>
    </div>
  );
} 