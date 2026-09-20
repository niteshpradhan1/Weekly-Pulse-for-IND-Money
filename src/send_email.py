#!/usr/bin/env python3
"""
Draft email sender — sends the weekly note to yourself/alias.
Uses local SMTP or Gmail App Password, or just opens default mail client via eml.

Usage:
  python src/send_email.py --to you@example.com
  python src/send_email.py --to you@example.com --smtp

Env for SMTP (optional):
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
  Defaults to Gmail: smtp.gmail.com:587

If no SMTP env, it will just show instructions and open the .eml file.
"""
import argparse, subprocess, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--to", required=True, help="Your email alias")
    p.add_argument("--smtp", action="store_true", help="Try SMTP send if env set")
    p.add_argument("--file", default=str(ROOT / "output" / "email_draft_latest.txt"))
    args = p.parse_args()
    fp = Path(args.file)
    if not fp.exists():
        # try eml
        fp = sorted((ROOT/"output").glob("email_draft_*.txt"))[-1] if list((ROOT/"output").glob("email_draft_*.txt")) else None
        if not fp or not fp.exists():
            print("No email draft found. Run python src/pulse.py first")
            sys.exit(1)
    content = fp.read_text()
    # Parse subject
    subject = [l for l in content.splitlines() if l.startswith("Subject:")]
    subj = subject[0] if subject else "Weekly Pulse"
    print(f"Draft loaded: {fp}")
    print(f"{subj}")
    print(f"To: {args.to}")
    print("\n--- Preview (first 800 chars) ---\n")
    print(content[:800])

    if args.smtp:
        host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        port = int(os.getenv("SMTP_PORT", "587"))
        user = os.getenv("SMTP_USER")
        pw = os.getenv("SMTP_PASS") or os.getenv("GMAIL_APP_PASSWORD")
        if not user or not pw:
            print("\n[Error] Set SMTP_USER and SMTP_PASS (Gmail App Password) env vars")
            print("  export SMTP_USER=you@gmail.com SMTP_PASS=xxxx")
            sys.exit(1)
        import smtplib, ssl
        from email.message import EmailMessage
        msg = EmailMessage()
        msg["To"] = args.to
        msg["From"] = user
        # extract subject line
        subj_line = subj.replace("Subject:","").strip() if subj else "Weekly Pulse"
        msg["Subject"] = subj_line
        # body is everything after first blank line
        body = content.split("\n\n",1)[1] if "\n\n" in content else content
        msg.set_content(body)
        try:
            with smtplib.SMTP(host, port) as s:
                s.ehlo()
                s.starttls(context=ssl.create_default_context())
                s.login(user, pw)
                s.send_message(msg)
            print(f"\n[Sent] Email sent to {args.to} via {host}:{port}")
        except Exception as e:
            print(f"[Failed] SMTP error: {e}")
            sys.exit(1)
    else:
        eml = ROOT / "output" / "email_draft_latest.eml"
        # Try to find latest eml
        emls = sorted((ROOT/"output").glob("*.eml"))
        if emls:
            eml = emls[-1]
        if eml.exists():
            print(f"\n[Info] Dry-run: Draft ready at {eml}")
            print(f"  - Double-click to open in Mail.app / Outlook")
            print(f"  - Or run with --smtp to actually send")
            # Try open on macOS
            try:
                subprocess.run(["open", str(eml)], check=False)
                print(f"[Opened] {eml} in default mail client")
            except:
                pass
        else:
            print(f"\n[Info] Draft at {fp} — copy/paste into your email client to send to {args.to}")

if __name__ == "__main__":
    main()
