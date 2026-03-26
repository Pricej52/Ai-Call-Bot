import Link from "next/link";
import { PageHeader } from "@/components/common/page-header";
import { TwilioIntegrationForm } from "@/components/settings/twilio-integration-form";

export default function TwilioIntegrationPage() {
  return (
    <div className="space-y-4">
      <PageHeader title="Settings / Integrations / Twilio" description="Connect and manage your tenant Twilio account." />
      <p className="text-sm text-slate-600">
        Need general settings?{" "}
        <Link href="/settings" className="text-blue-600 underline">
          Go back to Settings
        </Link>
      </p>
      <TwilioIntegrationForm />
    </div>
  );
}
