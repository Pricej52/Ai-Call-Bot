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
