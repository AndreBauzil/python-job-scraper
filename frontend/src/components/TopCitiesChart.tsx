// frontend/src/components/TopCitiesChart.tsx
import { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";

interface CityData {
  city: string;
  jobs: number;
}

export function TopCitiesChart() {
  const [data, setData] = useState<CityData[]>([]);

  useEffect(() => {
    axios.get('http://localhost:8000/analytics/top-cities')
      .then(response => setData(response.data))
      .catch(err => console.error("Erro ao buscar dados do gráfico:", err));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top 5 Cidades</CardTitle>
        <CardDescription>Cidades com o maior número de vagas coletadas.</CardDescription>
      </CardHeader>
      <CardContent className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical">
            <XAxis type="number" hide />
            <YAxis
              type="category"
              dataKey="city"
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              width={150}
            />
            <Tooltip
              cursor={{ fill: 'transparent' }}
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-card p-2 border rounded-lg shadow-sm">
                      <p className="font-bold">{`${payload[0].payload.city}`}</p>
                      <p className="text-sm">{`Vagas: ${payload[0].value}`}</p>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Bar dataKey="jobs" fill="hsl(var(--primary))" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}