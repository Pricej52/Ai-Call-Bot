"use client";

import { useCallback, useEffect, useState } from "react";
import { deleteAgent, listAgents } from "@/lib/api/admin-api";
import { getErrorMessage } from "@/lib/api/errors";
import { Agent } from "@/types/api";

const TENANT_ID = process.env.NEXT_PUBLIC_TENANT_ID;

export function useAgents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    if (!TENANT_ID) {
      setError("Missing NEXT_PUBLIC_TENANT_ID. Configure it to load agents.");
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await listAgents(TENANT_ID);
      setAgents(data);
    } catch (err) {
      setError(getErrorMessage(err, "Failed to load agents."));
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const remove = useCallback(async (agentId: string) => {
    await deleteAgent(agentId);
    await load();
  }, [load]);

  useEffect(() => {
    void load();
  }, [load]);

  return { agents, loading, error, reload: load, remove };
}
