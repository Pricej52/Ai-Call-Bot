export function TranscriptViewer({ callId }: { callId: string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6">
      <h2 className="mb-2 text-lg font-semibold">Transcript</h2>
      <p className="mb-4 text-sm text-slate-500">Call ID: {callId}</p>
      <div className="space-y-3 text-sm text-slate-700">
        <p>
          <strong>Agent:</strong> Hello! Thanks for calling. How can I help today?
        </p>
        <p>
          <strong>Caller:</strong> I want to reschedule my appointment.
        </p>
        <p>
          <strong>Agent:</strong> Absolutely — I can help with that.
        </p>
      </div>
    </div>
  );
}
