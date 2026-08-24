# Deploying trade-focus.com

Production site = two static pages, no build step:

| URL | File |
|---|---|
| `trade-focus.com/` | `index.html` (Trade Focus manifesto) |
| `trade-focus.com/keel/` | `keel/index.html` (KEEL landing) |

The concept archives (`/concepts`, `/v1`, `/v2`) are intentionally **not** deployed — they exist only in the repo and on the GitHub Pages staging URL.

## Before going live — 2 config values

Both pages have a config block at the top of their `<script>` tag:

1. `FORM_ENDPOINT` (both pages) — where the contact form POSTs.
   Zero-backend option: `https://formsubmit.co/<your-inbox>` — no account needed; the first submission emails that inbox a one-time activation link. A honeypot field is already in the form.
2. `BOOKING_URL` (`keel/index.html` only) — a Calendly or Cal.com event link. When set, the CTA opens it in a new tab; when empty, the CTA scrolls to the form.

## Option A — Coolify (recommended, same box as the KEEL portal)

1. Coolify → **+ New → Application → Public/Private repository**, pick this repo and branch.
2. Build pack: **Dockerfile** (it's at the repo root; copies only the two production pages into nginx:alpine, port 80).
3. Domain: `https://trade-focus.com` (add `https://www.trade-focus.com` too if you want the `www`).
4. DNS: `A` record for `trade-focus.com` (and `www`) → the server's IP. `keel.` and `s3.` records are untouched.
5. Deploy. Coolify's proxy handles TLS certificates automatically, exactly like it does for `keel.trade-focus.com`.

Every future `git push` to the configured branch can auto-deploy if you enable the webhook in Coolify.

## Option B — plain Caddy static

Copy the two pages to the server and add a site block:

```bash
rsync -av index.html keel user@server:/srv/trade-focus/
```

```caddy
trade-focus.com {
    root * /srv/trade-focus
    file_server
    encode gzip
}
```

Same DNS record as above; Caddy issues the certificate on first request.

## Smoke test after deploy

- `https://trade-focus.com/` loads the manifesto; EN/ES toggle persists across pages.
- `https://trade-focus.com/keel/` loads KEEL; the header wordmark links back to `/`.
- Submit the contact form once to trigger the FormSubmit activation email (if using FormSubmit), then click the activation link in the inbox.
- The KEEL CTA opens the booking link in a new tab (if configured).
