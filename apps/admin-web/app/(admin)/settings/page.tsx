import { PageHeader } from "@/components/common/page-header";
import { TenantSettingsForm } from "@/components/settings/tenant-settings-form";
import Link from "next/link";

export default function SettingsPage() {
  return (
    <div className="space-y-4">
      <PageHeader title="Settings" description="Configure tenant-level settings for your account." />
      <div className="rounded-lg border border-slate-200 bg-white p-4">
        <h3 className="text-base font-semibold">Integrations</h3>
        <p className="text-sm text-slate-600">Manage provider connections for this tenant.</p>
        <Link href="/settings/integrations/twilio" className="mt-2 inline-block text-sm text-blue-600 underline">
          Open Twilio Integration
        </Link>
      </div>
      <TenantSettingsForm />
    </div>
  );
}
