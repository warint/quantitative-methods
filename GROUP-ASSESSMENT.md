# Group assessment

**Ten groups of three. How the course checks that all three did the work.**

---

## The problem, stated plainly

Group work is the right vehicle for this course — the research mandates need three people, and
arguing about a specification is how you learn to choose one. But a group mark rewards the group,
and a group of three can carry a passenger for a whole semester without anyone outside noticing.

No single mechanism solves this. Peer ratings inflate. Commit counts are gameable. Vivas are
expensive. What works is **several cheap signals that are hard to game simultaneously**, with
consequences that only trigger when independent signals agree.

That is what this course does. Four mechanisms, three of which cost the instructor nothing during
the term.

---

## The four mechanisms

| # | Mechanism | When | Student cost | Instructor cost |
|---|---|---|---|---|
| 1 | **Random presenter draw** | Every practice session | Must be ready | 30 seconds |
| 2 | **Git contribution report** | Automatic | Commit under your own name | One command |
| 3 | **Everyone pushes** | Every practice session | Nothing — it is in the history | One glance |
| 4 | **Confidential peer ratings** | Once, at term end | Five minutes | ~20 minutes |

Mechanisms 1–3 are **deterrents**. They mostly work by existing. Mechanism 4 is the only one that
moves a mark, and it can only do so with mechanism 2's agreement.

---

### 1. The random presenter draw

The two-minute report at the end of every practice session is delivered by **a member drawn at random when the
group is called**.

```bash
python scripts/assess.py draw --session 5
```

Draw it live, on the screen, in front of the room. That is the entire point: not the randomness,
but the *visible* randomness. If any of the three can be called, all three must understand the
analysis, the number, and what would undermine it.

**The draw is balanced, not naive.** Whoever in the group has presented least is drawn first, and
nobody presents twice in a row. Over eleven sessions each member presents three or four times.
Every draw is logged to `assessment/presenter_log.csv`.

> This is the cheapest and most effective mechanism in the whole scheme. It costs thirty seconds a
> week and it changes how groups prepare, because the cost of a passenger becomes immediate and
> public rather than deferred and private.

**In Session 12**, questions during the defence are directed at a **named** member, not at the
group. Same principle.

---

### 2. The git contribution report

Every student commits under their own git identity, configured in Session 1's setup. The history
is then a continuous, passive record.

```bash
python scripts/assess.py contributions
```

Produces, per group: commits, share of group commits, lines added and removed, and — the most
informative column — **distinct weeks active**. Flags any student with no commits, under 10% of
their group's commits, or fewer than half their group's median active weeks.

**Read the caveats, because they matter.**

- Commit counts are noisy. A student who thinks hard and commits once may have contributed more
  than one who commits forty times.
- Pair programming legitimately concentrates commits in one identity. The `Co-authored-by:` trailer
  is supported and counted — teach students to use it:
  ```
  git commit -m "Add stability bootstrap

  Co-authored-by: Name <email@hec.ca>"
  ```
- The report is **evidence for a conversation, not a verdict**. A flag on its own changes nothing.

Its real value is at the extremes. A student with zero commits across eleven weeks is not a
measurement artefact.

---

### 3. Everyone pushes, every practice session

There are **no assigned roles**. All three members work on the practice together, and all three are
expected to **commit and push from their own machine** before they leave the room.

That is not self-reported. It is in the history:

```bash
python scripts/assess.py contributions
```

Alongside the commit table, this prints a per-member × per-week grid:

```
  G07  (angle C)
      student                     commits   share    +lines   -lines  weeks
      A. Dubois                        24    41%      1840      310      9
      B. Vogt                          21    36%      1502      260      9
      C. Mensah                        13    23%       690      120      5

      student                     36  37  38  39  40  41  42  43  44   pushed
      A. Dubois                    x   x   x   x   x   x   x   x   x   9/9
      B. Vogt                      x   x   x   x   x   x   x   x   x   9/9
      C. Mensah                    x   x   .   .   x   x   .   .   x   5/9
      note: C. Mensah pushed nothing in 4 active week(s)
```

> **Why the grid rather than the total.** A total can look acceptable while hiding that someone
> stopped contributing in week three. A row of gaps in the weeks when the group was demonstrably
> working is a specific, dated, checkable observation — and it is the one worth raising in week
> four rather than week eleven.

Groups of three left to themselves do tend to produce one person who types, one who talks and one
who watches. The requirement that **everyone pushes** is what makes that pattern visible, without
anyone having to fill in a form.

---

### 4. Confidential peer ratings

Once, at the end of the semester. Each student rates their **two teammates** — never themselves —
on four dimensions, 1–5:

**Preparation · Contribution to the analysis · Reliability · Understanding**

The form is [`assessment/peer-ratings/FORM.md`](assessment/peer-ratings/FORM.md). It takes five
minutes and includes one required free-text field: *one thing this person did that made the work
better*. That field is not decoration — it forces a specific memory instead of a general
impression, which measurably reduces both halo effects and retaliation.

```bash
python scripts/assess.py multipliers
```

---

## How a multiplier is computed

For each student: mean of the eight ratings received (two raters × four dimensions), divided by
their **group's** mean. Call it the relative score $\rho$.

| Relative score $\rho$ | Multiplier |
|---|---|
| $\rho \ge 0.90$ | **1.00 — no change** |
| $0.75 \le \rho < 0.90$ | 0.90 |
| $0.60 \le \rho < 0.75$ | 0.80 |
| $\rho < 0.60$ | 0.70 (floor) |
| Rating $\ge 4.5/5$ while a teammate falls below 1.00 | 1.05 |

### The gate — this is the important part

> **A multiplier below 1.00 is applied only if the git contribution report independently flags the
> same student.**

If peer ratings say one thing and the commit history says another, **no automatic change is made**.
The case is printed as `REVIEW` and lands on the instructor's desk with both records attached.

This single rule does most of the work of making the scheme fair and defensible:

- It defeats **collusion**. A group that agrees to rate each other 5/5 protects a passenger from
  the ratings, but not from the commit history.
- It defeats **retaliation**. A student who marks down a teammate they disliked cannot move that
  teammate's mark unless the git record agrees.
- It defeats **inflation** as a failure mode. Because the default is 1.00, universal 5s produce
  exactly the outcome that universal accuracy would for a well-functioning group: nobody moves.
- It keeps the burden of proof where it belongs. Reducing someone's mark requires two independent
  records to point the same way.

Because $\rho$ is computed **relative to the group's own mean**, a group that rates generously and
a group that rates strictly are treated identically. Only within-group differences matter.

### What it applies to

**The multiplier scales the team work only — the 20% of the course grade covering the
governance file, the analysis, the revised memo and the defence.**

It does **not** touch:

- the **midterm exam (30%)**, which is written alone under exam conditions;
- the **final exam (40%)**, which is individual in both components — the
  [paper is written alone](assessments/final-paper/README.md) and the oral examines each student
  directly, so there is no shared work to attribute;
- **participation**, which is already individual.

Nobody loses more than 30% of the group component. The 1.05 exists so that carrying a group is
recognised rather than merely endured.

### Appeals

Any student whose multiplier is not 1.00 is told the basis and may request review within seven
days. The review considers all three records together — ratings, git history, the per-week push grid — plus
anything the student brings. The point is to get it right, not to defend the arithmetic.

---

## The participation grade

Separate from the group mark, and worth **10%**. At HEC Montréal attendance is assumed, so
participation cannot mean turning up. It means contributing to the room.

### The mechanism

After each practice session — sixty seconds — the instructor records the students who made a **real
contribution**: a question that changed how another group thought about their result, a connection
between two angles, a challenge that landed, a correction. Not their own two-minute report; that is
already logged.

```bash
python scripts/assess.py participation --session 5
```

Prints a numbered class list grouped by group. Type the numbers. Done.

```bash
python scripts/assess.py participation --report
```

Produces the distribution, the quartiles, a bar-calibration table, and a verdict per student:
`pass`, `REVIEW` or `fail`. Those map to the 10% as full marks, an instructor decision, and a
partial mark respectively — the script reports the evidence, it does not compute the mark.

### The bar, and why it is absolute rather than relative

The obvious design is to rank students by tick count and fail the bottom quantile. It is worth
saying plainly why this course does not do that.

- **A rank is not a standard.** "Pass" implies a bar was met. Under ranking, the same student with
  the same behaviour passes in one cohort and fails in another. The word stops meaning anything.
- **It is weak on appeal.** *"You failed because eleven classmates were ticked more often"* is
  much harder to defend than *"you have no recorded contribution in ten sessions; the published bar
  is one."*
- **It is zero-sum, and this course is not.** The second half of every session is ten projects
  illuminating one theme, cross-group questions, peer review, disagreement treated as contribution.
  Rank-based participation gives a student a reason not to make another group look good. That cuts
  directly against the architecture.

**So: the quartiles calibrate the bar; they never assign the outcome.** You look at the
distribution, choose where the bar sits, publish it, and apply it to everyone. Students can read
the requirement in the syllabus and know what is asked of them without knowing anything about their
classmates.

The report prints a calibration table for exactly this:

```
  Candidate bars, and how many students fall below each
    bar 1    6 below ( 20%)  ▏▏▏▏▏▏
    bar 2   14 below ( 47%)  ▏▏▏▏▏▏▏▏▏▏▏▏▏▏
    bar 3   23 below ( 77%)  ▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏▏
```

### The arithmetic constraint — read this before setting the bar

This is the part that surprises people, and it is not a matter of judgement.

If you tick $t$ students per session over $S$ sessions in a class of $N$, the **average** student
can receive at most $tS/N$ ticks. Tick "a couple" — say 2 — across 10 sessions for 30 students, and
the average student receives **0.67 ticks**. Most receive zero. There is then no bar that
distinguishes the disengaged from the merely unnoticed, because the measurement is mostly noise:
whether a student was ticked depends on which side of the room you were looking at.

| Ticked per session | Average ticks per student over 10 sessions | Usable bar |
|---|---|---|
| 2 (7% of class) | 0.7 | none — too sparse to decide anything |
| 4 (13%) | 1.3 | 1, barely |
| **6 (20%)** | **2.0** | **1, comfortably** |
| 9 (30%) | 3.0 | 2 |

**Tick about a fifth of the class each session.** The script warns you if you drift below that.
A tick is a record that someone contributed, not a prize — being generous with it is what makes the
grade mean something at the end.

### The safety net

Your attention is the measuring instrument, and it is imperfect. Thirty students, ninety minutes,
ten reports — you will not notice everyone who deserved noticing.

So a student is **never automatically failed** if they delivered the two-minute report every time
they were drawn and were active in at least half the session weeks. They are marked `REVIEW`, with
the note: *did you simply not notice them?*

The distinction the tool draws is sharp and it is the right one:

```
  Farid Haddad     0 ticks   delivered 3/3   active  0/10 weeks   FAIL
  Klara Horvat     0 ticks   delivered 4/4   active 10/10 weeks   REVIEW
```

Same tick count. Completely different students. The verdict column knows the difference, and the
`REVIEW` cases are the only ones that need your judgement.

### What students are told

> Participation is worth 10% and it is not attendance. It is **active engagement**, and three
> routes count: contributing in the room — a question that changed how another group saw their
> result, a connection between angles, a challenge that landed — working the ninety minutes of the
> practice with your group, and completing an optional QMIB Lab App knowledge check at home.
> What is marked is sustained engagement across the term, judged on its own terms and never as a
> ranking against each other.
>
> If you are drawn to present, deliver. Failing to deliver when drawn is the clearest participation
> failure there is.
>
> If you contribute mainly in writing or within your group, tell the instructor. Being quiet is not
> the same as being absent, and the record should reflect what you actually did.

That last paragraph matters. Publish it.

---

## The instructor's routine

**Once, before the term**

```bash
cp assessment/roster.template.csv assessment/roster.csv
# fill in: group, student_id, name, email, git_name, git_email, angle
```

The `git_name` and `git_email` columns must match what students set in Session 1
(`git config user.name` / `user.email`). The report tells you about any unmatched identity, so
mistakes surface in week 2 rather than week 12.

**Every practice session — 90 seconds**

```bash
python scripts/assess.py draw --session 5           # before the reports: project it, call the groups
python scripts/assess.py participation --session 5  # after: tick who contributed. Aim for ~6 of 30.
```

If someone drawn could not deliver, put `y` in their `no_show` column in
`assessment/presenter_log.csv`.

**Twice a term — 5 minutes (week 6 and week 11)**

```bash
python scripts/assess.py status               # contributions + draws + participation
```

Week 6 is the one that matters. A passenger identified in week 6 can still be turned around; one
identified in week 12 can only be marked down, which helps nobody and least of all them.

**Once, at term end — 25 minutes**

```bash
python scripts/assess.py participation --report      # look at the calibration table, choose the bar
python scripts/assess.py participation --report --bar 1
python scripts/assess.py multipliers                 # writes assessment/multipliers.csv
```

Read the `REVIEW` lines. Everything else is a pass at ×1.00 and needs no attention.

---

## What students are told, and when

All of it, in Session 1. Every mechanism here works better when it is known about:

- The draw only changes preparation if students know it is coming.
- The commit history only encourages individual commits if students know it is read.
- The push requirement only prevents the type-talk-watch pattern if students know why it exists.
- The peer ratings only avoid inflation if students understand that the default is no change and
  that rating everyone 5 is a choice to let a free-rider take their mark.

Nothing here is a trap. It is published, and it is on the syllabus.

---

## What this system does not do

Stated honestly, because the limits matter:

- **It does not measure contribution.** It measures three proxies for it. A quiet student who does
  the hardest thinking and commits rarely can be under-detected, which is exactly why the gate
  requires two agreeing signals before anything happens.
- **It does not fix a group that has broken down.** That needs a conversation, in week 6, with you.
  These tools tell you which groups to have it with.
- **It does not remove your judgement.** It removes the routine work so that your judgement is spent
  on the three or four cases a year that need it.

---

## File map

```
GROUP-ASSESSMENT.md            this document
scripts/assess.py              draw · participation · contributions · multipliers · status
assessment/
├── roster.template.csv        copy to roster.csv and fill in
├── roster.csv                 (git-ignored — student data)
├── presenter_log.csv          written by `draw`; add 'y' to no_show if someone can't deliver
├── participation_log.csv      written by `participation --session N`
├── participation.csv          written by `participation --report` (git-ignored)
├── multipliers.csv            written by `multipliers` (git-ignored)
└── peer-ratings/
    ├── FORM.md                the student-facing form
    ├── ratings.template.csv   the entry format
    └── ratings.csv            (git-ignored — confidential)
```

Settings you may want to change live at the top of `scripts/assess.py`:
`PARTICIPATION_BAR`, `TICK_TARGET_PCT`, `MAX_MISSED_DRAWS`, `BANDS`.

Student-identifying files are git-ignored. The templates and this policy are committed.

---

*Related: [course overview](README.md) · [research
mandates](RESEARCH-MANDATES.md) · [Session 12](12-group-presentations/README.md)*
