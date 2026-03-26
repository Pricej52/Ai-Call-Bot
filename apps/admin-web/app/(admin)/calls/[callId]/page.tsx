import { TranscriptViewer } from "@/components/calls/transcript-viewer";
import { PageHeader } from "@/components/common/page-header";

export default async function TranscriptPage({ params }: { params: Promise<{ callId: string }> }) {
  const { callId } = await params;
  return (
    <div>
      <PageHeader title="Call Transcript" description="Detailed transcript and call summary." />
      <TranscriptViewer callId={callId} />
    </div>
  );
}
