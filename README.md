# AI Call Bot - Voice Backend Foundation

## Run locally

1. Create a virtual environment and install deps:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start the API:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Verify health:
   ```bash
   curl http://127.0.0.1:8000/health
   ```

## Endpoints

- `POST /webhooks/twilio/voice/inbound`
- `POST /calls/outbound-jobs`
- `GET /health`

## Run tests

```bash
pytest -q
```

## Operational verification (local + Docker)

Run the automated readiness check:

```bash
bash scripts/verify_operational.sh
```

What it validates:
- Required toolchain (Python, Node.js, Docker CLI when present)
- Docker Compose configuration validity
- Python dependency install + root tests
- `apps/api` dependency install + import smoke test
- `apps/admin-web` dependency install + lint + build

## End-to-end inbound voice test setup (Twilio + local)

### Required environment variables

Backend (`apps/api/.env`):

```bash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=aicallbot
REDIS_URL=redis://localhost:6379/0

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+15551234567
PUBLIC_WEBHOOK_BASE_URL=https://<your-ngrok-subdomain>.ngrok-free.app

OPENAI_API_KEY=sk-...
```

Frontend (`apps/admin-web/.env.local`):

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_TENANT_ID=<tenant_uuid>
NEXT_PUBLIC_CLIENT_ID=<client_uuid>
```

### Twilio phone webhook configuration

In Twilio Console for your purchased phone number:

1. **A call comes in** → webhook URL:
   `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/calls/webhooks/twilio/inbound`
2. Method: `HTTP POST`.
3. Optionally set status callback URL to:
   `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/calls/webhooks/twilio/status`

### Local run steps

1. Start database/redis stack (existing docker compose setup).
2. Initialize tables:

```bash
cd apps/api
python -m app.db.init_db
```

3. Run backend:

```bash
cd apps/api
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. Run frontend:

```bash
cd apps/admin-web
npm install
npm run dev
```

5. Start tunnel:

```bash
ngrok http 8000
```

### First successful call test

1. Create tenant + client (if not already created) via API or UI bootstrap.
2. In Admin UI, create an **inbound** agent and set:
   - Twilio phone number (E.164)
   - Base prompt
   - Talk tracks
   - CTA instructions
   - Status = **Published**
3. Save agent and verify it appears in Agents list.
4. Call your Twilio number from a real phone.
5. Confirm:
   - call is answered with TwiML voice prompts,
   - conversation loop runs via speech gather,
   - call/transcript records appear in Calls page,
   - call detail page shows transcript entries and status.
