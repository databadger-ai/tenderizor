# CanadaBuys Tender Workbench frontend

Transparent, supervised React/Vite MVP for the CanadaBuys AI Tender Assistant.

## Local development

```bash
npm install
VITE_API_URL=http://localhost:8000/api/v1 npm run dev
```

`VITE_API_URL` must point to the API v1 root. The default is same-origin `/api/v1`.

## Verification

```bash
npm run lint
npm run typecheck
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

## Production container

```bash
docker build --build-arg VITE_API_URL=/api/v1 -t canadabuys-frontend .
docker run --rm -p 8080:80 canadabuys-frontend
curl --fail http://localhost:8080/health
```

The production image serves static assets through nginx with SPA fallback and an unauthenticated liveness endpoint at `/health`. Nginx proxies `/api/v1/` to the Compose service `api:8000`.
