# KEEL — Landing concepts

Two parallel landing-page concepts for KEEL, kept side by side for comparison. No build step, no dependencies.

| Path | Concept | Copy | Notes |
|---|---|---|---|
| `/` | Chooser index | — | Minimal door page linking both versions. |
| `/v1/` | **A — The Registry** | EN rev 3 (CARD-2026-003) + ES (CARD-2026-006) | Index/archive aesthetic inspired by [zchry.org](https://www.zchry.org/): grotesque + mono, numbered sections, filterable classification registry, scroll reveals. |
| `/v2/` | **B — The Position** | rev 7 (EN/ES, for build) | Legal-opinion reference world. Governing rule: the code is never the hero (small/mono/grey everywhere). Exposure simulator (ghost state, right-to-left line) as the only interactive object; registry restored static and inverted; four-movement nav; cold→warm tonal cut at the hinge; motion inventory limited to the line and the cut. |

## Deploy

`.github/workflows/pages.yml` deploys the repo root to GitHub Pages on every push to this branch. Live at `https://virgiliorobor.github.io/keel_landing/` once Pages is enabled (Settings → Pages → Source: GitHub Actions).

## v2 build notes (rev 7 §8 compliance)

- Ghost state: full ledger + line computed from the 100,000/month default on load, warm grey at full weight; typing a real figure turns grey to ink with no layout shift and no re-animation.
- The line draws right to left, completes at ~60% of section scroll, never reverses, never redraws on keystroke (recomputes in place). Mobile and `prefers-reduced-motion` render it complete.
- Codes are 12px mono grey at one fixed size everywhere, including the registry (code is the last, smallest, greyest column).
- Simulator landing splits the total into Supported · Reconstructed. The one-line caption under the split is drafted from §4's own wording (EN/ES) since the brief specified the split but no visible line — flag if it should change.
- The withdrawal note (§4) is in place beside the rate ladder; founder verification pending before publication, per the brief.
