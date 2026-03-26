"use client";

import Link from "next/link";
import { useState } from "react";
import { useAgents } from "@/features/agents/use-agents";
import { Button } from "@/components/ui/button";

export function AgentsTable() {
  const { agents, loading, error, remove } = useAgents();
  const [deletingId, setDeletingId] = useState<string | null>(null);

  if (loading) return <p className="text-sm text-slate-600">Loading agents...</p>;
  if (error) return <p className="text-sm text-red-600">{error}</p>;

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="min-w-full divide-y divide-slate-200 text-sm">
        <thead className="bg-slate-50">
          <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Type</th>
            <th className="px-4 py-3 text-left">Language</th>
            <th className="px-4 py-3 text-left">Voice</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {agents.map((agent) => (
            <tr key={agent.id}>
              <td className="px-4 py-3">{agent.name}</td>
              <td className="px-4 py-3 capitalize">{agent.type}</td>
              <td className="px-4 py-3">{agent.language}</td>
              <td className="px-4 py-3">{agent.voice}</td>
              <td className="px-4 py-3">
                <span
                  className={`rounded-full px-2 py-1 text-xs font-medium ${
                    agent.is_published ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"
                  }`}
                >
                  {agent.is_published ? "Published" : "Draft"}
                </span>
              </td>
              <td className="px-4 py-3 text-right">
                <div className="flex justify-end gap-2">
                  <Link href={`/agents/${agent.id}`} className="text-blue-600 hover:underline">
                    View
                  </Link>
                  <Button
                    size="sm"
                    variant="destructive"
                    disabled={deletingId === agent.id}
                    onClick={async () => {
                      setDeletingId(agent.id);
                      try {
                        await remove(agent.id);
                      } catch {
                        alert("Delete failed");
                      } finally {
                        setDeletingId(null);
                      }
                    }}
                  >
                    Delete
                  </Button>
                </div>
              </td>
            </tr>
          ))}
          {agents.length === 0 ? (
            <tr>
              <td className="px-4 py-6 text-center text-slate-500" colSpan={6}>
                No agents found.
              </td>
            </tr>
          ) : null}
        </tbody>
      </table>
    </div>
  );
}
