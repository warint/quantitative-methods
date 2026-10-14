# Python cheatsheets, one per package

One sheet per Python package, in the spirit of the
[RStudio cheatsheets](https://rmarkdown.rstudio.com/lesson-15.HTML): boxed sections, a plain
sentence for each function, a line of code on the course's data, and a picture of what the
function does or produces. Only the functions this course uses — or the ones you will want next.

**Open them on the site:** [warint.github.io/quantitative-methods/python-cheatsheets/](https://warint.github.io/quantitative-methods/python-cheatsheets/)

| Sheet | What it covers | Sessions |
|---|---|---|
| [`pandas.pdf`](pandas.pdf) | tables: load, look, select, clean, summarise, combine | 2 to 13 |
| [`numpy.pdf`](numpy.pdf) | arrays, logs and exponentials, grids, linear algebra, random numbers | 2 to 13 |
| [`matplotlib.pdf`](matplotlib.pdf) | the anatomy of a figure, and the plots the course draws | 3 to 13 |
| [`statsmodels.pdf`](statsmodels.pdf) | OLS from a formula, diagnostics, binary, ordinal and multinomial logits | 2 to 7, 10, 11, 13 |
| [`sklearn.pdf`](sklearn.pdf) | scikit-learn: fit and predict, pipelines, ridge, lasso, elastic net, cross-validation, KNN | 5 to 8, 10, 13 |
| [`scipy.pdf`](scipy.pdf) | `scipy.stats`: shape statistics, tests, distributions | 2, 4, 5, 6, 9, 10 |
| [`linearmodels.pdf`](linearmodels.pdf) | panel data: fixed and random effects | 6 |
| [`semopy.pdf`](semopy.pdf) | structural equation models | 9 |
| [`prince.pdf`](prince.pdf) | PCA and FAMD | 13 |

Each session's README, and the *Your Python so far* slide of its decks, link to the sheets that
session uses. The session cheatsheets (`PYTHON-CHEATSHEET.pdf` in each session folder) are a
different thing: one line for every name taught so far, in the order you met them.

## Rebuilding them

The content of each sheet is a Python file in [`src/`](src/), `sheet_<package>.py`: its sections,
entries and figures. To rebuild, from the repository root:

```bash
python scripts/build_package_cheatsheets.py            # every sheet
python scripts/build_package_cheatsheets.py pandas     # one sheet
```

The script lays the sheets out as HTML and prints them to PDF with Chrome (or Chromium), which must
be installed; the figures are drawn on the course data. Then `python scripts/build_docs.py`
publishes them to the site.
