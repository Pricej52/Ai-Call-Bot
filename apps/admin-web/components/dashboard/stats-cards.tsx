"use client";

import { useEffect, useState } from "react";
import { getDashboardStats } from "@/lib/api/admin-api";
import { getErrorMessage } from "@/lib/api/errors";
import { DashboardStats } from "@/types/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const TENANT_ID = process.env.NEXT_PUBLIC_TENANT_ID;

export function StatsCards() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!TENANT_ID) {
        setError("Missing NEXT_PUBLIC_TENANT_ID. Configure it to load dashboard stats.");
        setLoading(false);
        return;
      }

      try {
        setError(null);
        const data = await getDashboardStats(TENANT_ID);
        setStats(data);
      } catch (loadError) {
        console.error(loadError);
        setError(getErrorMessage(loadError, "Failed to load dashboard stats."));
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, []);

  if (loading) {
    return <p className="text-sm text-slate-600">Loading dashboard stats...</p>;
  }

  if (error) {
    return <p className="text-sm text-red-600">{error}</p>;
  }

  if (!stats) {
    return <p className="text-sm text-slate-600">No dashboard stats available yet.</p>;
  }

  const hasNoActivity = stats.total_calls === 0 && stats.total_agents === 0 && stats.total_campaigns === 0;
  if (hasNoActivity) {
    return (
      <p className="rounded-lg border border-slate-200 bg-white p-6 text-sm text-slate-600">
        No activity yet. Create an agent or place a call to populate dashboard metrics.
      </p>
    );
  }

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
            <p className="text-3xl font-semibold">{stat.value}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
