import Link from "next/link";
import { AgentsTable } from "@/components/agents/agents-table";
import { PageHeader } from "@/components/common/page-header";
import { Button } from "@/components/ui/button";

export default function AgentsPage() {
  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <PageHeader title="Agents" description="Manage inbound and outbound AI agents." />
        <Link href="/agents/create">
          <Button>Create Agent</Button>
        </Link>
      </div>
      <AgentsTable />
    </div>
  );
}
