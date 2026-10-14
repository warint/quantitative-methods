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

Each paper is a script in [`starter/`](starter/), which you download into a folder of your own
(Part 0), and a step-by-step guide in [`replications/`](replications/). The guide tells you, for every step, what to run, why, and the
numbers **you should see**. You are **not** following the papers: each step is a code cell you
already know, run on new data, and the work is to read its output in words, with units.

> This is the best revision you can do for the midterm on **28 October**: every idea from
> sessions 2 to 6 comes back once, on real data, in the order it was taught.

---

## The three hours

| When | What | |
|---|---|---|
| **0:00 – 0:15** | **Part 0 · Set up** — a folder of your own, four packages, the scripts, the check | below |
| **0:15 – 0:55** | **Paper 1** · Session 02 data · news sentiment and stock returns — OLS, the three logits | [guide](replications/R1-fraiberger-2021.md) · [script](starter/r1_fraiberger_2021.py) |
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

Today you work **in a folder of your own, not in the course repository**, with plain Python and four
packages installed by name. No `requirements.txt`, no `qmib`: each script reads its paper's data from
the course site, over the internet.

### Step 0.1 · A new folder, opened in VS Codium

Make an empty folder **outside** `quantitative-methods` — `Desktop/session-07`, say. In VS Codium:
**File → Open Folder…** and choose it. Everything below happens inside it.

### Step 0.2 · A Python environment for this folder

Open the terminal (**Terminal → New Terminal**). Create the environment, then activate it:

- **macOS:** `python3 -m venv .venv` then `source .venv/bin/activate`
- **Linux:** `python3 -m venv .venv` then `source .venv/bin/activate`
- **Windows (PowerShell):** `py -m venv .venv` then `.venv\Scripts\Activate.ps1`

On **macOS**, if your Python came from python.org, run its certificate installer once first, or
the scripts cannot read the course site (`CERTIFICATE_VERIFY_FAILED`):
`open /Applications/Python\ 3*/Install\ Certificates.command`. Python from Homebrew, Linux and
Windows need nothing.

The prompt now starts with `(.venv)`. Then tell VS Codium to use it: `Ctrl`/`Cmd` + `Shift` + `P`,
**Python: Select Interpreter**, and choose the one inside this folder's `.venv`.

### Step 0.3 · Install the four packages

With `(.venv)` showing, the same line on all three platforms:

- **macOS:** `pip install pandas statsmodels scikit-learn matplotlib`
- **Linux:** `pip install pandas statsmodels scikit-learn matplotlib`
- **Windows (PowerShell):** `pip install pandas statsmodels scikit-learn matplotlib`

NumPy and SciPy come with them. That is the whole toolkit for today.

### Step 0.4 · Download the five scripts

All five in one zip — [`session-07-scripts.zip`](https://warint.github.io/quantitative-methods/session-07-scripts.zip) —
unzipped into your folder. Or from the terminal:

- **macOS:** `curl -LO https://warint.github.io/quantitative-methods/session-07-scripts.zip && unzip session-07-scripts.zip`
- **Linux:** `curl -LO https://warint.github.io/quantitative-methods/session-07-scripts.zip && unzip session-07-scripts.zip`
- **Windows (PowerShell):** `Invoke-WebRequest https://warint.github.io/quantitative-methods/session-07-scripts.zip -OutFile session-07-scripts.zip; Expand-Archive session-07-scripts.zip -DestinationPath .`

You now have `check_setup.py` and `r1_…py` to `r4_…py` side by side in the folder. (One at a time:
[check_setup.py](https://warint.github.io/quantitative-methods/session-07/check_setup.py) ·
[r1](https://warint.github.io/quantitative-methods/session-07/r1_fraiberger_2021.py) ·
[r2](https://warint.github.io/quantitative-methods/session-07/r2_saganowski_2019.py) ·
[r3](https://warint.github.io/quantitative-methods/session-07/r3_blonigen_piger_2014.py) ·
[r4](https://warint.github.io/quantitative-methods/session-07/r4_topalova_khandelwal_2011.py) —
open, then **Save As…** into the folder.)

### Step 0.5 · Run the check

Open `check_setup.py` and press the **Run** triangle (top right). Or, in the terminal:

- **macOS:** `python check_setup.py`
- **Linux:** `python check_setup.py`
- **Windows (PowerShell):** `python check_setup.py`

**You should see** your Python version, then every line `OK`: four packages, four data files. A line
that says `MISSING`:

- a **package** — the line prints the `pip install` to type, in the activated environment;
- a **data file** — no internet connection to the course site. Check the wifi and run it again.

### Step 0.6 · How to run a script one step at a time

Every script is cut into blocks that start `# Step 1 · …`, `# Step 2 · …`. The guide has the same
steps in the same order.

- **Run one step:** select its lines and press **Shift+Enter**. VS Codium sends them to a Python
  terminal and prints the result. Variables stay in memory, so the next step can use them.
- **Run the whole script:** the **Run** triangle. Each script reads its data from the site, then
  takes a few seconds.
- **Figures** open in a window; paper 4 also saves `p4_resid_vs_fitted.png` in your folder.

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
| **1** | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* | today's return on yesterday's news sentiment (OLS); an up day (binary logit); the day in thirds, down < flat < up (ordinal); the same three days unordered (multinomial) | sessions 03–04 |
| **2** | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* | does a group dissolve (binary logit); shrink, continue or grow (ordinal logit); which event (multinomial logit) | session 04 |
| **3** | Blonigen & Piger (2014), *Determinants of foreign direct investment* | log FDI on a few gravity variables (OLS), then 56 candidates in ridge, the lasso and the elastic net, scored on held-out pairs | sessions 03 and 05 |
| **4** | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* | productivity on output and input tariffs (OLS); above the median (binary), in thirds (ordinal), who owns the firm (multinomial); then all the firm variables in ridge, the lasso and the elastic net | sessions 03, 04 and 05 |

---

## Part 2 · The log — 10 min

The log is the one thing today that goes back into the course repository, because that is where
your group hands work in. Open `quantitative-methods` in a second VS Codium window
(**File → New Window**, then **File → Open Folder…**), copy
[`replication-log.md`](replication-log.md) into your group folder, and fill in one block per paper
you attempted:

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
