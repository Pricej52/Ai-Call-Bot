import { EditAgentForm } from "@/components/agents/edit-agent-form";
import { PageHeader } from "@/components/common/page-header";

export default async function EditAgentPage({ params }: { params: Promise<{ agentId: string }> }) {
  const { agentId } = await params;
  return (
    <div>
      <PageHeader title="Edit Agent" description="Update core details for your selected agent." />
      <EditAgentForm agentId={agentId} />
    </div>
  );
}
