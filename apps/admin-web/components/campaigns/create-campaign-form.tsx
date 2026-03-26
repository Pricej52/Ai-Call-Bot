"use client";

import { useState } from "react";
import { createCampaign } from "@/lib/api/admin-api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

export function CreateCampaignForm() {
  const [name, setName] = useState("");
  const [leads, setLeads] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <form
      className="space-y-4 rounded-lg border border-slate-200 bg-white p-6"
      onSubmit={async (event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        try {
          await createCampaign({ name, leads });
          setName("");
          setLeads("");
        } catch (createError) {
          console.error(createError);
          setError("Campaign endpoint is unavailable or failed.");
        } finally {
          setLoading(false);
        }
      }}
    >
      <div>
        <Label>Campaign Name</Label>
        <Input value={name} onChange={(event) => setName(event.target.value)} required />
      </div>
      <div>
        <Label>Leads Placeholder</Label>
        <Textarea
          value={leads}
          onChange={(event) => setLeads(event.target.value)}
          placeholder="Paste lead identifiers, CSV notes, etc."
          required
        />
      </div>
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <Button type="submit" disabled={loading}>
        {loading ? "Creating..." : "Create Campaign"}
      </Button>
    </form>
  );
}
