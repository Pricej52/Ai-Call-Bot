import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const stats = [
  { title: "Total Calls", value: "1,248" },
  { title: "Active Agents", value: "12" },
  { title: "Live Campaigns", value: "8" },
];

export function StatsCards() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {stats.map((stat) => (
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
