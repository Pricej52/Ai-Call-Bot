import { PageHeader } from "@/components/common/page-header";
import { CreateAgentWizard } from "@/components/agents/create-agent-wizard";

export default function CreateAgentPage() {
  return (
    <div>
      <PageHeader title="Create Agent" description="Use the 4-step wizard to configure your new AI agent." />
      <CreateAgentWizard />
    </div>
  );
}
