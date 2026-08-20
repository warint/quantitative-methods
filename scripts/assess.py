#!/usr/bin/env python3
"""
group assessment toolkit.

One script, five jobs. Run from the repository root.

    python scripts/assess.py draw --session 5
        Draw this week's presenter for each group. Balanced (whoever has
        presented least is drawn first), unpredictable, and logged.

    python scripts/assess.py contributions
        Per-group git contribution table from the commit history.
        Flags students whose activity is far below their group's.

    python scripts/assess.py participation --session 5
        Tick who made a substantive cross-group contribution today.
        Interactive, ~60 seconds. Everything else is derived automatically.

    python scripts/assess.py participation --report
        Pass/fail against the published bar, with the class distribution
        so you can see whether the bar is calibrated.

    python scripts/assess.py multipliers
        Compute end-of-term individual multipliers from peer ratings,
        gated on the git evidence. Only extremes move.

    python scripts/assess.py status
        Everything at once, one screen. Use this in week 6 and week 11.

Files it reads and writes, all under assessment/:
    roster.csv              you fill this in once
    presenter_log.csv       written by `draw`
    participation_log.csv   written by `participation`
    peer-ratings/ratings.csv  collected once at term end
    multipliers.csv         written by `multipliers`
"""

import argparse
import csv
import os
import random
import re
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assessment")
ROSTER = os.path.join(A, "roster.csv")
PRESENTER_LOG = os.path.join(A, "presenter_log.csv")
PARTICIPATION_LOG = os.path.join(A, "participation_log.csv")
RATINGS = os.path.join(A, "peer-ratings", "ratings.csv")
MULTIPLIERS = os.path.join(A, "multipliers.csv")
PARTICIPATION_OUT = os.path.join(A, "participation.csv")

DIMENSIONS = ["preparation", "contribution", "reliability", "understanding"]

# ── Participation ────────────────────────────────────────────────────────────
# After each lab you tick the students who made a real contribution. Those ticks
# are the measurement. The distribution is then used to LOCATE the bar — not to
# rank students against one another. See GROUP-ASSESSMENT.md for why.
LAB_SESSIONS = list(range(2, 12))          # 02..11  -> 10 sessions
TICK_TARGET_PCT = 0.20                     # aim to tick ~a fifth of the class each session
PARTICIPATION_BAR = 2                      # sessions with a recorded contribution, to PASS
BORDERLINE = 1                             # within this many -> manual review, not auto-fail
MAX_MISSED_DRAWS = 1                       # times you may fail to deliver when drawn

# Multiplier bands, applied to the relative peer score rho = mean(student) / mean(group).
# Nobody moves unless BOTH peer ratings and git evidence agree — see gate below.
BANDS = [
    (0.90, 1.00),   # rho >= 0.90  -> no change (the overwhelming majority)
    (0.75, 0.90),
    (0.60, 0.80),
    (0.00, 0.70),   # floor
]
CARRY_BONUS = 1.05      # awarded when someone demonstrably carried the group
CARRY_MIN_RATING = 4.5


# ─────────────────────────────────────────────────────────────── helpers
def die(msg):
    print(f"\n  ERROR: {msg}\n", file=sys.stderr)
    sys.exit(1)


def load_roster():
    if not os.path.exists(ROSTER):
        die(f"no roster at {ROSTER}\n         copy assessment/roster.template.csv and fill it in")
    with open(ROSTER, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("student_id", "").strip()]
    if not rows:
        die("roster.csv has no students in it yet")
    for r in rows:
        for k in list(r):
            r[k] = (r[k] or "").strip()
    return rows


def by_group(roster):
    g = defaultdict(list)
    for r in roster:
        g[r["group"]].append(r)
    return dict(sorted(g.items()))


def rule(char="─", width=78):
    print(char * width)


def head(title):
    print()
    rule("═")
    print(f"  {title}")
    rule("═")


# ─────────────────────────────────────────────────────────────── draw
def read_presenter_log():
    if not os.path.exists(PRESENTER_LOG):
        return []
    with open(PRESENTER_LOG, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def cmd_draw(args):
    roster = load_roster()
    groups = by_group(roster)
    log = read_presenter_log()

    if any(int(r["session"]) == args.session for r in log) and not args.redraw:
        die(f"session {args.session} has already been drawn. "
            f"Use --redraw to overwrite (it will be recorded as a redraw).")

    counts = Counter(r["student_id"] for r in log)
    last_session = {}
    for r in sorted(log, key=lambda x: int(x["session"])):
        last_session[r["group"]] = r["student_id"]

    head(f"SESSION {args.session:02d} — PRESENTER DRAW")
    print("  Balanced: whoever has presented least is drawn first.")
    print("  Draw this live, in front of the room. That is the whole point.")
    print()

    rng = random.SystemRandom()
    drawn, stamp = [], datetime.now().isoformat(timespec="seconds")

    for gid, members in groups.items():
        pool = [m for m in members if m["student_id"] != last_session.get(gid)] or members
        fewest = min(counts[m["student_id"]] for m in pool)
        eligible = [m for m in pool if counts[m["student_id"]] == fewest]
        pick = rng.choice(eligible)
        drawn.append((gid, pick))
        hist = counts[pick["student_id"]]
        print(f"  {gid}   {pick['name']:<28s} (angle {pick['angle']}, "
              f"{hist} previous {'turn' if hist == 1 else 'turns'})")

    if args.dry_run:
        print("\n  --dry-run: nothing written.")
        return

    new = not os.path.exists(PRESENTER_LOG)
    os.makedirs(A, exist_ok=True)
    with open(PRESENTER_LOG, "a", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        if new:
            wr.writerow(["session", "group", "student_id", "name", "drawn_at",
                         "redraw", "no_show"])
        for gid, p in drawn:
            wr.writerow([args.session, gid, p["student_id"], p["name"], stamp,
                         "yes" if args.redraw else "", ""])
    print(f"\n  Logged to {os.path.relpath(PRESENTER_LOG, ROOT)}")
    print("  If someone drawn could not deliver, put 'y' in their no_show column.")


# ─────────────────────────────────────────────────────────────── contributions
def git_log():
    """Return [(email, name, iso_week, added, removed, files)] per commit."""
    fmt = "%x01%H%x02%aE%x02%aN%x02%aI%x02%B%x03"
    try:
        out = subprocess.run(
            ["git", "log", "--numstat", "--no-merges", f"--pretty=format:{fmt}"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        die("could not read git history — is this a git repository?")

    commits = []
    for chunk in out.split("\x01"):
        if not chunk.strip():
            continue
        headpart, _, numstat = chunk.partition("\x03")
        parts = headpart.split("\x02")
        if len(parts) < 5:
            continue
        _, email, name, iso, body = parts[0], parts[1], parts[2], parts[3], parts[4]
        try:
            dt = datetime.fromisoformat(iso)
        except ValueError:
            continue
        week = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
        added = removed = files = 0
        for line in numstat.strip().splitlines():
            m = re.match(r"^(\d+|-)\t(\d+|-)\t(.+)$", line)
            if not m:
                continue
            files += 1
            if m.group(1) != "-":
                added += int(m.group(1))
            if m.group(2) != "-":
                removed += int(m.group(2))
        authors = [(email.lower(), name)]
        for co in re.findall(r"Co-authored-by:\s*(.+?)\s*<(.+?)>", body):
            authors.append((co[1].lower().strip(), co[0].strip()))
        for em, nm in authors:
            commits.append((em, nm, week, added, removed, files))
    return commits


def attribute(roster, commits):
    """Map commits to students by git email, then git name, then roster email/name."""
    by_email, by_name = {}, {}
    for r in roster:
        for key in (r.get("git_email"), r.get("email")):
            if key:
                by_email[key.lower()] = r["student_id"]
        for key in (r.get("git_name"), r.get("name")):
            if key:
                by_name[key.lower()] = r["student_id"]

    stats = defaultdict(lambda: {"commits": 0, "added": 0, "removed": 0,
                                 "files": 0, "weeks": set()})
    unmatched = Counter()
    for email, name, week, added, removed, files in commits:
        sid = by_email.get(email) or by_name.get(name.lower())
        if not sid:
            unmatched[f"{name} <{email}>"] += 1
            continue
        s = stats[sid]
        s["commits"] += 1
        s["added"] += added
        s["removed"] += removed
        s["files"] += files
        s["weeks"].add(week)
    return stats, unmatched


def contribution_flags(roster, stats):
    """Flag students whose activity is far below their group's. Evidence, not verdict."""
    flags = defaultdict(list)
    for members in by_group(roster).values():
        cs = [stats[m["student_id"]]["commits"] for m in members]
        ws = [len(stats[m["student_id"]]["weeks"]) for m in members]
        total = sum(cs) or 1
        med_w = statistics.median(ws) if ws else 0
        for m in members:
            sid = m["student_id"]
            share = stats[sid]["commits"] / total
            weeks = len(stats[sid]["weeks"])
            if stats[sid]["commits"] == 0:
                flags[sid].append("no commits at all")
            else:
                if share < 0.10:
                    flags[sid].append(f"{share:.0%} of group commits")
                if med_w and weeks < 0.5 * med_w:
                    flags[sid].append(f"active {weeks}w vs group median {med_w:.0f}w")
    return flags


def lab_grid(members, stats):
    """Per-member x per-week attendance grid, derived from commits.

    The course asks every member to commit and push in every lab. That is not
    self-reported: it is in the history. This prints one row per member and one
    column per week in which the group did anything at all, so a member who was
    carried shows up as a row of gaps rather than as a total that looks fine.
    """
    weeks = sorted({w for m in members for w in stats[m["student_id"]]["weeks"]})
    if not weeks:
        print("      no commits yet")
        return []
    labels = [w.split("-W")[-1] for w in weeks]
    print(f"      {'student':<26s} " + " ".join(f"{x:>3s}" for x in labels) + "   pushed")
    silent = []
    for m in members:
        active = stats[m["student_id"]]["weeks"]
        cells = " ".join(f"{'  x' if w in active else '  .'}" for w in weeks)
        n = sum(1 for w in weeks if w in active)
        if n < len(weeks):
            silent.append((m, len(weeks) - n))
        print(f"      {m['name'][:26]:<26s} {cells}   {n}/{len(weeks)}")
    return silent

def cmd_contributions(args):
    roster = load_roster()
    stats, unmatched = attribute(roster, git_log())
    flags = contribution_flags(roster, stats)

    head("GIT CONTRIBUTION REPORT")
    print("  Evidence for a conversation, not a verdict. Commit counts are noisy and")
    print("  gameable; pair programming legitimately concentrates them. The per-week")
    print("  grid is the more useful half: the course asks every member to push in")
    print("  every lab, and a row of gaps says more than a low total.")
    print()

    for gid, members in by_group(roster).items():
        total = sum(stats[m["student_id"]]["commits"] for m in members) or 1
        print(f"  {gid}  (angle {members[0]['angle']})")
        print(f"      {'student':<26s} {'commits':>8s} {'share':>7s} {'+lines':>9s} "
              f"{'-lines':>8s} {'weeks':>6s}")
        for m in sorted(members, key=lambda x: -stats[x["student_id"]]["commits"]):
            s = stats[m["student_id"]]
            mark = "  <-- FLAG" if m["student_id"] in flags else ""
            print(f"      {m['name'][:26]:<26s} {s['commits']:>8d} "
                  f"{s['commits']/total:>6.0%} {s['added']:>9d} {s['removed']:>8d} "
                  f"{len(s['weeks']):>6d}{mark}")
        print()
        silent = lab_grid(members, stats)
        for m, missed in silent:
            print(f"      note: {m['name']} pushed nothing in {missed} active week(s)")
        print()

    if flags:
        rule()
        print("  FLAGGED")
        for sid, why in flags.items():
            who = next(r for r in roster if r["student_id"] == sid)
            print(f"    {who['group']}  {who['name']:<26s} {'; '.join(why)}")
        print()
        print("  A flag alone changes nothing. It gates the peer-rating multiplier:")
        print("  a mark is only reduced when the peer ratings AND this report agree.")
    else:
        rule()
        print("  No contribution anomalies detected.")

    if unmatched:
        print()
        rule()
        print("  UNMATCHED GIT IDENTITIES (add these to roster.csv git_email / git_name)")
        for who, n in unmatched.most_common(12):
            print(f"    {n:>4d} commits   {who}")
    return flags


# ─────────────────────────────────────────────────────────────── participation
def session_weeks():
    """Map session number -> ISO week, taken from when that session's draw was made."""
    out = {}
    for r in read_presenter_log():
        try:
            dt = datetime.fromisoformat(r["drawn_at"])
        except (ValueError, KeyError):
            continue
        out[int(r["session"])] = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
    return out


def read_participation_log():
    if not os.path.exists(PARTICIPATION_LOG):
        return []
    with open(PARTICIPATION_LOG, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def credit_matrix(roster):
    """Per student: the ticks they earned, plus the corroborating evidence.

    ticks      sessions in which you recorded a real contribution  <- THE MEASUREMENT
    delivered  sessions they gave the two-minute report when drawn }  corroboration,
    commits    sessions in whose week they committed work          }  used only to
    missed     times drawn but did not deliver                     }  block a false fail
    """
    weeks = session_weeks()
    stats, _ = attribute(roster, git_log())
    labs = set(LAB_SESSIONS)

    drawn, delivered = defaultdict(set), defaultdict(set)
    for r in read_presenter_log():
        s = int(r["session"])
        drawn[r["student_id"]].add(s)
        if str(r.get("no_show", "")).strip().lower() not in ("y", "yes", "1", "true"):
            delivered[r["student_id"]].add(s)

    ticks = defaultdict(set)
    for r in read_participation_log():
        ticks[r["student_id"]].add(int(r["session"]))

    def near(week, active):
        """Session week, or the week either side — students commit after class too."""
        if not week:
            return False
        y, w = int(week[:4]), int(week[-2:])
        return any(f"{y}-W{w + d:02d}" in active for d in (-1, 0, 1))

    out = {}
    for m in roster:
        sid = m["student_id"]
        commits = {s for s in LAB_SESSIONS if near(weeks.get(s), stats[sid]["weeks"])}
        out[sid] = {"ticks": ticks[sid] & labs,
                    "delivered": delivered[sid] & labs,
                    "commits": commits,
                    "drawn": drawn[sid],
                    "missed": drawn[sid] - delivered[sid]}
    return out


def quantiles(values):
    """Q1/Q2/Q3 cut points, and the index of each value's quartile (1 = lowest)."""
    s = sorted(values)
    if not s:
        return (0, 0, 0)
    def q(p):
        k = (len(s) - 1) * p
        lo, hi = int(k), min(int(k) + 1, len(s) - 1)
        return s[lo] + (s[hi] - s[lo]) * (k - lo)
    return (q(0.25), q(0.50), q(0.75))


def cmd_participation(args):
    roster = load_roster()
    if args.report:
        return participation_report(roster, args)
    if args.session is None:
        die("give --session N to record a session, or --report to compute pass/fail")

    groups = by_group(roster)
    existing = {r["student_id"] for r in read_participation_log()
                if int(r["session"]) == args.session}

    head(f"SESSION {args.session:02d} — CROSS-GROUP CONTRIBUTION")
    print("  Who said something substantive about ANOTHER group's work today?")
    print("  Questions, challenges, connections between angles. Not their own report —")
    print("  that is already logged. Be generous: this is the route by which a quiet")
    print("  student who thinks well gets credit.")
    print()

    numbered_list, i = [], 1
    for gid, members in groups.items():
        print(f"  {gid}", end="")
        for m in members:
            mark = "*" if m["student_id"] in existing else " "
            print(f"   {i:2d}{mark} {m['name'][:22]:<22s}", end="")
            numbered_list.append(m)
            i += 1
        print()
    if existing:
        print("\n  (* already recorded for this session)")

    picks = args.spoke
    if picks is None:
        print()
        try:
            raw = input("  Numbers, space-separated (blank = nobody, q = cancel): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  cancelled."); return
        if raw.lower() in ("q", "quit"):
            print("  cancelled."); return
        picks = raw.split()

    chosen = []
    for tok in picks:
        if tok.isdigit() and 1 <= int(tok) <= len(numbered_list):
            chosen.append(numbered_list[int(tok) - 1])
        else:
            hits = [m for m in roster if tok.lower() in m["name"].lower()]
            if len(hits) == 1:
                chosen.append(hits[0])
            elif len(hits) > 1:
                print(f"  '{tok}' is ambiguous: {', '.join(h['name'] for h in hits)} — skipped")
            else:
                print(f"  '{tok}' matched nobody — skipped")

    chosen = [m for m in chosen if m["student_id"] not in existing]
    if not chosen:
        print("\n  Nothing new recorded.")
        return

    new = not os.path.exists(PARTICIPATION_LOG)
    os.makedirs(A, exist_ok=True)
    with open(PARTICIPATION_LOG, "a", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        if new:
            wr.writerow(["session", "group", "student_id", "name", "recorded_at"])
        stamp = datetime.now().isoformat(timespec="seconds")
        for m in chosen:
            wr.writerow([args.session, m["group"], m["student_id"], m["name"], stamp])
    print(f"\n  Recorded {len(chosen)}: " + ", ".join(m["name"] for m in chosen))
    print(f"  -> {os.path.relpath(PARTICIPATION_LOG, ROOT)}")


def participation_report(roster, args):
    cm = credit_matrix(roster)
    n_students, n_sessions = len(roster), len(LAB_SESSIONS)
    counts = {m["student_id"]: len(cm[m["student_id"]]["ticks"]) for m in roster}
    vals = list(counts.values())
    total_ticks = sum(vals)
    sessions_ticked = len({int(r["session"]) for r in read_participation_log()})

    head("PARTICIPATION")
    print(f"  {total_ticks} contribution ticks recorded over {sessions_ticked} session(s)")
    if sessions_ticked:
        per = total_ticks / sessions_ticked
        pct = per / n_students
        print(f"  averaging {per:.1f} per session = {pct:.0%} of the class")
        if pct < TICK_TARGET_PCT * 0.6:
            print()
            print(f"  ⚠  You are ticking about {pct:.0%} of the class each session. Below roughly")
            print(f"     {TICK_TARGET_PCT:.0%} the measurement gets too sparse to support a")
            print("     pass/fail decision: most students sit at zero, the quartiles collapse")
            print("     into ties, and whether a student was ticked starts to depend on which")
            print("     side of the room you were looking at. Be more generous — the tick is")
            print("     a record that someone contributed, not a prize.")

    # ── the distribution, and the quartiles ──────────────────────────────────
    q1, q2, q3 = quantiles(vals)
    dist = Counter(vals)
    hi = max(vals) if vals else 0
    peak = max(dist.values()) if dist else 1
    print()
    print("  Distribution of ticks per student")
    for k in range(hi, -1, -1):
        n = dist.get(k, 0)
        blocks = "█" * max(0, round(26 * n / peak)) if n else ""
        note = ""
        if k == int(q1):
            note = "  Q1"
        if k == int(q2):
            note = (note + " Q2(median)").strip()
        if k == int(q3):
            note = (note + " Q3").strip()
        print(f"    {k:>3d} {blocks:<26s} {n:>2d}   {note}")
    print(f"\n  quartiles: Q1 = {q1:.1f}   median = {q2:.1f}   Q3 = {q3:.1f}")

    bottom = [m for m in roster if counts[m["student_id"]] <= q1]
    zeros = [m for m in roster if counts[m["student_id"]] == 0]
    print(f"  bottom quartile (≤ Q1): {len(bottom)} students · never ticked: {len(zeros)}")

    # ── where could the bar go? ──────────────────────────────────────────────
    print()
    print("  Candidate bars, and how many students fall below each")
    for b in range(1, min(hi, 6) + 1):
        below = sum(1 for v in vals if v < b)
        blocks = "▏" * below
        print(f"    bar {b}   {below:>2d} below ({below / n_students:>4.0%})  {blocks}")
    print()
    print("  Rule of thumb: if a candidate bar puts more than ~15% of the class below")
    print("  it, either the bar is too high or you have not ticked generously enough.")
    print("  The arithmetic is unforgiving — at t ticks per session over "
          f"{n_sessions} sessions the")
    print(f"  average student can only receive {total_ticks / max(n_students,1):.1f} ticks, so a bar "
          "above that fails half the")
    print("  room by construction, however engaged they were.")

    # ── the bar ──────────────────────────────────────────────────────────────
    bar = args.bar if args.bar is not None else PARTICIPATION_BAR
    print()
    rule()
    print(f"  BAR = {bar}: a pass requires a recorded contribution in at least {bar}")
    print(f"  of {n_sessions} lab sessions, with no more than {MAX_MISSED_DRAWS} failure")
    print("  to deliver when drawn.")
    print()
    print("  The quartiles are for CALIBRATING this bar, not for assigning outcomes.")
    print("  Move it with --bar N if the distribution says it sits in the wrong place —")
    print("  then move it once, for everyone, and say so. A student should be able to")
    print("  read the bar in the syllabus and know what is required of them without")
    print("  knowing anything about their classmates.")

    # ── verdicts ─────────────────────────────────────────────────────────────
    rows, npass, nrev, nfail = [], 0, 0, 0
    for members in by_group(roster).values():
        for m in members:
            sid, c = m["student_id"], cm[m["student_id"]]
            n, missed = counts[sid], len(c["missed"])
            # Never auto-fail a student who did everything asked of them and was
            # simply not noticed. Your attention is the measuring instrument, and it
            # is imperfect; that is a limit of the measurement, not a student failing.
            solid = (missed == 0 and len(c["drawn"]) > 0
                     and len(c["commits"]) >= 0.5 * n_sessions)
            if n >= bar and missed <= MAX_MISSED_DRAWS:
                verdict, why = "pass", ""
                npass += 1
            elif missed > MAX_MISSED_DRAWS:
                verdict, why = "REVIEW", f"failed to deliver when drawn {missed}x"
                nrev += 1
            elif n >= max(1, bar - BORDERLINE):
                verdict, why = "REVIEW", f"{n} tick(s), within {BORDERLINE} of the bar"
                nrev += 1
            elif solid:
                verdict = "REVIEW"
                why = (f"only {n} tick(s), but delivered every time drawn "
                       f"({len(c['delivered'])}x) and active in {len(c['commits'])} of "
                       f"{n_sessions} session weeks — did you simply not notice them?")
                nrev += 1
            else:
                verdict = "FAIL"
                why = (f"{n} tick(s); delivered {len(c['delivered'])}/{len(c['drawn'])} when "
                       f"drawn; active {len(c['commits'])}/{n_sessions} weeks")
                nfail += 1
            rows.append((m, c, n, verdict, why))

    shown = rows if args.all else [r for r in rows if r[3] != "pass"]
    if shown:
        print()
        rule()
        print(f"  {'student':<24s} {'grp':>4s} {'ticks':>6s} {'deliv':>6s} {'wks':>4s}   verdict")
        for m, c, n, verdict, why in sorted(shown, key=lambda r: (r[3] != "FAIL", r[2])):
            print(f"  {m['name'][:24]:<24s} {m['group']:>4s} {n:>6d} "
                  f"{len(c['delivered']):>6d} {len(c['commits']):>4d}   {verdict}")
            if why:
                print(f"      {why}")
        print()

    rule()
    print(f"  {npass} pass · {nrev} review · {nfail} fail   (bar = {bar})")
    if nfail + nrev > n_students * 0.25:
        print()
        print("  More than a quarter of the class is below the bar. Either the bar is")
        print("  mis-calibrated, or you have not been ticking generously enough. Check")
        print("  the ticks-per-session figure above before you conclude it is the class.")
    if nrev:
        print()
        print("  REVIEW is not a fail. It means the records disagree, and the disagreement")
        print("  deserves thirty seconds of your judgement rather than an automatic outcome.")

    if not args.dry_run:
        os.makedirs(A, exist_ok=True)
        with open(PARTICIPATION_OUT, "w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["group", "student_id", "name", "ticks", "quartile",
                         "delivered_when_drawn", "active_session_weeks",
                         "missed_draws", "verdict", "note"])
            for m, c, n, verdict, why in rows:
                qt = 1 if n <= q1 else (2 if n <= q2 else (3 if n <= q3 else 4))
                wr.writerow([m["group"], m["student_id"], m["name"], n, qt,
                             len(c["delivered"]), len(c["commits"]),
                             len(c["missed"]), verdict, why])
        print(f"\n  Written to {os.path.relpath(PARTICIPATION_OUT, ROOT)}")


# ─────────────────────────────────────────────────────────────── multipliers
def load_ratings():
    if not os.path.exists(RATINGS):
        die(f"no ratings at {RATINGS}\n         collect them with "
            f"assessment/peer-ratings/FORM.md, then fill ratings.csv")
    with open(RATINGS, encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("ratee_id", "").strip()]
    out = []
    for r in rows:
        try:
            vals = [float(r[d]) for d in DIMENSIONS]
        except (KeyError, ValueError):
            continue
        if any(v < 1 or v > 5 for v in vals):
            continue
        out.append({"rater_id": r["rater_id"].strip(),
                    "ratee_id": r["ratee_id"].strip(),
                    "mean": sum(vals) / len(vals)})
    if not out:
        die("ratings.csv parsed but contained no usable rows (need 1–5 on each dimension)")
    return out


def band(rho):
    for lo, mult in BANDS:
        if rho >= lo:
            return mult
    return BANDS[-1][1]


def cmd_multipliers(args):
    roster = load_roster()
    ratings = load_ratings()
    stats, _ = attribute(roster, git_log())
    flags = contribution_flags(roster, stats)

    means = defaultdict(list)
    raters = defaultdict(set)
    for r in ratings:
        means[r["ratee_id"]].append(r["mean"])
        raters[r["ratee_id"]].add(r["rater_id"])

    head("INDIVIDUAL MULTIPLIERS")
    print("  Default is 1.00. A mark is reduced ONLY when the peer ratings and the")
    print("  git contribution report agree. One signal alone opens a conversation;")
    print("  it does not move a mark.")
    print()

    results = []
    for gid, members in by_group(roster).items():
        gvals = [v for m in members for v in means.get(m["student_id"], [])]
        gmean = statistics.mean(gvals) if gvals else 0
        if not gmean:
            print(f"  {gid}   no ratings received")
            continue
        print(f"  {gid}   group mean rating {gmean:.2f}")
        low_present = False
        rows = []
        for m in members:
            sid = m["student_id"]
            vals = means.get(sid, [])
            if not vals:
                rows.append((m, None, None, 1.00, "no ratings received — review manually"))
                continue
            rbar = statistics.mean(vals)
            rho = rbar / gmean
            raw = band(rho)
            gated, note = 1.00, ""
            if raw < 1.00:
                if sid in flags:
                    gated = raw
                    note = f"peer {rho:.2f} + git flag ({flags[sid][0]})"
                    low_present = True
                else:
                    note = f"peer {rho:.2f} low but git shows normal activity — REVIEW, no auto-change"
            if len(raters[sid]) < 2:
                note = (note + "; " if note else "") + f"only {len(raters[sid])} rater(s)"
            rows.append((m, rbar, rho, gated, note))

        for m, rbar, rho, mult, note in rows:
            if rbar is not None and rbar >= CARRY_MIN_RATING and low_present and mult == 1.00:
                mult, note = CARRY_BONUS, "carried the group"
            rb = f"{rbar:.2f}" if rbar is not None else "  — "
            rh = f"{rho:.2f}" if rho is not None else " — "
            print(f"      {m['name'][:26]:<26s} rating {rb}  rel {rh}  "
                  f"×{mult:.2f}   {note}")
            results.append({"group": m["group"], "student_id": m["student_id"],
                            "name": m["name"], "mean_rating": rb.strip(),
                            "relative": rh.strip(), "multiplier": f"{mult:.2f}",
                            "note": note})
        print()

    changed = [r for r in results if r["multiplier"] != "1.00"]
    rule()
    print(f"  {len(results)} students · {len(changed)} multiplier(s) other than 1.00")
    if changed:
        print("  Every one of these must be reviewed by you before marks are released,")
        print("  and the student must be told the basis and offered the appeal route.")

    if not args.dry_run:
        os.makedirs(A, exist_ok=True)
        with open(MULTIPLIERS, "w", encoding="utf-8", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=["group", "student_id", "name",
                                               "mean_rating", "relative", "multiplier", "note"])
            wr.writeheader()
            wr.writerows(results)
        print(f"\n  Written to {os.path.relpath(MULTIPLIERS, ROOT)}")


# ─────────────────────────────────────────────────────────────── status
def cmd_status(args):
    roster = load_roster()
    groups = by_group(roster)
    log = read_presenter_log()
    head("ASSESSMENT STATUS")
    print(f"  {len(roster)} students in {len(groups)} groups")
    sessions = sorted({int(r['session']) for r in log})
    print(f"  presenter draws recorded: {len(sessions)} "
          f"({'sessions ' + ', '.join(map(str, sessions)) if sessions else 'none yet'})")
    counts = Counter(r["student_id"] for r in log)
    never = [r for r in roster if counts[r["student_id"]] == 0]
    if sessions and never:
        print(f"  students who have never presented: {len(never)}")
        for r in never[:10]:
            print(f"      {r['group']}  {r['name']}")
    plog = read_participation_log()
    psess = sorted({int(r["session"]) for r in plog})
    print(f"  participation ticks recorded: {len(plog)} across "
          f"{len(psess)} session(s){' — none yet' if not psess else ''}")
    if sessions and set(sessions) - set(psess):
        print(f"      sessions drawn but not ticked: "
              f"{', '.join(map(str, sorted(set(sessions) - set(psess))))}")
    print(f"  peer ratings collected: {'yes' if os.path.exists(RATINGS) else 'not yet'}")
    print()
    cmd_contributions(args)
    if plog:
        args.report, args.bar, args.all, args.dry_run = True, None, False, True
        participation_report(roster, args)


# ─────────────────────────────────────────────────────────────── main
def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("draw", help="draw this week's presenter for each group")
    d.add_argument("--session", type=int, required=True)
    d.add_argument("--redraw", action="store_true", help="overwrite an existing draw")
    d.add_argument("--dry-run", action="store_true")
    d.set_defaults(func=cmd_draw)

    c = sub.add_parser("contributions", help="git contribution table with flags")
    c.set_defaults(func=cmd_contributions)


    pa = sub.add_parser("participation", help="record a session, or report pass/fail")
    pa.add_argument("--session", type=int, help="record cross-group contributions for this session")
    pa.add_argument("--spoke", nargs="*", default=None,
                    help="numbers or surnames, to skip the interactive prompt")
    pa.add_argument("--report", action="store_true", help="compute pass/fail with the distribution")
    pa.add_argument("--bar", type=int, help=f"override the bar (default {PARTICIPATION_BAR})")
    pa.add_argument("--all", action="store_true", help="list every student, not only non-passes")
    pa.add_argument("--dry-run", action="store_true")
    pa.set_defaults(func=cmd_participation)

    m = sub.add_parser("multipliers", help="end-of-term multipliers from peer ratings")
    m.add_argument("--dry-run", action="store_true")
    m.set_defaults(func=cmd_multipliers)

    s = sub.add_parser("status", help="everything at once")
    s.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)
    print()


if __name__ == "__main__":
    main()
