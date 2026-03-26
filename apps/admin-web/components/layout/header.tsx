export function Header() {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 md:px-6">
      <p className="text-sm text-slate-600">Manage your agents, campaigns, and calls.</p>
      <button className="rounded-md border border-slate-200 px-3 py-2 text-sm font-medium">Admin User</button>
    </header>
  );
}
