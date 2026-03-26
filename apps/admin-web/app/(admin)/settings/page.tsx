import { PageHeader } from "@/components/common/page-header";
import { TenantSettingsForm } from "@/components/settings/tenant-settings-form";

export default function SettingsPage() {
  return (
    <div>
      <PageHeader title="Settings" description="Configure tenant-level settings for your account." />
      <TenantSettingsForm />
    </div>
  );
}
