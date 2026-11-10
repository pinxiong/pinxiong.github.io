#!/usr/bin/env python3
"""Hourly engagement collector for Pin's published articles.

Channels:
  devto  full stats (views / reactions / comments) + comment text, via Forem API
  bc     likesCount + commentsCount, scraped from the embedded JSON in the
         public Builder Center page; comment TEXT comes from the public
         content-service endpoint /cs/v2/comments/public (no auth needed)
  medium not collected: medium.com is unreachable from this network. Manual.
  site   static Hugo, no engagement metrics.

Writes:
  data/history.jsonl      one row per article per channel per run
  data/latest.json        last snapshot, used for diffing
  data/dashboard.md       human-readable table
  data/comments/<id>.json              all known Dev.to comments per article
  data/comments/bc-<uc>-<id>.json      all BC top-level comments per article
  data/new-comments.md                 comments discovered in THIS run only (empty = none)

No third-party dependencies. Never prints secrets.
"""
from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
REGISTRY = json.loads((ROOT / "registry.json").read_text())["articles"]
DEVTO_KEY_FILE = pathlib.Path.home() / ".workbuddy" / "secrets" / "devto_api_key"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36")
SELF = "pinxiongcn"  # own Dev.to username: my own replies are not new work


def fetch(url: str, api_key: str | None = None, timeout: int = 60,
          extra_headers: dict | None = None) -> str | None:
    headers = {"User-Agent": UA}
    if api_key:
        headers["api-key"] = api_key
    if extra_headers:
        headers.update(extra_headers)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # network is flaky here; retry quietly
            if attempt == 2:
                print(f"  FETCH FAIL {url[:90]} -> {type(e).__name__}: {e}", file=sys.stderr)
                return None
            time.sleep(3)


def flatten_comments(nodes, out, depth=0):
    for n in nodes:
        out.append({
            "id": n.get("id_code"),
            "user": n.get("user", {}).get("username"),
            "name": n.get("user", {}).get("name"),
            "created_at": n.get("created_at"),
            "depth": depth,
            "text": re.sub(r"<[^>]+>", "", n.get("body_html", "")).strip(),
        })
        flatten_comments(n.get("children") or [], out, depth + 1)


BC_COMMENTS_API = "https://api.builder.aws.com/cs/v2/comments/public"


def bc_comments(bc_id: str) -> list[dict] | None:
    """Public Builder Center comment text. No auth; top-level comments only."""
    url = (f"{BC_COMMENTS_API}?contentId=/content/{bc_id}"
           "&contentType=ARTICLE&sortBy=NEWEST&pageSize=100")
    raw = fetch(url, timeout=25, extra_headers={
        "Accept": "application/json", "Origin": "https://builder.aws.com"})
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    out = []
    for c in data.get("comments", []):
        au = c.get("author") or {}
        created = c.get("createdAt")
        when = (dt.datetime.fromtimestamp(created / 1000, dt.timezone.utc)
                .isoformat(timespec="seconds")) if created else ""
        out.append({"id": c.get("commentId"), "user": au.get("alias"),
                    "name": au.get("preferredName"), "created_at": when,
                    "likes": c.get("likesCount"),
                    "text": (c.get("markdownDescription") or "").strip()})
    return out


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc).astimezone()
    ts = now.isoformat(timespec="seconds")
    (DATA / "comments").mkdir(parents=True, exist_ok=True)
    previous = {}
    latest_file = DATA / "latest.json"
    if latest_file.exists():
        previous = json.loads(latest_file.read_text()).get("articles", {})

    key = DEVTO_KEY_FILE.read_text().strip()
    raw = fetch("https://dev.to/api/articles/me/published?per_page=100", api_key=key)
    if raw is None:
        print("Dev.to unreachable; aborting run without touching state")
        return 1
    articles = json.loads(raw)

    snapshot, rows, new_notes = {}, [], []
    for a in articles:
        slug = a["slug"]
        reg = REGISTRY.get(slug, {})
        devto = {
            "id": a["id"],
            "views": a.get("page_views_count"),
            "reactions": a.get("public_reactions_count"),
            "comments": a.get("comments_count"),
            "url": a.get("url"),
        }
        rows.append({"ts": ts, "channel": "devto", "slug": slug,
                     "views": devto["views"], "reactions": devto["reactions"],
                     "comments": devto["comments"]})

        # Comment text is only fetched when the count moved (cheap hourly run).
        old_count = (previous.get(slug, {}).get("devto") or {}).get("comments")
        if devto["comments"] and devto["comments"] != old_count:
            craw = fetch(f"https://dev.to/api/comments?a_id={a['id']}")
            if craw:
                flat: list[dict] = []
                flatten_comments(json.loads(craw), flat)
                cfile = DATA / "comments" / f"{a['id']}.json"
                known = set()
                if cfile.exists():
                    known = {c["id"] for c in json.loads(cfile.read_text())}
                cfile.write_text(json.dumps(flat, ensure_ascii=False, indent=1))
                for c in flat:
                    if c["id"] not in known and c["user"] != SELF:
                        new_notes.append(
                            f"### Dev.to · {a['title']}\n"
                            f"- url: {devto['url']}\n- author: {c['name']} (@{c['user']})\n"
                            f"- at: {c['created_at']}\n- depth: {c['depth']}\n\n{c['text']}\n")

        bc_id = reg.get("bc")
        bc = None
        if bc_id:
            html = fetch(f"https://builder.aws.com/content/{bc_id}")
            if html:
                likes = re.search(r'"likesCount":(\d+)', html)
                comms = re.search(r'"commentsCount":(\d+)', html)
                bc = {"id": bc_id,
                      "likes": int(likes.group(1)) if likes else None,
                      "comments": int(comms.group(1)) if comms else None,
                      "url": f"https://builder.aws.com/content/{bc_id}"}
                rows.append({"ts": ts, "channel": "bc", "slug": slug,
                             "views": None, "reactions": bc["likes"],
                             "comments": bc["comments"]})
                old_bc = (previous.get(slug, {}).get("bc") or {}).get("comments")
                cfile = DATA / "comments" / f"bc-{reg.get('uc') or 'x'}-{bc_id}.json"
                baseline = not cfile.exists()
                known = set()
                if not baseline:
                    try:
                        known = {c["id"] for c in json.loads(cfile.read_text())}
                    except (json.JSONDecodeError, KeyError, TypeError):
                        baseline = True  # tolerate older raw-API-shaped files
                count_moved = (bc["comments"] is not None and old_bc is not None
                               and bc["comments"] != old_bc)
                if baseline or count_moved:
                    comments = bc_comments(bc_id)
                    if comments is not None:
                        cfile.write_text(json.dumps(comments, ensure_ascii=False, indent=1))
                        # First run only builds a baseline; historical comments are not news.
                        if not baseline:
                            fresh = [c for c in comments
                                     if c["id"] not in known and c["user"] != SELF]
                            for c in fresh:
                                new_notes.append(
                                    f"### Builder Center · {a['title']}\n"
                                    f"- url: {bc['url']}\n"
                                    f"- author: {c['name']} (@{c['user']})\n"
                                    f"- at: {c['created_at']}\n\n{c['text']}\n")
                            if not fresh and bc["comments"] and old_bc is not None \
                                    and bc["comments"] > old_bc:
                                new_notes.append(
                                    f"### Builder Center · {a['title']}\n"
                                    f"- url: {bc['url']}\n"
                                    f"- comment count {old_bc} -> {bc['comments']}; "
                                    f"no new top-level comment (likely a reply). "
                                    f"Read /cs/childrenComments before replying.\n")

        snapshot[slug] = {
            "title": a["title"], "published_at": a.get("published_at"),
            "series": reg.get("series", "other"), "uc": reg.get("uc"),
            "devto": devto, "bc": bc,
            "medium": {"url": reg.get("medium"), "status": "manual-not-collected"},
            "site": reg.get("site"),
        }

    with (DATA / "history.jsonl").open("a") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    (DATA / "latest.json").write_text(json.dumps(
        {"ts": ts, "articles": snapshot}, ensure_ascii=False, indent=1))
    (DATA / "new-comments.md").write_text(
        f"# New comments discovered at {ts}\n\n" + ("\n".join(new_notes) if new_notes else "none\n"))

    lines = [f"# Engagement dashboard — {ts}", "",
             "| article | series | published | devto views | devto reactions | devto comments | BC likes | BC comments |",
             "|---|---|---|---|---|---|---|---|"]
    for slug, s in sorted(snapshot.items(),
                          key=lambda kv: kv[1].get("published_at") or "", reverse=True):
        if (s.get("published_at") or "")[:10] < "2026-09-01":
            continue  # Pin, 2026-11-07: only Sep-2026 onward belongs in the report
        d, b = s["devto"], s["bc"] or {}
        title = s["title"][:58].replace("|", "\\|")
        lines.append(f"| [{title}]({d['url']}) | {s['series']} | "
                     f"{(s['published_at'] or '')[:10]} | {d['views']} | {d['reactions']} | "
                     f"{d['comments']} | {b.get('likes', '—')} | {b.get('comments', '—')} |")
    (DATA / "dashboard.md").write_text("\n".join(lines) + "\n")

    print(f"scan complete {ts}: {len(snapshot)} articles, {len(rows)} metric rows")
    print(f"new comment items: {len(new_notes)}")
    for n in new_notes:
        print("  NEW:", n.splitlines()[0])
    print(f"dashboard: {DATA / 'dashboard.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
