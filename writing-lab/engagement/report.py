#!/usr/bin/env python3
"""Build a Chinese, image-first daily report for the engagement data.

Usage:
  .venv/bin/python report.py                # today
  .venv/bin/python report.py --date 2026-11-07

Outputs:
  reports/<date>.html        email-ready HTML, images referenced by absolute URL
  reports/<date>.md          plain-text fallback
  <site>/static/images/engagement/<date>/*.png

Images are hosted on xiongpin.dev so mail clients can load them; push the site
repo before sending the mail.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent
SITE = ROOT.parents[1]  # pinxiong.github.io
plt.rcParams["font.sans-serif"] = ["PingFang SC", "Hiragino Sans GB", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False
BLUE, TEAL, ORANGE, GREY = "#2f6f9f", "#3aa39a", "#d97b29", "#8a939b"

SHORT = [
    ("how-the-strands-agent-loop", "UC01 Agent 循环"),
    ("the-tools-that-got-replaced", "UC02 工具被取代"),
    ("the-limits-that-dont-limit", "UC03 限额"),
    ("it-remembers-across-restarts", "UC04 会话与记忆"),
    ("i-red-teamed-my-own-support-bot", "红队测试"),
    ("two-specialists-one-orchestrator", "双专家编排"),
    ("finding-what-broke", "可观测性"),
    ("a-research-agent-that-searches", "研究代理"),
    ("stopping-an-agent-from-overreaching", "策略强制"),
    ("reaching-real-systems-without-holding", "网关与身份"),
    ("an-agent-that-remembers", "AgentCore 记忆篇"),
    ("your-first-agent-as-a-service", "首个代理服务"),
    ("how-aws-bedrock-agentcore-actually-works", "AgentCore 原理"),
    ("how-engineers-should-learn", "AI 时代学习"),
    ("ai-coding-in-practice", "AI Coding 实践"),
    ("easy-to-use-ecs", "ECS（2022）"),
    ("how-to-build-eks-with-terraform", "EKS（2022）"),
    ("how-to-build-vpc-with-terraform", "VPC（2022）"),
]


def label(slug: str, title: str) -> str:
    for prefix, name in SHORT:
        if slug.startswith(prefix):
            return name
    return title[:22]


def barh(items, title, fname, color=BLUE, xlabel="", out=None):
    """items: list of (label, value) already sorted ascending for display."""
    labels = [i[0] for i in items]
    values = [i[1] for i in items]
    h = max(2.2, 0.42 * len(items) + 1.0)
    fig, ax = plt.subplots(figsize=(9.2, h), dpi=150)
    bars = ax.barh(labels, values, color=color, height=0.62)
    for b, v in zip(bars, values):
        ax.text(b.get_width() + max(values) * 0.012, b.get_y() + b.get_height() / 2,
                f"{v}", va="center", fontsize=9, color="#333")
    ax.set_title(title, fontsize=13, pad=12, color="#1f2a33")
    ax.set_xlabel(xlabel, fontsize=9, color=GREY)
    ax.set_xlim(0, max(values) * 1.14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#d5dade")
    ax.tick_params(axis="y", labelsize=10, length=0)
    ax.tick_params(axis="x", labelsize=9, colors=GREY)
    ax.grid(axis="x", color="#eceff1", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(out / fname, facecolor="white")
    plt.close(fig)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args()
    date = args.date

    snap = json.loads((ROOT / "data" / "latest.json").read_text())
    arts = snap["articles"]
    out = SITE / "static" / "images" / "engagement" / date
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    for slug, a in arts.items():
        d = a["devto"]
        b = a.get("bc") or {}
        rows.append({
            "slug": slug, "name": label(slug, a["title"]),
            "published": (a.get("published_at") or "")[:10],
            "views": d.get("views") or 0, "reactions": d.get("reactions") or 0,
            "comments": d.get("comments") or 0,
            "bc_likes": b.get("likes"), "bc_comments": b.get("comments"),
        })

    images = []
    top = sorted(rows, key=lambda r: r["views"], reverse=True)[:12]
    barh([(r["name"], r["views"]) for r in reversed(top)],
         f"Dev.to 阅读量（{date} 累计）", "devto-views.png", BLUE, "次", out)
    images.append(("devto-views.png", "Dev.to 阅读量"))

    bc = [r for r in rows if r["bc_likes"] is not None]
    if bc:
        bc = sorted(bc, key=lambda r: r["bc_likes"], reverse=True)
        barh([(r["name"], r["bc_likes"]) for r in reversed(bc)],
             "Builder Center 点赞数（累计）", "bc-likes.png", TEAL, "赞", out)
        images.append(("bc-likes.png", "Builder Center 点赞"))

    eng = [r for r in rows if r["views"] >= 15 and r["published"] <= (dt.date.today() - dt.timedelta(days=2)).isoformat()]
    if eng:
        eng = sorted(eng, key=lambda r: r["comments"] / r["views"] * 100, reverse=True)[:10]
        barh([(r["name"], round(r["comments"] / r["views"] * 100, 1)) for r in reversed(eng)],
             "每百次阅读带来的评论数（发布满 48 小时的文章）", "comment-rate.png",
             ORANGE, "条 / 百次阅读", out)
        images.append(("comment-rate.png", "评论率"))

    # Trend chart only once more than one day of history exists.
    hist = ROOT / "data" / "history.jsonl"
    days = set()
    if hist.exists():
        for line in hist.read_text().splitlines():
            if line.strip():
                days.add(json.loads(line)["ts"][:10])
    if len(days) >= 2:
        per_day: dict[str, dict[str, int]] = {}
        for line in hist.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            day = r["ts"][:10]
            # take the last snapshot of each day per article
            key = (day, r["channel"], r["slug"])
            per_day.setdefault(day, {})
            per_day[day][f"{r['channel']}:{r['slug']}"] = r["views"] if r["channel"] == "devto" else (r["reactions"] or 0)
        ordered = sorted(days)
        devto_tot = [sum(v for k, v in per_day[d].items() if k.startswith("devto:")) for d in ordered]
        bc_tot = [sum(v for k, v in per_day[d].items() if k.startswith("bc:")) for d in ordered]
        fig, ax = plt.subplots(figsize=(9.2, 3.6), dpi=150)
        ax.plot(ordered, devto_tot, marker="o", color=BLUE, label="Dev.to 阅读")
        ax.plot(ordered, bc_tot, marker="o", color=TEAL, label="BC 点赞")
        ax.set_title("总量趋势", fontsize=13, color="#1f2a33")
        ax.legend(frameon=False, fontsize=10)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#eceff1")
        ax.set_axisbelow(True)
        fig.tight_layout()
        fig.savefig(out / "trend.png", facecolor="white")
        plt.close(fig)
        images.append(("trend.png", "总量趋势"))

    tot_v = sum(r["views"] for r in rows)
    tot_r = sum(r["reactions"] for r in rows)
    tot_c = sum(r["comments"] for r in rows)
    tot_bl = sum(r["bc_likes"] or 0 for r in rows)
    tot_bc = sum(r["bc_comments"] or 0 for r in rows)
    top_bc = max(rows, key=lambda r: r["bc_likes"] or 0)

    base = f"https://xiongpin.dev/images/engagement/{date}/"
    img_html = "\n".join(
        f'<h3 style="margin:26px 0 8px;font-size:16px;color:#1f2a33">{t}</h3>'
        f'<img src="{base}{n}" alt="{t}" style="width:100%;max-width:760px;border:1px solid #e6eaed;border-radius:6px">'
        for n, t in images)
    html = f"""<div style="font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;color:#1f2a33;max-width:800px">
<h2 style="margin:0 0 4px">文章反馈日报 · {date}</h2>
<p style="color:#8a939b;font-size:13px;margin:0 0 18px">数据截止 {snap['ts']} ｜ Dev.to 与 Builder Center 分渠道统计，不相加</p>
<table style="border-collapse:collapse;font-size:14px;margin-bottom:8px">
<tr style="background:#f2f6f9">
<th style="padding:8px 14px;border:1px solid #e6eaed">Dev.to 阅读</th>
<th style="padding:8px 14px;border:1px solid #e6eaed">reactions</th>
<th style="padding:8px 14px;border:1px solid #e6eaed">Dev.to 评论</th>
<th style="padding:8px 14px;border:1px solid #e6eaed">BC 点赞</th>
<th style="padding:8px 14px;border:1px solid #e6eaed">BC 评论</th></tr>
<tr style="text-align:center;font-size:17px;font-weight:600">
<td style="padding:10px;border:1px solid #e6eaed">{tot_v}</td>
<td style="padding:10px;border:1px solid #e6eaed">{tot_r}</td>
<td style="padding:10px;border:1px solid #e6eaed">{tot_c}</td>
<td style="padding:10px;border:1px solid #e6eaed">{tot_bl}</td>
<td style="padding:10px;border:1px solid #e6eaed">{tot_bc}</td></tr></table>
<p style="font-size:13px;color:#5a6672">共 {len(rows)} 篇文章。Medium 未采集（本机网络不可达），主站为静态站无互动指标。</p>
{img_html}
<h3 style="margin:26px 0 8px;font-size:16px">读数结论</h3>
<ul style="font-size:14px;line-height:1.9;padding-left:20px">
<li>BC 推荐位是最大杠杆：{top_bc['name']} 一篇 {top_bc['bc_likes']} 赞，其余各篇多为个位数到二十。</li>
<li>Dev.to 上评论集中在「边界 + 实测失败」类文章；流程介绍类只有阅读没有对话。</li>
<li>下一篇优先写「manifest 注入的 token 与 TTFT 成本实测」，补齐 UC04 公开承认的缺口。</li>
</ul>
<p style="font-size:12px;color:#8a939b;margin-top:24px">由每日 21:30 自动任务生成；原始数据与选题库见 writing-lab/engagement/。</p>
</div>"""
    reports_dir = ROOT / "reports"
    if not reports_dir.exists():
        reports_dir.mkdir(parents=True)
    (ROOT / "reports" / f"{date}.html").write_text(html)

    md = [f"# 文章反馈日报 · {date}", "",
          f"Dev.to：{len(rows)} 篇 / {tot_v} 阅读 / {tot_r} reactions / {tot_c} 评论",
          f"BC：{tot_bl} 赞 / {tot_bc} 评论（口径不同，不相加）", ""]
    md += [f"- {t}：{base}{n}" for n, t in images]
    (ROOT / "reports" / f"{date}.md").write_text("\n".join(md) + "\n")

    print(f"report: {ROOT / 'reports' / (date + '.html')}")
    print(f"images: {out}")
    for n, _ in images:
        print("  ", base + n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
