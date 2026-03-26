"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { getAgent, updateAgent } from "@/lib/api/admin-api";
import { Agent } from "@/types/api";

export function EditAgentForm({ agentId }: { agentId: string }) {
  const router = useRouter();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getAgent(agentId);
        setAgent(data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    void load();
  }, [agentId]);

  if (loading) return <p className="text-sm text-slate-600">Loading agent...</p>;
  if (!agent) return <p className="text-sm text-red-600">Agent not found.</p>;

  return (
    <form
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-6"
      onSubmit={async (event) => {
        event.preventDefault();
        setSaving(true);
        try {
          await updateAgent(agentId, {
            name: agent.name,
            voice: agent.voice,
            language: agent.language,
            twilio_phone_number: agent.twilio_phone_number ?? "",
            base_prompt: agent.base_prompt ?? "",
            talk_tracks: agent.talk_tracks ?? "",
            cta_instructions: agent.cta_instructions ?? "",
            voicemail_behavior: agent.voicemail_behavior ?? "",
            webhook_url: agent.webhook_url ?? "",
            status: agent.is_published ? "published" : "draft",
          });
          router.refresh();
        } catch (error) {
          console.error(error);
          alert("Failed to update agent.");
        } finally {
          setSaving(false);
        }
      }}
    >
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label>Name</Label>
          <Input value={agent.name} onChange={(event) => setAgent({ ...agent, name: event.target.value })} required />
        </div>
        <div>
          <Label>Twilio Number</Label>
          <Input
            value={agent.twilio_phone_number ?? ""}
            onChange={(event) => setAgent({ ...agent, twilio_phone_number: event.target.value })}
          />
        </div>
        <div>
          <Label>Voice</Label>
          <Input value={agent.voice} onChange={(event) => setAgent({ ...agent, voice: event.target.value })} required />
        </div>
        <div>
          <Label>Language</Label>
          <Input
            value={agent.language}
            onChange={(event) => setAgent({ ...agent, language: event.target.value })}
            required
          />
        </div>
      </div>
      <div>
        <Label>Base Prompt</Label>
        <Textarea
          value={agent.base_prompt ?? ""}
          onChange={(event) => setAgent({ ...agent, base_prompt: event.target.value })}
        />
      </div>
      <div>
        <Label>Talk Tracks / Objections</Label>
        <Textarea
          value={agent.talk_tracks ?? ""}
          onChange={(event) => setAgent({ ...agent, talk_tracks: event.target.value })}
        />
      </div>
      <div>
        <Label>CTA Instructions</Label>
        <Textarea
          value={agent.cta_instructions ?? ""}
          onChange={(event) => setAgent({ ...agent, cta_instructions: event.target.value })}
        />
      </div>
      <div>
        <Label>Webhook URL</Label>
        <Input
          value={agent.webhook_url ?? ""}
          onChange={(event) => setAgent({ ...agent, webhook_url: event.target.value })}
        />
      </div>
      <Label className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={agent.is_published}
          onChange={(event) => setAgent({ ...agent, is_published: event.target.checked })}
        />
        Published (test-ready)
      </Label>
      <Button type="submit" disabled={saving}>
        {saving ? "Saving..." : "Save Changes"}
      </Button>
    </form>
  );
}
