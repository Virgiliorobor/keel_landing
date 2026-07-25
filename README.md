# KEEL — Landing (concept v2: "The Registry")

Single-file landing page concept for KEEL (`index.html`). No build step, no dependencies — open the file in a browser.

## Direction

Index/archive aesthetic inspired by [zchry.org](https://www.zchry.org/) ([Awwwards ref](https://www.awwwards.com/inspiration/portfolio-filtering-portfolio-zachary-hayes)) — not a copy, an adaptation of the idea to the product argument:

**KEEL is a system of record, so the site looks like one.** Hairline rules, numbered sections, mono metadata, a document-style header (DOC / SCOPE / FIELD / STATUS), and — the centerpiece nod to the reference — a **filterable classification registry** (section 04) where records animate in and out by status/jurisdiction, the way the reference site filters its project index. The medium demonstrates the promise: this is what your classifications look like when the record exists.

- Copy: approved EN rev 3 (CARD-2026-003) + ES localization (CARD-2026-006), switchable via the EN/ES toggle in the header (persisted in localStorage).
- Give/hold respected: registry rows are illustrative, outcome-level only; no mechanics shown. Single CTA: Book a walkthrough.
- Type: Inter (display/body) + JetBrains Mono (metadata, labels, codes). Monochrome ink-on-paper.
- Motion: scroll reveals + filter row collapse; respects `prefers-reduced-motion`.

## Previous concept

The sea/keel canvas concept (waterline that calms as you scroll) lives in the project drafts (`keel_site_concept.html`, CARD-2026-008) and is superseded by this direction for now.
