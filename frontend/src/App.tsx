// frontend/src/App.tsx
import { useState, useEffect, useMemo } from 'react';
import axios from 'axios';

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { TopCitiesChart } from './components/TopCitiesChart';


interface IJob {
  id: number;
  title: string;
  company: string;
  location: string;
  url: string;
}

function App() {
  const [jobs, setJobs] = useState<IJob[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [titleFilter, setTitleFilter] = useState("");
  const [companyFilter, setCompanyFilter] = useState("");

  useEffect(() => {
    setIsLoading(true);

    // Objeto com parâmetros de busca
    const params = new URLSearchParams();
    if (titleFilter) params.append('title', titleFilter);
    if (companyFilter) params.append('company', companyFilter);
    
    axios.get(`http://localhost:8000/vagas?${params.toString()}`)
    .then(response => {
      setJobs(response.data);
    })
    .catch(error => {
      console.error("Houve um erro ao buscar as vagas:", error);
    })
    .finally(() => {
      setIsLoading(false);
    });
  }, [titleFilter, companyFilter]);

  const stats = useMemo(() => {
    const totalJobs = jobs.length;
    const uniqueCompanies = new Set(jobs.map(job => job.company)).size;
    return { totalJobs, uniqueCompanies };
  }, [jobs]);

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="p-4 border-b">
        <h1 className="text-2xl font-bold container mx-auto">Job Scraper - Análise de Vagas</h1>
      </header>

      <main className="container mx-auto p-4 md:p-8">
        {/* Métricas */}
        <section className="grid gap-4 md:grid-cols-2 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>Total de Vagas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">{stats.totalJobs}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Empresas Contratando</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">{stats.uniqueCompanies}</div>
            </CardContent>
          </Card>
          <div className="md:col-span-3">
            <TopCitiesChart />
          </div>
        </section>

        {/* Filtros e Tabela */}
        <section>
          <h2 className="text-3xl font-bold mb-6">Vagas Coletadas</h2>

          <div className="flex gap-4 mb-4">
            <Input
              placeholder="Filtrar por título..."
              value={titleFilter}
              onChange={(e) => setTitleFilter(e.target.value)}
            />
            <Input
              placeholder="Filtrar por empresa..."
              value={companyFilter}
              onChange={(e) => setCompanyFilter(e.target.value)}
            />
          </div>

          <div className="border rounded-lg">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Título</TableHead>
                  <TableHead>Empresa</TableHead>
                  <TableHead>Localização</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center">Carregando vagas...</TableCell>
                  </TableRow>
                ) : jobs.map((job) => (
                  <TableRow key={job.id}>
                    <TableCell className="font-medium">
                      <a href={job.url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                        {job.title}
                      </a>
                    </TableCell>
                    <TableCell>{job.company}</TableCell>
                    <TableCell>{job.location}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;