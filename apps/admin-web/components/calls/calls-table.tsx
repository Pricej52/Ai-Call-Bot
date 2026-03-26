"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listCalls } from "@/lib/api/admin-api";
import { getErrorMessage } from "@/lib/api/errors";
import { CallLog } from "@/types/api";

const TENANT_ID = process.env.NEXT_PUBLIC_TENANT_ID;

export function CallsTable() {
  const [calls, setCalls] = useState<CallLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!TENANT_ID) {
        setError("Missing NEXT_PUBLIC_TENANT_ID. Configure it to load calls.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const data = await listCalls(TENANT_ID);
        setCalls(data);
      } catch (loadError) {
        console.error(loadError);
        setError(getErrorMessage(loadError, "Failed to load call logs."));
      } finally {
        setLoading(false);
      }
    };

    void load();
  }, []);

  if (loading) return <p className="text-sm text-slate-600">Loading call logs...</p>;
  if (error) return <p className="text-sm text-red-600">{error}</p>;

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left">Call SID</th>
            <th className="px-4 py-3 text-left">From</th>
            <th className="px-4 py-3 text-left">To</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-right">Transcript</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {calls.map((call) => (
            <tr key={call.id}>
              <td className="px-4 py-3">{call.provider_call_sid}</td>
              <td className="px-4 py-3">{call.from_number}</td>
              <td className="px-4 py-3">{call.to_number}</td>
              <td className="px-4 py-3 capitalize">{call.status}</td>
              <td className="px-4 py-3 text-right">
                <Link href={`/calls/${call.id}`} className="text-blue-600 hover:underline">
                  View
                </Link>
              </td>
            </tr>
          ))}
          {calls.length === 0 ? (
            <tr>
              <td className="px-4 py-6 text-center text-slate-500" colSpan={5}>
                No call logs available.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}
