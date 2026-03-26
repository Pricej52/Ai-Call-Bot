"use client";

import { useEffect, useState } from "react";
import { getDashboardStats } from "@/lib/api/admin-api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const TENANT_ID = process.env.NEXT_PUBLIC_TENANT_ID ?? "00000000-0000-0000-0000-000000000000";

export function StatsCards() {
  const [stats, setStats] = useState({ total_calls: 0, total_agents: 0, total_campaigns: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getDashboardStats(TENANT_ID);
        setStats(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  const cards = [
    { title: "Total Calls", value: stats.total_calls },
    { title: "Total Agents", value: stats.total_agents },
    { title: "Total Campaigns", value: stats.total_campaigns },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {cards.map((stat) => (
        <Card key={stat.title}>
          <CardHeader>
            <CardTitle className="text-sm font-medium text-slate-600">{stat.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-semibold">{loading ? "..." : stat.value}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
