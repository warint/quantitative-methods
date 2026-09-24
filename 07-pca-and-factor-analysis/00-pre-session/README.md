# Session 07 — Before the workshop

**Wednesday 14 October 2026** · 15:30–18:30 · Décelles — Victoriaville

> The workshop is three hours of work at your own keyboard. It goes well if the data is already
> on your machine when you arrive, and badly if you spend the first hour downloading.
> This page is **30 minutes**, most of it waiting for downloads.

---

## 1. Re-read the five abstracts — 10 min

You read these papers before sessions 2 to 6. You do not need to re-read them in full: re-read the
**abstract and the one table or figure** each replication aims at, so you know what you are looking
for.

| # | Paper | Re-read |
|---|---|---|
| 1 | Fraiberger, Lee, Puy & Ranciere (2021), *Media sentiment and international asset prices* · [article](https://doi.org/10.1016/j.jinteco.2021.103526) | Figure 2, panel B |
| 2 | Amsili, van Es & Schindelbeck (2024), *Pedotransfer functions …* · [article](https://doi.org/10.1080/00103624.2024.2336573) | Equation 6 and Figure 2, p. 8 |
| 3 | Saganowski, Bródka, Koziarski & Kazienko (2019), *Analysis of group evolution prediction in complex networks* · [article](https://doi.org/10.1371/journal.pone.0224194) | the six events, and Table F of the S1 File |
| 4 | Blonigen & Piger (2014), *Determinants of foreign direct investment* · [article](https://doi.org/10.1111/caje.12091) · [free preprint](https://www.nber.org/papers/w16704) | Table 3, the inclusion probabilities |
| 5 | Topalova & Khandelwal (2011), *Trade liberalization and firm productivity* · [article](https://doi.org/10.1162/REST_a_00095) | Table 5, columns 1 and 3 |

---

## 2. Make sure the data is on your machine — 15 min, mostly waiting

Four of the five papers use the authors' Dataverse package, which you were asked to download
before its own session. Paper 4 needs no download: `qmib.load("fdi")` reads a file already in the
repository.

**First, check what you already have.** Open the repository in VS Codium and run
[`02-practice/starter/check_setup.py`](../02-practice/starter/check_setup.py) with the **Run** triangle.
Every line that says `OK` is done. For each line that says `MISSING`, run the matching command
below **from the repository root**, in the VS Codium terminal.

| Paper | Package | Size of the download |
|---|---|---|
| 1 · Fraiberger et al. | [10.7910/DVN/QNKFJF](https://doi.org/10.7910/DVN/QNKFJF) | about 35 MB |
| 2 · Amsili et al. | [10.7910/DVN/U5DAEP](https://doi.org/10.7910/DVN/U5DAEP) | about 220 MB |
| 3 · Saganowski et al. | [10.7910/DVN/ONOFS7](https://doi.org/10.7910/DVN/ONOFS7) | about 160 MB |
| 5 · Topalova & Khandelwal | [10.7910/DVN/8WEXYD](https://doi.org/10.7910/DVN/8WEXYD) | about 2 MB |

### macOS

```bash
get() { curl -L "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/$1" -o "$1.zip" && mkdir -p "$2/data/replication" && unzip -o -q "$1.zip" -d "$2/data/replication" && rm "$1.zip"; }
get QNKFJF 02-exploratory-data-analysis
get U5DAEP 03-regression-adequacy-and-validity
get ONOFS7 04-logistic-ordinal-multinomial
get 8WEXYD 06-advanced-regression
```

### Linux

```bash
get() { curl -L "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/$1" -o "$1.zip" && mkdir -p "$2/data/replication" && unzip -o -q "$1.zip" -d "$2/data/replication" && rm "$1.zip"; }
get QNKFJF 02-exploratory-data-analysis
get U5DAEP 03-regression-adequacy-and-validity
get ONOFS7 04-logistic-ordinal-multinomial
get 8WEXYD 06-advanced-regression
```

If `unzip` is missing: `sudo apt install unzip` (Debian, Ubuntu) or `sudo dnf install unzip` (Fedora).

### Windows (PowerShell)

```powershell
function Get-Package($doi, $dir) {
  curl.exe -L "https://dataverse.harvard.edu/api/access/dataset/:persistentId/?persistentId=doi:10.7910/DVN/$doi" -o "$doi.zip"
  Expand-Archive "$doi.zip" -DestinationPath "$dir\data\replication" -Force
  Remove-Item "$doi.zip"
}
Get-Package QNKFJF 02-exploratory-data-analysis
Get-Package U5DAEP 03-regression-adequacy-and-validity
Get-Package ONOFS7 04-logistic-ordinal-multinomial
Get-Package 8WEXYD 06-advanced-regression
```

Type `curl.exe`, not `curl`: in PowerShell, `curl` is a different command.

> Run only the lines you need — each `get` line fetches one package. The folders are
> **git-ignored**, so nothing large is ever committed. If a download is refused (Dataverse
> sometimes asks you to accept terms first), open the DOI in a browser, click
> **Access Dataset → Download ZIP**, and unzip it into the same folder.

Then run `check_setup.py` again. Every line should now say `OK`.

---

## 3. Bring the right questions — 5 min

For each paper, write one line on paper, from memory:

1. What is the research question?
2. What is the one number the paper's argument rests on?

You will check both against the guides in the first minutes of each replication.

---

## Arrive with

- [ ] `check_setup.py` all `OK`
- [ ] The five target tables or figures located
- [ ] Your two lines per paper, on paper
- [ ] Your group decided: alone, split-and-teach, or pairs ([how](../02-practice/README.md#alone-or-in-a-team--both-work))

---

[Session 07 overview](../README.md) · [The workshop](../02-practice/README.md)
