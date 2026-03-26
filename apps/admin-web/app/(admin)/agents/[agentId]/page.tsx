import { EditAgentForm } from "@/components/agents/edit-agent-form";
import { PageHeader } from "@/components/common/page-header";

export default async function EditAgentPage({ params }: { params: Promise<{ agentId: string }> }) {
  const { agentId } = await params;
  return (
    <div>
      <PageHeader title="Agent Detail" description="Inspect full configuration and set publish/test-ready status." />
      <EditAgentForm agentId={agentId} />
    </div>
  );
}
