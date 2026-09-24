# Session 07 — The replication workshop (3 hours, in autonomy)

# Five papers, one toolkit

> **[Open the workshop slides](https://warint.github.io/quantitative-methods/session-07-practice.html)** ·
> source: [`MATH60033A-S07-Practice.qmd`](MATH60033A-S07-Practice.qmd)

---

## What this afternoon is

No new method. For three hours you go back to the five papers you read before sessions 2 to 6,
open the authors' own data, and rebuild a published result **with only the Python you typed in
class** — `pandas`, `smf.ols`, `smf.logit`, `sm.MNLogit`, `LassoCV`, `PanelOLS` and friends.

Each replication is a script in [`starter/`](starter/) and a step-by-step guide in
[`replications/`](replications/). The guide tells you, for every step, what to run, why, and the
exact numbers **you should see**. Three of the five land on the published number; one lands on it
partly by luck; one has no published number to land on. Finding out which is which, and why, is
the point.

> This is the best revision you can do for the midterm on **28 October**: every idea from
> sessions 2 to 6 comes back once, on real data, in the order it was taught.

---

## The three hours

| When | What | |
|---|---|---|
| **0:00 – 0:15** | **Part 0 · Set up** — open the repository, run the check script | below |
| **0:15 – 0:45** | **Replication 1** · Session 02 · news sentiment and stock returns | [guide](replications/R1-fraiberger-2021.md) · [script](starter/r1_fraiberger_2021.py) |
| **0:45 – 1:15** | **Replication 2** · Session 03 · a soil regression, diagnosed | [guide](replications/R2-amsili-2024.md) · [script](starter/r2_amsili_2024.py) |
| **1:15 – 1:45** | **Replication 3** · Session 04 · what happens next to a social group | [guide](replications/R3-saganowski-2019.md) · [script](starter/r3_saganowski_2019.py) |
| 1:45 – 1:55 | Break | |
| **1:55 – 2:25** | **Replication 4** · Session 05 · 56 candidate determinants of FDI | [guide](replications/R4-blonigen-piger-2014.md) · [script](starter/r4_blonigen_piger_2014.py) |
| **2:25 – 2:50** | **Replication 5** · Session 06 · India's tariff cuts and firm productivity | [guide](replications/R5-topalova-khandelwal-2011.md) · [script](starter/r5_topalova_khandelwal_2011.py) |
| **2:50 – 3:00** | **Part 2 · The log** — fill it in, commit, push | [`replication-log.md`](replication-log.md) |

**If you fall behind,** move on at the half-hour mark anyway and come back later: a finished log for
three papers beats a half-finished one for five. **If you finish early,** each guide ends with
*Pitfalls* — try the variation it suggests (another cut-off, another cluster, another network).

---

## Alone or in a team — both work

**Alone.** Do the replications in order. Keep the guide open on one side of the screen and the
script on the other.

**As a team (2 to 5).** Two ways, pick one at the start:

- **Split and teach.** Each person takes one or two papers. At **2:25**, stop and take five minutes
  each to walk the others through *your* result: the target, your number, the gap, the catch.
  Everyone's log then covers all five.
- **Pair at one screen.** One types, one reads the guide aloud and checks the numbers; swap at
  every paper.

Either way, **every member runs at least one script on their own machine**, and the log names
who did what.

---

## Part 0 · Set up — 15 min

### Step 0.1 · Open the repository in VS Codium

**File → Open Folder…** and choose `Desktop/quantitative-methods` — the folder that contains
`qmib.py`. Not a subfolder: the scripts expect the whole repository.

### Step 0.2 · Get the latest version

Open the terminal in VS Codium (**Terminal → New Terminal**) and pull:

```bash
git checkout main
git pull
```

The commands are the same on macOS, Linux and Windows.

### Step 0.3 · Use the course's Python

Bottom-right of VS Codium, click the Python version and choose the one in `.venv`. Or activate it in
the terminal:

- **macOS:** `source .venv/bin/activate`
- **Linux:** `source .venv/bin/activate`
- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`

### Step 0.4 · Run the check

Open [`starter/check_setup.py`](starter/check_setup.py) and press the **Run** triangle (top right).
Or, in the terminal:

- **macOS:** `python3 07-pca-and-factor-analysis/02-practice/starter/check_setup.py`
- **Linux:** `python3 07-pca-and-factor-analysis/02-practice/starter/check_setup.py`
- **Windows:** `python 07-pca-and-factor-analysis\02-practice\starter\check_setup.py`

**You should see** a list in which every line says `OK`. A line that says `MISSING`:

- a **package** — run `pip install -r requirements.txt` in the activated environment;
- a **paper's data** — you did not download that package before its session. The
  [pre-session page](../00-pre-session/README.md), section 2, has the one command per platform
  that fetches it. Start with a paper whose data you do have while it downloads.

### Step 0.5 · How to run a script one step at a time

Every script is cut into blocks that start `# Step 1 · …`, `# Step 2 · …`. The guide has the same
steps in the same order.

- **Run one step:** select its lines and press **Shift+Enter**. VS Codium sends them to a Python
  terminal and prints the result. Variables stay in memory, so the next step can use them.
- **Run the whole script:** the **Run** triangle. Every script takes a few seconds.
- **Figures** are saved in `07-pca-and-factor-analysis/02-practice/output/`. Open them from the
  Explorer on the left.

Run the steps **in order**: step 5 needs what step 4 made.

---

## Part 1 · The five replications

Each guide has the same shape, so you always know where you are:

1. **The paper in brief** and **the research question** — read these first, two minutes.
2. **The published target** — the number you are aiming at, and where it is printed.
3. **Data** — the file, what one row is, the variables that matter.
4. **Steps** — seven to ten, each with its code and **You should see**.
5. **Compare with the paper** — how close you came, and why.
6. **What this does not license** — the part the midterm's Part D asks about.
7. **Pitfalls** — what tripped us, so it does not trip you.

| # | Paper | Reuses | The punchline |
|---|---|---|---|
| **1** | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* | Session 02 · centre, spread, shape; the first regression | You land on the published 0.049 — but only after rebuilding a variable the package lacks, and the match is partly luck. |
| **2** | Amsili, van Es & Schindelbeck (2024), *Pedotransfer functions for field capacity, wilting point and available water* | Session 03 · residuals, leverage, Cook's distance, AIC/BIC | The paper's regression reproduces to three decimals — and **one soil sample** out of 7,232 decides whether an interaction is significant. |
| **3** | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* | Session 04 · logit, odds ratios, LR test, multinomial logit | The paper publishes no number for this data, so you replicate its **design**: the logit's coefficients are significant, yet it does not beat the base rate. |
| **4** | Blonigen & Piger (2014), *Determinants of foreign direct investment* | Session 05 · ridge, lasso, cross-validation, stability | The lasso keeps all nine survivors the course names from the paper — and keeps a tax-haven dummy the paper all but discarded. |
| **5** | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* | Session 06 · pooled OLS, clustering, fixed and random effects | Table 5 reproduces to every printed digit; the random-effects estimate shows why the paper reports fixed effects. |

---

## Part 2 · The log — 10 min

Copy [`replication-log.md`](replication-log.md) into your group folder and fill in one block per
paper you attempted:

```bash
git checkout -b group-XX
mkdir -p groups/A2026/group-XX/session-07
cp 07-pca-and-factor-analysis/02-practice/replication-log.md groups/A2026/group-XX/session-07/
```

On **Windows (PowerShell)**, the last two lines are:

```powershell
New-Item -ItemType Directory -Force groups\A2026\group-XX\session-07
Copy-Item 07-pca-and-factor-analysis\02-practice\replication-log.md groups\A2026\group-XX\session-07\
```

Then commit and push, the same on every platform:

```bash
git add groups/A2026/group-XX/session-07
git commit -m "Session 07 replication log"
git push -u origin group-XX
```

Replace `XX` with your group number — group 07 uses `group-07`.

---

## What loses marks

- Reporting a replicated number without the published one beside it
- Calling a replication failed without saying where it breaks
- Reaching for a method the course has not taught to force a match
- Pasting output with no sentence saying what it means

---

[Back to session 07](../README.md) · [Pre-session](../00-pre-session/README.md) ·
[Workshop slides](https://warint.github.io/quantitative-methods/session-07-practice.html)
