"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { updateAgent } from "@/lib/api/admin-api";

export function EditAgentForm({ agentId }: { agentId: string }) {
  const router = useRouter();
  const [name, setName] = useState("");
  const [voice, setVoice] = useState("alloy");
  const [language, setLanguage] = useState("en");
  const [loading, setLoading] = useState(false);

  return (
    <form
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-6"
      onSubmit={async (event) => {
        event.preventDefault();
        setLoading(true);
        try {
          await updateAgent(agentId, { name, voice, language });
          router.push("/agents");
        } catch (error) {
          console.error(error);
          alert("Failed to update agent.");
        } finally {
          setLoading(false);
        }
      }}
    >
      <div>
        <Label>Name</Label>
        <Input value={name} onChange={(event) => setName(event.target.value)} required />
      </div>
      <div>
        <Label>Voice</Label>
        <Input value={voice} onChange={(event) => setVoice(event.target.value)} required />
      </div>
      <div>
        <Label>Language</Label>
        <Input value={language} onChange={(event) => setLanguage(event.target.value)} required />
      </div>
      <Button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Save Changes"}
      </Button>
    </form>
  );
}
