
# QuantumGuard Backend (Phase 1)

FastAPI + MongoDB Atlas + real PQC (liboqs). Ready for Render.com deployment.

## Quick Start

1) Create MongoDB Atlas M0, allow 0.0.0.0/0, get connection string.
2) Set env vars on Render Web Service:
   - `MONGO_URI` (include db name, e.g. `/quantumguard`)
   - `DB_NAME=quantumguard`
   - `JWT_SECRET` (random)
   - `APIKEY_KDF_SALT` (random, different)
   - `APP_ENV=production`
   - `CORS_ORIGINS=http://localhost:3000`
   - `RATE_LIMITS_PQC=10/second,2000/day`
3) Deploy Dockerfile at `services/api/Dockerfile`.

## Test

- Sign up:
  ```bash
  curl -X POST -H 'Content-Type: application/json' \
    -d '{"email":"you@example.com","password":"StrongPass!","industry":"ai"}' \    https://<api>/v1/auth/signup
  ```
- Create API key:
  ```bash
  curl -X POST -H 'Authorization: Bearer <JWT>' -H 'Content-Type: application/json' \    -d '{"label":"prod"}' https://<api>/v1/keys
  ```
- Kyber round-trip:
  ```bash
  curl -X POST -H 'X-API-Key: <key>' -H 'Content-Type: application/json' \    -d '{"scheme":"Kyber1024"}' https://<api>/v1/pqc/kem/keypair
  ```

## Notes
- We never store private keys.
- API keys are hashed (HMAC-SHA256 + app salt).
- Rate limits are enforced; tune via env.
