"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { createAgent } from "@/lib/api/admin-api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

const schema = z.object({
  type: z.enum(["inbound", "outbound"]),
  name: z.string().min(2, "Name is required"),
  phone_number_id: z.string().optional(),
  twilioPhoneNumber: z.string().optional(),
  voice: z.string().min(1),
  language: z.string().min(2),
  prompt: z.string().min(10, "Prompt should be at least 10 characters"),
  talkTracks: z.string().min(3, "Talk tracks are required"),
  ctaText: z.string().min(2, "CTA text is required"),
  ctaAction: z.string().min(2, "CTA action is required"),
  voicemailEnabled: z.boolean().default(false),
  voicemailMessage: z.string().optional(),
  webhookUrl: z.string().url("Webhook URL must be valid"),
  status: z.enum(["draft", "published"]).default("draft"),
});

type WizardValues = z.infer<typeof schema>;

const tenantId = process.env.NEXT_PUBLIC_TENANT_ID ?? "00000000-0000-0000-0000-000000000000";
const clientId = process.env.NEXT_PUBLIC_CLIENT_ID ?? "00000000-0000-0000-0000-000000000000";

export function CreateAgentWizard() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const form = useForm<WizardValues>({
    resolver: zodResolver(schema),
    defaultValues: {
      type: "inbound",
      name: "",
      phone_number_id: "",
      twilioPhoneNumber: "",
      voice: "alloy",
      language: "en",
      prompt: "",
      talkTracks: "",
      ctaText: "",
      ctaAction: "",
      voicemailEnabled: false,
      voicemailMessage: "",
      webhookUrl: "",
      status: "draft",
    },
    mode: "onBlur",
  });

  const values = form.watch();
  const canGoNext = useMemo(() => {
    if (step === 1) return !!values.type;
    if (step === 2) return !!values.name && !!values.voice && !!values.language;
    if (step === 3) return !!values.prompt && !!values.talkTracks && !!values.webhookUrl;
    return true;
  }, [step, values]);

  const onSubmit = form.handleSubmit(async (data) => {
    try {
      setIsSubmitting(true);
      setError(null);
      await createAgent({
        tenant_id: tenantId,
        client_account_id: clientId,
        type: data.type,
        name: data.name,
        phone_number_id: data.phone_number_id,
        twilio_phone_number: data.twilioPhoneNumber,
        language: data.language,
        voice: data.voice,
        base_prompt: data.prompt,
        talk_tracks: data.talkTracks,
        cta_instructions: `${data.ctaText} (${data.ctaAction})`,
        voicemail_behavior: data.voicemailEnabled ? data.voicemailMessage : "disabled",
        webhook_url: data.webhookUrl,
        status: data.status,
      });
      router.push("/agents");
    } catch (submitError) {
      console.error(submitError);
      setError("Failed to create agent. Please review your inputs and try again.");
    } finally {
      setIsSubmitting(false);
    }
  });

  return (
    <form className="space-y-6 rounded-lg border border-slate-200 bg-white p-6" onSubmit={onSubmit}>
      <div className="text-sm font-medium text-slate-600">Step {step} of 4</div>

      {step === 1 ? (
        <div className="space-y-2">
          <Label>Agent Type</Label>
          <Select
            options={[
              { label: "Inbound", value: "inbound" },
              { label: "Outbound", value: "outbound" },
            ]}
            {...form.register("type")}
          />
        </div>
      ) : null}

      {step === 2 ? (
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <Label>Name</Label>
            <Input {...form.register("name")} />
            <p className="mt-1 text-xs text-red-600">{form.formState.errors.name?.message}</p>
          </div>
          <div>
            <Label>Phone Number ID</Label>
            <Input {...form.register("phone_number_id")} />
          </div>
          <div>
            <Label>Twilio Phone Number (E.164)</Label>
            <Input {...form.register("twilioPhoneNumber")} placeholder="+15551234567" />
          </div>
          <div>
            <Label>Voice</Label>
            <Input {...form.register("voice")} />
          </div>
          <div>
            <Label>Language</Label>
            <Input {...form.register("language")} />
          </div>
        </div>
      ) : null}

      {step === 3 ? (
        <div className="space-y-4">
          <div>
            <Label>Prompt Editor</Label>
            <Textarea {...form.register("prompt")} />
            <p className="mt-1 text-xs text-red-600">{form.formState.errors.prompt?.message}</p>
          </div>
          <div>
            <Label>Talk Tracks</Label>
            <Textarea {...form.register("talkTracks")} />
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <Label>CTA Text</Label>
              <Input {...form.register("ctaText")} />
            </div>
            <div>
              <Label>CTA Action</Label>
              <Input {...form.register("ctaAction")} />
            </div>
          </div>
          <div className="space-y-2">
            <Label className="flex items-center gap-2">
              <input type="checkbox" {...form.register("voicemailEnabled")} /> Enable voicemail
            </Label>
            <Textarea {...form.register("voicemailMessage")} placeholder="Voicemail message" />
          </div>
          <div>
            <Label>Webhook URL</Label>
            <Input {...form.register("webhookUrl")} placeholder="https://..." />
            <p className="mt-1 text-xs text-red-600">{form.formState.errors.webhookUrl?.message}</p>
          </div>
          <div>
            <Label>Status</Label>
            <Select
              options={[
                { label: "Draft", value: "draft" },
                { label: "Published (test-ready)", value: "published" },
              ]}
              {...form.register("status")}
            />
          </div>
        </div>
      ) : null}

      {step === 4 ? (
        <div className="space-y-2 rounded-md bg-slate-50 p-4 text-sm">
          <p>
            <strong>Type:</strong> {values.type}
          </p>
          <p>
            <strong>Name:</strong> {values.name}
          </p>
          <p>
            <strong>Voice:</strong> {values.voice}
          </p>
          <p>
            <strong>Language:</strong> {values.language}
          </p>
          <p>
            <strong>Webhook:</strong> {values.webhookUrl}
          </p>
        </div>
      ) : null}

      {error ? <p className="text-sm text-red-600">{error}</p> : null}

      <div className="flex justify-between">
        <Button type="button" variant="outline" onClick={() => setStep((prev) => Math.max(1, prev - 1))}>
          Previous
        </Button>

        {step < 4 ? (
          <Button type="button" onClick={() => setStep((prev) => prev + 1)} disabled={!canGoNext}>
            Next
          </Button>
        ) : (
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Agent"}
          </Button>
        )}
      </div>
    </form>
  );
}
