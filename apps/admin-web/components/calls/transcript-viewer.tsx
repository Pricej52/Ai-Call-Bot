"use client";

import { useEffect, useState } from "react";
import { getCall } from "@/lib/api/admin-api";
import { CallLogDetail } from "@/types/api";

export function TranscriptViewer({ callId }: { callId: string }) {
  const [call, setCall] = useState<CallLogDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getCall(callId);
        setCall(data);
      } catch (err) {
        console.error(err);
        setError("Failed to load transcript.");
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, [callId]);

  if (loading) return <p className="text-sm text-slate-600">Loading transcript...</p>;
  if (error) return <p className="text-sm text-red-600">{error}</p>;
  if (!call) return <p className="text-sm text-slate-600">No call found.</p>;

  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6">
      <h2 className="mb-2 text-lg font-semibold">Transcript</h2>
      <p className="mb-1 text-sm text-slate-500">Call SID: {call.provider_call_sid}</p>
      <p className="mb-4 text-sm text-slate-500">Status: {call.status}</p>
      <div className="space-y-3 text-sm text-slate-700">
        {call.transcript_entries.map((entry) => (
          <p key={entry.id}>
            <strong className="capitalize">{entry.speaker}:</strong> {entry.content}
          </p>
        ))}
        {call.transcript_entries.length === 0 ? <p>No transcript entries yet.</p> : null}
      </div>
    </div>
  );
}
