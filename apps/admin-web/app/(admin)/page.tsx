import { PageHeader } from "@/components/common/page-header";
import { StatsCards } from "@/components/dashboard/stats-cards";

export default function DashboardPage() {
  return (
    <div>
      <PageHeader title="Dashboard" description="Overview of your AI voice agent platform." />
      <StatsCards />
    </div>
  );
}
