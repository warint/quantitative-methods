# Session 07 — Before the workshop

**Wednesday 14 October 2026** · 15:30–18:30 · Décelles — Victoriaville

> The workshop is three hours of work at your own keyboard, in a folder of your own. It goes well
> if that folder is ready when you arrive, and badly if you spend the first hour installing.
> This page is **30 minutes**.

---

## 1. Re-read the four abstracts — 10 min

You read these papers before sessions 2 to 6. You do not need to re-read them in full: re-read the
**abstract and the description of the data** — what one observation is, and what is measured — so
you know what the models will be fitted on.

| # | Paper | What you will fit |
|---|---|---|
| 1 | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* · [article](https://doi.org/10.1016/j.jinteco.2021.103526) | OLS, binary, ordinal and multinomial logits |
| 2 | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* · [article](https://doi.org/10.1371/journal.pone.0224194) | binary, ordinal and multinomial logits |
| 3 | Blonigen & Piger (2014), *Determinants of foreign direct investment* · [article](https://doi.org/10.1111/caje.12091) · [free preprint](https://www.nber.org/papers/w16704) | OLS, ridge, lasso, elastic net |
| 4 | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* · [article](https://doi.org/10.1162/REST_a_00095) | OLS, binary, ordinal and multinomial logits, ridge, lasso, elastic net |

---

## 2. Set up your session-07 folder — 15 min

Make an empty folder **outside** the course repository — `Desktop/session-07`, say — and open it
in VS Codium (**File → Open Folder…**). Then, in its terminal (**Terminal → New Terminal**):

### macOS

```bash
open /Applications/Python\ 3*/Install\ Certificates.command   # python.org Python only, once
python3 -m venv .venv
source .venv/bin/activate
pip install pandas statsmodels scikit-learn matplotlib
curl -LO https://warint.github.io/quantitative-methods/session-07-scripts.zip
unzip session-07-scripts.zip
python check_setup.py
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pandas statsmodels scikit-learn matplotlib
curl -LO https://warint.github.io/quantitative-methods/session-07-scripts.zip
unzip session-07-scripts.zip
python check_setup.py
```

If `unzip` is missing: `sudo apt install unzip` (Debian, Ubuntu) or `sudo dnf install unzip` (Fedora).

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install pandas statsmodels scikit-learn matplotlib
$zip = "https://warint.github.io/quantitative-methods/session-07-scripts.zip"
Invoke-WebRequest $zip -OutFile session-07-scripts.zip
Expand-Archive session-07-scripts.zip -DestinationPath .
python check_setup.py
```

The last line checks Python, the four packages, and that the four data files on the course site
answer. Every line should say `OK`. A `MISSING` package prints the `pip install` to type.

> No `requirements.txt`, no download of the papers' packages: plain Python, four packages by name,
> and each script reads its paper's data from the course site — so on the day, you need the
> internet. The step-by-step version is [Part 0 of the workshop](../02-practice/README.md#part-0--set-up--15-min).

---

## 3. Bring the right questions — 5 min

For each paper, write one line on paper, from memory:

1. What is the research question?
2. What is the simplest model from sessions 3 to 6 that could answer it?

You will check both against the guides in the first minutes of each paper.

---

## Arrive with

- [ ] `check_setup.py` all `OK`
- [ ] Your two lines per paper, on paper
- [ ] Your group decided: alone, split-and-teach, or pairs ([how](../02-practice/README.md#alone-or-in-a-team--both-work))

---

[Session 07 overview](../README.md) · [The workshop](../02-practice/README.md)
