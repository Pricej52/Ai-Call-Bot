import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";

export function AdminShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50 md:flex">
      <Sidebar />
      <div className="flex-1">
        <Header />
        <main className="p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
