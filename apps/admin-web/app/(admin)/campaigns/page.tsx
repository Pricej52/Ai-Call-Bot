import { CreateCampaignForm } from "@/components/campaigns/create-campaign-form";
import { CampaignsList } from "@/components/campaigns/campaigns-list";
import { PageHeader } from "@/components/common/page-header";

export default function CampaignsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Campaigns" description="Create and manage campaign batches." />
      <CampaignsList />
      <CreateCampaignForm />
    </div>
  );
}
