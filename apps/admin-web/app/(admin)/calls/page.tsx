import { CallsTable } from "@/components/calls/calls-table";
import { PageHeader } from "@/components/common/page-header";

export default function CallsPage() {
  return (
    <div>
      <PageHeader title="Calls" description="Track call logs and inspect interaction outcomes." />
      <CallsTable />
    </div>
  );
}
