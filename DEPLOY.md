# Deploying trade-focus.com

Self-contained repo, deployed separately from the KEEL portal. Two containers:

| Service | What | Files |
|---|---|---|
| `web` | nginx serving the two pages, proxying `/api/contact` to the receiver | `Dockerfile`, `nginx.conf`, `index.html`, `keel/index.html` |
| `contact` | contact-form receiver → SMTP. Single-file Python, standard library only — no dependencies to patch | `Dockerfile.contact`, `contact/server.py` |

| URL | Serves |
|---|---|
| `trade-focus.com/` | Trade Focus manifesto |
| `trade-focus.com/keel/` | KEEL landing |
| `trade-focus.com/api/contact` | form receiver (same-origin — no CORS involved) |

The concept archives (`/concepts`, `/v1`, `/v2`) are **not** deployed; they exist only in the repo and on the GitHub Pages staging URL.

## Option A — Coolify (recommended)

1. **+ New → Docker Compose**, pick this repo/branch (`docker-compose.yaml` at the root).
2. Attach the domain `https://trade-focus.com` to the **web** service (add `www` if wanted). Coolify's proxy issues TLS automatically.
3. Set the environment for the **contact** service:

   | Var | Value |
   |---|---|
   | `CONTACT_EMAIL` | inbox that receives leads (**required** — unset ⇒ endpoint answers 503) |
   | `SMTP_HOST` / `SMTP_PORT` | your relay (e.g. Brevo, same values the portal uses), default port 587 |
   | `SMTP_USERNAME` / `SMTP_PASSWORD` | relay credentials |
   | `SMTP_STARTTLS` | `1` (default) for authenticated relays on 587 |
   | `SMTP_FROM` | default `Trade Focus <no-reply@trade-focus.com>` |

4. DNS: `A` record for `trade-focus.com` (and `www`) → the server IP. `keel.` and `s3.` are untouched.
5. Deploy. Enable the webhook if you want auto-deploy on push.

## Option B — plain Caddy + docker

Run the two containers with `docker compose up -d` (same env), then:

```caddy
trade-focus.com {
    encode gzip
    handle /api/contact {
        reverse_proxy contact:8080
    }
    handle {
        reverse_proxy web:80
    }
}
```

## The receiver, in brief (`contact/server.py`)

- `POST /contact` (or `/api/contact`) with JSON `{name, email, company?, message?, _subject?, _honey?}`.
- Honeypot `_honey` filled → fake success, nothing sent. Field caps (name/company 200, message 4000), 16 KB body cap, per-IP rate limit (5/hour, in-memory).
- Sends plain text to `CONTACT_EMAIL` via SMTP; `GET /health` for monitoring.
- **Visitor acknowledgment**: after the lead is delivered, the visitor gets a short bilingual confirmation (their form language) with `Reply-To: CONTACT_EMAIL` — for walkthrough requests it echoes the requested slot and says the calendar invite follows once confirmed. Fixed template; only the sanitized name and slot are echoed, never the message. Best-effort (an ack failure never loses the lead). Disable with `ACK_ENABLED=0`. The confirmed `.ics` invite is sent personally (e.g. from Thunderbird: New Event → add the prospect as attendee).
- `ALLOWED_ORIGINS` env exists for running it on a separate host, but the default same-origin proxy setup needs no CORS at all.

## Booking

No third-party scheduler. The KEEL contact card has a local calendar widget (weekdays, 2-day lead, ~6 weeks out, three curated windows per day in Mexico City time with the visitor's local time shown). The chosen slot is a REQUEST — it rides inside the contact message ("Requested walkthrough slot: …") and the real invite goes out manually by email (Thunderbird sends .ics invites natively). Slot hours are the `SLOT_HOURS` array at the top of `keel/index.html`'s script.

## Still pending before go-live

- Founder review: ES manifesto localization; the withdrawal note on the KEEL simulator (rev 7 §4 flag).

## Smoke test

- `/` and `/keel/` load; EN/ES persists across pages; wordmark links back to `/`.
- `curl https://trade-focus.com/api/contact -X POST -H 'Content-Type: application/json' -d '{"name":"Test","email":"you@example.com","message":"smoke"}'` → `{"ok": true}` and the mail lands in `CONTACT_EMAIL`.
- Submit the real form once from the page; button shows Sending… → Sent.
