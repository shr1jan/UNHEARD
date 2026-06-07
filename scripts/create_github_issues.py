#!/usr/bin/env python3
"""
Create / sync GitHub Issues for Unheard from the backlog/ markdown files.

The backlog (backlog/E*.md) is the single source of truth. This script:
  1. Creates/updates labels (type + criticality + per-epic).
  2. Creates phase Milestones (Phase 0 .. Phase 5).
  3. Creates one Issue per backlog item, with the full body, labels, and milestone.
  4. Second pass: rewrites in-body dependency references (E#-#) into clickable
     issue links (#N) once every issue number is known.

Idempotent: existing issues are matched by title and skipped (their deps are
still re-linked). Re-running after editing the backlog adds only what's new.

Usage:
  python3 scripts/create_github_issues.py            # create / sync
  python3 scripts/create_github_issues.py --dry-run  # preview, write nothing
  python3 scripts/create_github_issues.py --repo owner/name

Requires: gh CLI authenticated with `repo` scope.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "backlog"

# ---------------------------------------------------------------------------
# Label catalogue: name -> (color hex, description)
# ---------------------------------------------------------------------------
TYPE_LABELS = {
    "privacy-critical": ("5319E7", "Defect can de-anonymize a user. Elevated review + CI gates."),
    "safety-critical":  ("B60205", "Defect can harm someone in crisis. Clinical-advisor review."),
    "core":             ("0E8A16", "On the critical path for the MVP."),
    "ml":               ("6F42C1", "Masking / STT / moderation model work."),
    "infra":            ("BFD4F2", "Platform, CI, storage, queues."),
    "client":           ("0052CC", "Mobile / web app."),
    "backend":          ("1D76DB", "API gateway / services."),
    "legal":            ("D4C5F9", "Gated on or producing legal/clinical sign-off."),
    "risk":             ("FBCA04", "High-uncertainty; benchmark/spike before committing."),
}

# Phase number -> milestone (title, description)
MILESTONES = {
    0: ("Phase 0 — Foundations & Safety Design",
        "Make the dangerous parts safe before building the easy parts. Gates Phase 3."),
    1: ("Phase 1 — Core Social MVP",
        "Record -> server mask -> preview -> post; feed; topics; reactions; my-posts; hard delete."),
    2: ("Phase 2 — Interaction & Moderation",
        "Comments + poster controls; pain/harm/crisis moderation; abuse controls; crisis detection + interim bridge."),
    3: ("Phase 3 — Human Crisis Hotline",
        "Three channels; real-time DSP masking; 24/7 no-dead-ends; user-only break glass. Blocked by legal sign-off."),
    4: ("Phase 4 — Sustainability & Trust",
        "Contextual non-tracking ads; separate hotline funding; money transparency; nonprofit structure."),
    5: ("Phase 5 — Deepen Support & Quality",
        "Own peer + clinical responder tiers; stronger real-time neural masking; ongoing tuning."),
}

ISSUE_RE = re.compile(r"^### \[[ x]\] (E\d+-\d+) — (.+)$")
DEP_TOKEN_RE = re.compile(r"\bE\d+-\d+\b")
BACKTICK_RE = re.compile(r"`([^`]+)`")
PHASE_RE = re.compile(r"\*\*Phase:\*\*\s*(\d+)")
EPIC_HEADER_RE = re.compile(r"^# Epic (E\d+) — (.+?)\s*$")


def run(args, dry=False, capture=True):
    """Run a gh/subprocess command. Returns stdout (str) or '' in dry-run."""
    printable = " ".join(a if " " not in a else f'"{a}"' for a in args)
    if dry:
        print(f"  [dry-run] {printable}")
        return ""
    res = subprocess.run(args, capture_output=capture, text=True)
    if res.returncode != 0:
        sys.stderr.write(f"! command failed: {printable}\n{res.stderr}\n")
        raise SystemExit(1)
    return res.stdout.strip()


def detect_repo() -> str:
    out = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
    return out


def parse_backlog():
    """Return (issues, epic_labels).

    issues: list of dicts {id, title, epic_code, epic_name, phase, labels, body}
    epic_labels: dict label_name -> (color, description)
    """
    issues = []
    epic_labels = {}
    for path in sorted(BACKLOG.glob("E*.md")):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        epic_code, epic_name = "", ""
        m = EPIC_HEADER_RE.match(lines[0]) if lines else None
        if m:
            epic_code, epic_name = m.group(1), m.group(2)
        phase_m = PHASE_RE.search(text)
        phase = int(phase_m.group(1)) if phase_m else 1

        epic_label = f"epic:{epic_code}"
        epic_labels[epic_label] = ("EDEDED", f"{epic_code} — {epic_name}")

        # Split file into issue blocks
        idx = 0
        n = len(lines)
        while idx < n:
            im = ISSUE_RE.match(lines[idx])
            if not im:
                idx += 1
                continue
            issue_id = im.group(1)
            heading_rest = im.group(2)
            # title = heading minus backtick label tokens and trailing emoji/space
            title_clean = BACKTICK_RE.sub("", heading_rest)
            title_clean = re.sub(r"[🔒🛡️]", "", title_clean).strip(" ·-—\t")
            labels = [t.strip() for t in BACKTICK_RE.findall(heading_rest)]
            labels = [l for l in labels if l in TYPE_LABELS]

            # gather body until next issue heading or EOF
            body_lines = []
            j = idx + 1
            while j < n and not ISSUE_RE.match(lines[j]):
                body_lines.append(lines[j])
                j += 1
            body = "\n".join(body_lines).strip()

            issues.append({
                "id": issue_id,
                "title": f"{issue_id} — {title_clean}",
                "epic_code": epic_code,
                "epic_name": epic_name,
                "epic_label": epic_label,
                "phase": phase,
                "labels": labels + [epic_label],
                "body": body,
                "src": path.name,
            })
            idx = j
    return issues, epic_labels


def build_body(issue, id_to_num, link_deps: bool) -> str:
    body = issue["body"]
    if link_deps:
        # turn every E#-# reference into a clickable issue link (keep the id for humans)
        def repl(m):
            ref = m.group(0)
            num = id_to_num.get(ref)
            return f"{ref} (#{num})" if num else ref
        body = DEP_TOKEN_RE.sub(repl, body)
    header = (f"**Epic:** {issue['epic_code']} — {issue['epic_name']}  ·  "
              f"**Phase:** {issue['phase']}  ·  **ID:** `{issue['id']}`\n\n")
    footer = (f"\n\n---\n_Generated from "
              f"[`backlog/{issue['src']}`](../blob/main/backlog/{issue['src']}) — "
              f"the backlog is the source of truth; edit there and re-run "
              f"`scripts/create_github_issues.py`._")
    return header + body + footer


def ensure_labels(all_labels, dry):
    print("== Labels ==")
    for name, (color, desc) in all_labels.items():
        run(["gh", "label", "create", name, "--color", color,
             "--description", desc, "--force"], dry=dry)
        print(f"  ✓ {name}")


def ensure_milestones(repo, phases_used, dry):
    print("== Milestones ==")
    existing = {}
    if not dry:
        raw = run(["gh", "api", f"repos/{repo}/milestones?state=all&per_page=100"])
        for m in json.loads(raw or "[]"):
            existing[m["title"]] = m["number"]
    for phase in sorted(phases_used):
        title, desc = MILESTONES[phase]
        if title in existing:
            print(f"  • exists: {title}")
            continue
        run(["gh", "api", f"repos/{repo}/milestones", "-f", f"title={title}",
             "-f", f"description={desc}", "-f", "state=open"], dry=dry)
        print(f"  ✓ {title}")


def existing_issue_map(repo, dry):
    if dry:
        return {}
    raw = run(["gh", "issue", "list", "--repo", repo, "--state", "all",
               "--limit", "500", "--json", "number,title"])
    out = {}
    for it in json.loads(raw or "[]"):
        out[it["title"]] = it["number"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="owner/name (default: from git remote)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    repo = args.repo or detect_repo()
    print(f"Repo: {repo}{'  (DRY RUN)' if args.dry_run else ''}\n")

    issues, epic_labels = parse_backlog()
    print(f"Parsed {len(issues)} issues across {len({i['epic_code'] for i in issues})} epics.\n")

    all_labels = {**TYPE_LABELS, **epic_labels}
    ensure_labels(all_labels, args.dry_run)

    phases_used = {i["phase"] for i in issues}
    ensure_milestones(repo, phases_used, args.dry_run)

    existing = existing_issue_map(repo, args.dry_run)
    id_to_num = {}
    # title -> id, to backfill numbers for already-existing issues
    title_to_id = {i["title"]: i["id"] for i in issues}
    for title, num in existing.items():
        if title in title_to_id:
            id_to_num[title_to_id[title]] = num

    # Pass 1: create missing issues (body without dep links yet)
    print("\n== Issues (pass 1: create) ==")
    created = []
    for issue in issues:
        if issue["title"] in existing:
            print(f"  • exists: {issue['title']}")
            continue
        milestone_title = MILESTONES[issue["phase"]][0]
        body = build_body(issue, id_to_num, link_deps=False)
        cmd = ["gh", "issue", "create", "--repo", repo,
               "--title", issue["title"], "--body", body,
               "--milestone", milestone_title]
        for lbl in issue["labels"]:
            cmd += ["--label", lbl]
        url = run(cmd, dry=args.dry_run)
        if not args.dry_run and url:
            num = int(url.rstrip("/").split("/")[-1])
            id_to_num[issue["id"]] = num
            print(f"  ✓ #{num}  {issue['title']}")
        else:
            print(f"  ✓ {issue['title']}")
        created.append(issue["id"])

    # Pass 2: re-link dependencies now that all numbers are known
    print("\n== Issues (pass 2: link dependencies) ==")
    for issue in issues:
        num = id_to_num.get(issue["id"])
        if not num:
            continue
        if not DEP_TOKEN_RE.search(issue["body"]):
            continue  # no cross-references to link
        body = build_body(issue, id_to_num, link_deps=True)
        run(["gh", "issue", "edit", str(num), "--repo", repo, "--body", body],
            dry=args.dry_run)
        print(f"  ↻ #{num}  {issue['id']} dependencies linked")

    print(f"\nDone. Created {len(created)} new issue(s); "
          f"{len(issues) - len(created)} already existed.")


if __name__ == "__main__":
    main()
