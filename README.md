# Trade Focus / KEEL — site

Static site, no build step. Final shape: `trade-focus.com` is the Trade Focus main page, `trade-focus.com/keel/` is the KEEL product landing.

| Path | Page | Status |
|---|---|---|
| `/` | **Trade Focus** main page | Draft — services copy (section 02) and hero are placeholder drafts pending founder review. |
| `/keel/` | **KEEL landing** (canonical) | The standing version (concept B, rev 7 copy, Vooma-style design) plus the booking CTA and contact form. |
| `/concepts/` | Concept archive chooser | Links `/v1/` and `/v2/`. |
| `/v1/`, `/v2/` | Concept archives | A — The Registry; B — The Position (pre-contact-form snapshot). |

## Contact / booking configuration

Both `/index.html` and `/keel/index.html` have a config block at the top of their `<script>`:

- `BOOKING_URL` (keel only) — a Calendly or Cal.com event link; the CTA button opens it in a new tab. Empty → button scrolls to the form.
- `FORM_ENDPOINT` — where the contact form POSTs. Zero-backend option: `https://formsubmit.co/<inbox>` (first submission triggers a one-time activation email to that inbox; the `_honey` honeypot field is already in the form). Formspree also works. Empty → the form shows "not connected yet" instead of sending.

## Deploy

`.github/workflows/pages.yml` deploys the repo root to GitHub Pages on every push to this branch. Live at `https://virgiliorobor.github.io/keel_landing/`.

### Pointing trade-focus.com here

1. DNS: apex `trade-focus.com` → GitHub Pages A records (185.199.108.153 / .109. / .110. / .111.) + `www` CNAME to `virgiliorobor.github.io`. The `keel.` and `s3.` subdomains keep pointing at the app server — unaffected.
2. Repo: add a `CNAME` file at the root containing `trade-focus.com` (or set the custom domain in Settings → Pages, which commits it).
3. Enforce HTTPS in Settings → Pages once the certificate is issued.

## v2 build notes (rev 7 §8 compliance)

- Ghost state: full ledger + line computed from the 100,000/month default on load, warm grey at full weight; typing a real figure turns grey to ink with no layout shift and no re-animation.
- The line draws right to left, completes at ~60% of section scroll, never reverses, never redraws on keystroke (recomputes in place). Mobile and `prefers-reduced-motion` render it complete.
- Codes are 12px mono grey at one fixed size everywhere, including the registry (code is the last, smallest, greyest column).
- Simulator landing splits the total into Supported · Reconstructed. The one-line caption under the split is drafted from §4's own wording (EN/ES) since the brief specified the split but no visible line — flag if it should change.
- The withdrawal note (§4) is in place beside the rate ladder; founder verification pending before publication, per the brief.
