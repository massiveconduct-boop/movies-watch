#!/usr/bin/env python3
"""Post the catalog to a Telegram channel, one title per message.

Setup:
  1. Create a bot with @BotFather -> token.
  2. Make the bot an admin of your channel (or use a private chat id).
  3. export TELEGRAM_BOT_TOKEN="123:abc"
     export TELEGRAM_CHAT_ID="@yourchannel"

Usage:
  python3 post.py --dry-run
  python3 post.py --limit 5
  python3 post.py                  # all 60, 4s apart
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

API = "https://api.telegram.org/bot%s/%s"
POSTS = Path(__file__).with_name("posts.json")


def call(token, method, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API % (token, method), data=data)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        try:
            return json.loads(body)
        except Exception:
            return {"ok": False, "description": body or str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--chat", help="override TELEGRAM_CHAT_ID")
    ap.add_argument("--start", type=int, default=1, help="1-based index")
    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    ap.add_argument("--delay", type=float, default=4.0)
    args = ap.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat = args.chat or os.environ.get("TELEGRAM_CHAT_ID", "")
    if not args.dry_run and (not token or not chat):
        sys.exit("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (or use --dry-run).")

    posts = json.loads(POSTS.read_text())
    posts = posts[args.start - 1:]
    if args.limit:
        posts = posts[:args.limit]

    for i, p in enumerate(posts, start=args.start):
        print("[%d/%d] %s" % (i, args.start + len(posts) - 1, p["title"]))
        if args.dry_run:
            print(p["caption"].replace("\n", "\n    "))
            continue
        params = {"chat_id": chat, "photo": p["image"], "caption": p["caption"], "parse_mode": "HTML"}
        res = call(token, "sendPhoto", params)
        if not res.get("ok"):
            print("  ! sendPhoto failed:", res.get("description"))
            res = call(token, "sendMessage", {"chat_id": chat, "text": p["caption"], "parse_mode": "HTML",
                                              "disable_web_page_preview": "false"})
            if not res.get("ok"):
                print("  ! sendMessage failed:", res.get("description"))
        time.sleep(args.delay)


if __name__ == "__main__":
    main()
