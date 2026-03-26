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
