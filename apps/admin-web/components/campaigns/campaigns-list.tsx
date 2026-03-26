import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const campaignRows = [
  { name: "Spring Renewals", leads: 320, status: "Active" },
  { name: "Missed Appointments", leads: 140, status: "Draft" },
];

export function CampaignsList() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Campaign List</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500">
                <th className="pb-2">Name</th>
                <th className="pb-2">Leads</th>
                <th className="pb-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {campaignRows.map((campaign) => (
                <tr key={campaign.name} className="border-t border-slate-100">
                  <td className="py-2">{campaign.name}</td>
                  <td className="py-2">{campaign.leads}</td>
                  <td className="py-2">{campaign.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
