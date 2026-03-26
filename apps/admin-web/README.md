# Admin Web

Next.js admin frontend for the AI voice agent platform.

## Run locally

```bash
npm install
npm run dev
```

## Environment

Create `.env.local`:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_TENANT_ID=<tenant-uuid>
NEXT_PUBLIC_CLIENT_ID=<client-uuid>
```

Use `NEXT_PUBLIC_TENANT_ID` and `NEXT_PUBLIC_CLIENT_ID` values that exist in the API database so dashboards, agents, and call logs resolve to real persisted records.
