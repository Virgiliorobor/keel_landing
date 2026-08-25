"""Trade Focus contact receiver — standalone, stdlib-only.

Receives the marketing site's contact form (POST /contact as JSON) and
forwards it by SMTP. Runs as its own container next to the static site;
nginx proxies /api/contact to it, so the browser sees same-origin and no
CORS is needed (CORS headers are still emitted when ALLOWED_ORIGINS is set,
for setups that serve it on a separate host).

Abuse controls: honeypot field (_honey -> fake success, nothing sent),
hard field caps, 16 KB body cap, and a per-IP fixed-window rate limit
(in-memory; this is a single-process service).

Configuration (environment):
  CONTACT_EMAIL   destination inbox; unset -> 503 (visible misconfiguration)
  SMTP_HOST       default localhost
  SMTP_PORT       default 1025
  SMTP_USERNAME   empty -> unauthenticated
  SMTP_PASSWORD
  SMTP_STARTTLS   "1"/"true" for authenticated relays on 587
  SMTP_FROM       default "Trade Focus <no-reply@trade-focus.com>"
  ALLOWED_ORIGINS comma-separated origins for CORS (optional)
  RATE_LIMIT      default 5 submissions
  RATE_WINDOW     default 3600 seconds
  PORT            default 8080
"""
from __future__ import annotations

import json
import os
import re
import smtplib
import threading
import time
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MAX_BODY = 16 * 1024
CAPS = {"name": 200, "email": 320, "company": 200, "message": 4000,
        "_subject": 200, "_slot": 200, "lang": 8}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "5"))
RATE_WINDOW = int(os.environ.get("RATE_WINDOW", "3600"))
_rate_lock = threading.Lock()
_rate: dict[str, tuple[float, int]] = {}


def _allow(ip: str) -> bool:
    now = time.monotonic()
    with _rate_lock:
        start, count = _rate.get(ip, (now, 0))
        if now - start >= RATE_WINDOW:
            start, count = now, 0
        count += 1
        _rate[ip] = (start, count)
        if len(_rate) > 10000:  # prune abandoned windows
            for k in [k for k, (s, _) in _rate.items() if now - s >= RATE_WINDOW]:
                del _rate[k]
        return count <= RATE_LIMIT


def _send(to_addr: str, subject: str, body: str, reply_to: str = "") -> None:
    msg = EmailMessage()
    msg["From"] = os.environ.get("SMTP_FROM", "Trade Focus <no-reply@trade-focus.com>")
    msg["To"] = to_addr
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(body)
    host = os.environ.get("SMTP_HOST", "localhost")
    port = int(os.environ.get("SMTP_PORT", "1025"))
    user = os.environ.get("SMTP_USERNAME", "")
    with smtplib.SMTP(host, port, timeout=20) as s:
        if os.environ.get("SMTP_STARTTLS", "").lower() in ("1", "true", "yes"):
            s.starttls()
        if user:
            s.login(user, os.environ.get("SMTP_PASSWORD", ""))
        s.send_message(msg)


def _line(value: str, cap: int) -> str:
    """Collapse to one line and cap length — visitor text never shapes the mail."""
    return " ".join(str(value).split())[:cap]


ACK = {
    "en": {
        "subject_slot": "KEEL walkthrough — request received",
        "subject": "Trade Focus — we received your message",
        "body_slot": ("Hello {name},\n\n"
                      "We received your walkthrough request for:\n\n"
                      "    {slot}\n\n"
                      "You'll receive the calendar invite once we confirm, "
                      "usually within one business day.\n\n"
                      "Trade Focus — tools for customs specialists\n"
                      "https://trade-focus.com\n"),
        "body": ("Hello {name},\n\n"
                 "We received your message and will get back to you soon.\n\n"
                 "Trade Focus — tools for customs specialists\n"
                 "https://trade-focus.com\n"),
    },
    "es": {
        "subject_slot": "Demostración KEEL — solicitud recibida",
        "subject": "Trade Focus — recibimos tu mensaje",
        "body_slot": ("Hola {name},\n\n"
                      "Recibimos tu solicitud de demostración para:\n\n"
                      "    {slot}\n\n"
                      "Recibirás la invitación de calendario en cuanto confirmemos, "
                      "normalmente dentro de un día hábil.\n\n"
                      "Trade Focus — herramientas para especialistas de aduanas\n"
                      "https://trade-focus.com\n"),
        "body": ("Hola {name},\n\n"
                 "Recibimos tu mensaje y te contactamos pronto.\n\n"
                 "Trade Focus — herramientas para especialistas de aduanas\n"
                 "https://trade-focus.com\n"),
    },
}


def _send_ack(fields: dict, contact_addr: str) -> None:
    """Acknowledgment to the visitor. Fixed template; echoes only the
    sanitized name and slot. The confirmed .ics invite is sent personally
    by the operator — this mail only sets that expectation."""
    lang = "es" if fields.get("lang", "").lower().startswith("es") else "en"
    t = ACK[lang]
    name = _line(fields["name"], 80) or ("Hola" if lang == "es" else "Hello")
    slot = _line(fields.get("_slot", ""), 120)
    if slot:
        subject, body = t["subject_slot"], t["body_slot"].format(name=name, slot=slot)
    else:
        subject, body = t["subject"], t["body"].format(name=name)
    _send(fields["email"], subject, body, reply_to=contact_addr)


class Handler(BaseHTTPRequestHandler):
    server_version = "tfcontact/1.0"

    def _origin_headers(self) -> list[tuple[str, str]]:
        allowed = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o.strip()]
        origin = self.headers.get("Origin", "")
        if allowed and origin in allowed:
            return [("Access-Control-Allow-Origin", origin),
                    ("Access-Control-Allow-Methods", "POST, OPTIONS"),
                    ("Access-Control-Allow-Headers", "Content-Type"),
                    ("Vary", "Origin")]
        return []

    def _reply(self, code: int, payload: dict) -> None:
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in self._origin_headers():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _client_ip(self) -> str:
        fwd = self.headers.get("X-Forwarded-For", "")
        if fwd:
            return fwd.split(",")[0].strip()
        return self.client_address[0]

    def do_GET(self):
        if self.path == "/health":
            self._reply(200, {"status": "ok"})
        else:
            self._reply(404, {"error": "not_found"})

    def do_OPTIONS(self):
        self.send_response(204)
        for k, v in self._origin_headers():
            self.send_header(k, v)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        if self.path.rstrip("/") not in ("/contact", "/api/contact"):
            self._reply(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                self._reply(413, {"error": "body_too_large"})
                return
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError
        except Exception:
            self._reply(400, {"error": "bad_json"})
            return

        # honeypot: pretend success, send nothing
        if str(data.get("_honey", "")).strip():
            self._reply(200, {"ok": True})
            return

        fields = {k: str(data.get(k, "")).strip() for k in CAPS}
        if not fields["name"] or not EMAIL_RE.match(fields["email"]):
            self._reply(422, {"error": "invalid_fields"})
            return
        for k, cap in CAPS.items():
            if len(fields[k]) > cap:
                self._reply(422, {"error": "field_too_long", "field": k})
                return

        to_addr = os.environ.get("CONTACT_EMAIL", "")
        if not to_addr:
            self._reply(503, {"error": "contact_not_configured"})
            return
        if not _allow(self._client_ip()):
            self._reply(429, {"error": "rate_limited"})
            return

        slot = _line(fields.get("_slot", ""), 120)
        body = ((f"Slot:    {slot}\n" if slot else "")
                + f"Name:    {fields['name']}\n"
                f"Email:   {fields['email']}\n"
                f"Company: {fields['company'] or '-'}\n\n"
                f"{fields['message'] or '(no message)'}\n")
        try:
            _send(to_addr, fields["_subject"] or "Contact", body)
        except Exception as exc:  # noqa: BLE001 — surface as 502, log the class only
            print(f"send failed: {type(exc).__name__}", flush=True)
            self._reply(502, {"error": "send_failed"})
            return
        # acknowledgment to the visitor — best-effort, never blocks the lead
        if os.environ.get("ACK_ENABLED", "1").lower() not in ("0", "false", "no"):
            try:
                _send_ack(fields, to_addr)
            except Exception as exc:  # noqa: BLE001
                print(f"ack failed: {type(exc).__name__}", flush=True)
        self._reply(200, {"ok": True})

    def log_message(self, fmt, *args):  # quieter default log, no query PII
        print(f"{self._client_ip()} {self.command} {self.path} -> done", flush=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print(f"tfcontact listening on :{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
