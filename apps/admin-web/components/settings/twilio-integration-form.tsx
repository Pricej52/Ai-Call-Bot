"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  connectTwilioIntegration,
  disconnectTwilioIntegration,
  getTwilioIntegration,
  listTenantTwilioNumbers,
  testTwilioIntegration,
  updateTwilioIntegration,
} from "@/lib/api/admin-api";
import { TwilioIntegration } from "@/types/api";

const tenantId = process.env.NEXT_PUBLIC_TENANT_ID ?? "00000000-0000-0000-0000-000000000000";
const clientId = process.env.NEXT_PUBLIC_CLIENT_ID ?? "00000000-0000-0000-0000-000000000000";

export function TwilioIntegrationForm() {
  const [integration, setIntegration] = useState<TwilioIntegration | null>(null);
  const [accountSid, setAccountSid] = useState("");
  const [authToken, setAuthToken] = useState("");
  const [defaultPhoneNumber, setDefaultPhoneNumber] = useState("");
  const [numbers, setNumbers] = useState<string[]>([]);
  const [message, setMessage] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const loadIntegration = async () => {
    const data = await getTwilioIntegration(tenantId);
    setIntegration(data);
    setAccountSid(data?.account_sid ?? "");
    setDefaultPhoneNumber(data?.default_phone_number ?? "");
  };

  useEffect(() => {
    void loadIntegration();
  }, []);

  const onSave = async () => {
    setLoading(true);
    setMessage("");
    try {
      if (!integration) {
        await connectTwilioIntegration({
          tenant_id: tenantId,
          account_sid: accountSid,
          auth_token: authToken,
          default_phone_number: defaultPhoneNumber,
        });
        setMessage("Twilio credentials saved.");
      } else {
        await updateTwilioIntegration({
          tenant_id: tenantId,
          account_sid: accountSid || undefined,
          auth_token: authToken || undefined,
          default_phone_number: defaultPhoneNumber || undefined,
        });
        setMessage("Twilio credentials updated.");
      }
      setAuthToken("");
      await loadIntegration();
    } catch (error) {
      console.error(error);
      setMessage("Failed to save Twilio settings.");
    } finally {
      setLoading(false);
    }
  };

  const onTest = async () => {
    setLoading(true);
    setMessage("");
    try {
      const data = await testTwilioIntegration(tenantId);
      setNumbers(data.numbers);
      setMessage(`${data.message} (${data.numbers.length} numbers found)`);
      await loadIntegration();
    } catch (error) {
      console.error(error);
      setMessage("Twilio connection test failed.");
    } finally {
      setLoading(false);
    }
  };

  const onFetchNumbers = async () => {
    setLoading(true);
    try {
      const fetched = await listTenantTwilioNumbers(tenantId, clientId);
      setNumbers(fetched);
      setMessage(`Fetched ${fetched.length} phone numbers from Twilio.`);
    } catch (error) {
      console.error(error);
      setMessage("Failed to fetch phone numbers.");
    } finally {
      setLoading(false);
    }
  };

  const onDisconnect = async () => {
    if (!confirm("Disconnect Twilio for this tenant? Existing agent number mappings remain saved.")) return;
    setLoading(true);
    try {
      await disconnectTwilioIntegration(tenantId);
      setIntegration(null);
      setAccountSid("");
      setAuthToken("");
      setDefaultPhoneNumber("");
      setNumbers([]);
      setMessage("Twilio integration disconnected.");
    } catch (error) {
      console.error(error);
      setMessage("Failed to disconnect Twilio.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4 rounded-lg border border-slate-200 bg-white p-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Twilio Integration</h3>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
          {integration?.status ?? "not_configured"}
        </span>
      </div>

      <div>
        <Label>Twilio Account SID</Label>
        <Input value={accountSid} onChange={(e) => setAccountSid(e.target.value)} placeholder="AC..." />
      </div>
      <div>
        <Label>Twilio Auth Token {integration ? "(enter to rotate)" : ""}</Label>
        <Input
          type="password"
          value={authToken}
          onChange={(e) => setAuthToken(e.target.value)}
          placeholder={integration ? integration.masked_auth_token : "••••••••"}
        />
      </div>
      <div>
        <Label>Default Twilio Number (optional)</Label>
        <Input value={defaultPhoneNumber} onChange={(e) => setDefaultPhoneNumber(e.target.value)} placeholder="+15551234567" />
      </div>

      <div className="flex flex-wrap gap-2">
        <Button onClick={onSave} disabled={loading || !accountSid || (!integration && !authToken)}>
          {integration ? "Update Credentials" : "Connect Twilio"}
        </Button>
        <Button variant="outline" onClick={onTest} disabled={loading || !integration}>
          Test Connection
        </Button>
        <Button variant="outline" onClick={onFetchNumbers} disabled={loading || !integration}>
          Fetch Numbers
        </Button>
        <Button variant="outline" onClick={onDisconnect} disabled={loading || !integration}>
          Disconnect
        </Button>
      </div>

      {message ? <p className="text-sm text-slate-700">{message}</p> : null}

      {numbers.length > 0 ? (
        <div>
          <p className="mb-1 text-sm font-medium">Available Numbers</p>
          <ul className="list-disc space-y-1 pl-6 text-sm text-slate-700">
            {numbers.map((number) => (
              <li key={number}>{number}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}
