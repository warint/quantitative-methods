# Session 07 — The workshop (3 hours, in autonomy)

# Four papers, one toolkit

> **[Open the workshop slides](https://warint.github.io/quantitative-methods/session-07-practice.html)** ·
> source: [`MATH60033A-S07-Practice.qmd`](MATH60033A-S07-Practice.qmd)

---

## What this afternoon is

No new method. For three hours you take the data of four papers you read before sessions 2 to 6
and plug it into the course's models, **with exactly the Python you typed in class** — `smf.ols`,
`smf.logit`, `OrderedModel`, `sm.MNLogit`, `RidgeCV`, `LassoCV`, `ElasticNetCV`. Only the variable
names change.

Each paper is a script in [`starter/`](starter/) and a step-by-step guide in
[`replications/`](replications/). The guide tells you, for every step, what to run, why, and the
numbers **you should see**. You are **not** following the papers: each step is a code cell you
already know, run on new data, and the work is to read its output in words, with units.

> This is the best revision you can do for the midterm on **28 October**: every idea from
> sessions 2 to 6 comes back once, on real data, in the order it was taught.

---

## The three hours

| When | What | |
|---|---|---|
| **0:00 – 0:15** | **Part 0 · Set up** — open the repository, run the check script | below |
| **0:15 – 0:55** | **Paper 1** · Session 02 data · news sentiment and stock returns — OLS, binary logit | [guide](replications/R1-fraiberger-2021.md) · [script](starter/r1_fraiberger_2021.py) |
| **0:55 – 1:35** | **Paper 2** · Session 04 data · social groups — binary, ordinal, multinomial logits | [guide](replications/R2-saganowski-2019.md) · [script](starter/r2_saganowski_2019.py) |
| 1:35 – 1:45 | Break | |
| **1:45 – 2:15** | **Paper 3** · Session 05 data · foreign direct investment — OLS, ridge, lasso, elastic net | [guide](replications/R3-blonigen-piger-2014.md) · [script](starter/r3_blonigen_piger_2014.py) |
| **2:15 – 2:50** | **Paper 4** · Session 06 data · tariffs and productivity — OLS, the three logits, ridge, lasso, elastic net | [guide](replications/R4-topalova-khandelwal-2011.md) · [script](starter/r4_topalova_khandelwal_2011.py) |
| **2:50 – 3:00** | **Part 2 · The log** — fill it in, commit, push | [`replication-log.md`](replication-log.md) |

**If you fall behind,** move on at the half-hour mark anyway and come back later: a finished log for
three papers beats a half-finished one for four. **If you finish early,** each guide ends with
*Pitfalls* — try the variation it suggests (another predictor, another penalty, another threshold).

---

## Alone or in a team — both work

**Alone.** Do the papers in order. Keep the guide open on one side of the screen and the
script on the other.

**As a team (2 to 5).** Two ways, pick one at the start:

- **Split and teach.** Each person takes one or two papers. At **2:15**, stop and take five minutes
  each to walk the others through *your* paper: the question, the model, the result in words, and
  how it differs from the paper.
  Everyone's log then covers all four.
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

- **macOS:** `python3 07-replication-workshop/02-practice/starter/check_setup.py`
- **Linux:** `python3 07-replication-workshop/02-practice/starter/check_setup.py`
- **Windows:** `python 07-replication-workshop\02-practice\starter\check_setup.py`

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
- **Figures** are saved in `07-replication-workshop/02-practice/output/`. Open them from the
  Explorer on the left.

Run the steps **in order**: step 5 needs what step 4 made.

---

## Part 1 · The four papers

Each guide has the same shape, so you always know where you are:

1. **The data** — one line on the paper, what one row is, the variables used.
2. **The models, and where the code comes from** — which session's slide each step copies.
3. **Steps** — each with its code and **You should see**.
4. **Interpretation** — each result as a sentence, in units.
5. **What this does not license** — the part the midterm's Part D asks about.
6. **Pitfalls** — what tripped us, so it does not trip you.

| # | Paper | The simple models | With the code of |
|---|---|---|---|
| **1** | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* | today's return on yesterday's news sentiment (OLS); an up day or a down day (binary logit) | sessions 03–04 |
| **2** | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* | does a group dissolve (binary logit); shrink, continue or grow (ordinal logit); which event (multinomial logit) | session 04 |
| **3** | Blonigen & Piger (2014), *Determinants of foreign direct investment* | log FDI on a few gravity variables (OLS), then 56 candidates in ridge, the lasso and the elastic net, scored on held-out pairs | sessions 03 and 05 |
| **4** | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* | productivity on output and input tariffs (OLS); above the median (binary), in thirds (ordinal), who owns the firm (multinomial); then all the firm variables in ridge, the lasso and the elastic net | sessions 03, 04 and 05 |

---

## Part 2 · The log — 10 min

Copy [`replication-log.md`](replication-log.md) into your group folder and fill in one block per
paper you attempted:

```bash
git checkout -b group-XX
mkdir -p groups/A2026/group-XX/session-07
cp 07-replication-workshop/02-practice/replication-log.md groups/A2026/group-XX/session-07/
```

On **Windows (PowerShell)**, the last two lines are:

```powershell
New-Item -ItemType Directory -Force groups\A2026\group-XX\session-07
Copy-Item 07-replication-workshop\02-practice\replication-log.md groups\A2026\group-XX\session-07\
```

Then commit and push, the same on every platform:

```bash
git add groups/A2026/group-XX/session-07
git commit -m "Session 07 log"
git push -u origin group-XX
```

Replace `XX` with your group number — group 07 uses `group-07`.

---

## What loses marks

- A coefficient with no sentence, no units, or no "holding the others fixed"
- An odds ratio read as a probability, or a lasso zero read as "no effect"
- Presenting a number from a simple model as the paper's finding
- Pasting output with no sentence saying what it means

---

[Back to session 07](../README.md) · [Pre-session](../00-pre-session/README.md) ·
[Workshop slides](https://warint.github.io/quantitative-methods/session-07-practice.html)
