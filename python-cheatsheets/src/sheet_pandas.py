"""pandas — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import grid, arrow, svg, text, small  # noqa: E402

ACCENT = "#150458"
BLUE, RED, GREEN, SAND = "#cfe0f5", "#f8d3cd", "#d4ecd9", "#f2efe8"

META = dict(
    title="pandas",
    color=ACCENT,
    tagline="Data in tables: load it, look at it, select, clean, summarise, combine",
    sessions="2 to 13",
)
META["import"] = "import pandas as pd"
META["version_note"] = "a DataFrame is a table; a Series is one column"


def anatomy():
    b = grid(70, 22, 4, 4, cell=18, fills={("col", 0): "#fff"})
    b += "".join(text(70 + 9 + 18 * c, 17, n, 7) for c, n in enumerate(["geo", "time", "gdp", "pop"]))
    b += "".join(text(60, 34 + 18 * r, str(r), 7, "end") for r in range(4))
    b += text(110, 112, "columns: d.columns · index: d.index · values", 7.5)
    b += text(18, 50, "index", 7.5, "middle", "#150458", "bold")
    b += text(230, 30, "d.shape", 7.5, "start", "#150458", "bold")
    b += text(230, 42, "→ (4, 4)", 7.5, "start")
    b += text(230, 66, 'd["gdp"]', 7.5, "start", "#150458", "bold")
    b += text(230, 78, "→ a Series", 7.5, "start")
    b += f'<rect x="106" y="22" width="18" height="72" fill="none" stroke="#e3120b" stroke-width="2"/>'
    return svg(300, 118, b)


def selecting():
    b = text(50, 10, 'd[["a", "c"]]', 7.5, "middle", ACCENT, "bold")
    b += grid(20, 16, 4, 4, 14, fills={("col", 0): BLUE, ("col", 2): BLUE})
    b += text(150, 10, "d.loc[d.x > 0]", 7.5, "middle", ACCENT, "bold")
    b += grid(122, 16, 4, 4, 14, fills={("row", 1): RED, ("row", 3): RED})
    b += text(250, 10, 'd.loc[d.x > 0, "a"]', 7.5, "middle", ACCENT, "bold")
    b += grid(222, 16, 4, 4, 14, fills={(1, 0): GREEN, (3, 0): GREEN})
    b += text(50, 86, "columns", 7) + text(150, 86, "rows that meet a condition", 7) + text(250, 86, "both", 7)
    return svg(300, 92, b)


def split_apply():
    fills_in = {("row", 0): BLUE, ("row", 1): RED, ("row", 2): BLUE, ("row", 3): GREEN, ("row", 4): RED}
    b = grid(8, 14, 5, 2, 13, fills=fills_in)
    b += text(21, 10, "d", 7.5, "middle", ACCENT, "bold")
    b += arrow(40, 46, 70, 46, label="split")
    b += grid(76, 6, 2, 2, 13, fills={("row", 0): BLUE, ("row", 1): BLUE})
    b += grid(76, 38, 2, 2, 13, fills={("row", 0): RED, ("row", 1): RED})
    b += grid(76, 70, 1, 2, 13, fills={("row", 0): GREEN})
    b += arrow(110, 46, 140, 46, label="apply mean")
    b += grid(146, 14, 1, 1, 13, fills={(0, 0): BLUE}) + grid(146, 40, 1, 1, 13, fills={(0, 0): RED})
    b += grid(146, 66, 1, 1, 13, fills={(0, 0): GREEN})
    b += arrow(165, 46, 195, 46, label="combine")
    b += grid(201, 27, 3, 2, 13, fills={(0, 0): BLUE, (1, 0): RED, (2, 0): GREEN})
    b += text(214, 22, "result", 7)
    return svg(240, 90, b)


def merge_pic():
    L = grid(10, 18, 3, 2, 13, fills={(0, 0): BLUE, (1, 0): RED, (2, 0): SAND})
    Rr = grid(60, 18, 3, 2, 13, fills={(0, 0): BLUE, (1, 0): RED, (2, 0): GREEN})
    b = L + Rr + text(23, 13, "left", 7) + text(73, 13, "right", 7)
    b += text(160, 13, 'how="inner"', 7, "middle", ACCENT, "bold")
    b += grid(140, 18, 2, 3, 13, fills={(0, 0): BLUE, (1, 0): RED})
    b += text(250, 13, 'how="left"', 7, "middle", ACCENT, "bold")
    b += grid(230, 18, 3, 3, 13, fills={(0, 0): BLUE, (1, 0): RED, (2, 0): SAND, (2, 2): "#eee"})
    b += text(250, 72, "NaN where no match", 6.5)
    b += text(55, 72, 'on="geo" — the key column', 6.5)
    return svg(300, 78, b)


def hist_describe():
    import qmib
    g = qmib.load("core")["gdp_pc_eur"].dropna()
    fig, ax = small(3.0, 1.45)
    ax.hist(g, bins=30, color="#7a8fbf")
    ax.axvline(g.mean(), color="#e3120b", lw=1.6, label=f"mean {g.mean():,.0f}")
    ax.axvline(g.median(), color="#2e8b57", lw=1.6, ls="--", label=f"median {g.median():,.0f}")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v/1000:.0f}k")
    ax.set_xlabel("GDP per capita (EUR), 30 countries 2009–2023", fontsize=7); ax.legend(fontsize=6, frameon=False)
    return fig


def bars_counts():
    import qmib
    s = qmib.load("hsbdemo")["prog"].value_counts()
    fig, ax = small(3.0, 1.2)
    ax.barh(s.index, s.values, color="#7a8fbf")
    for i, v in enumerate(s.values):
        ax.text(v + 2, i, str(v), va="center", fontsize=6.5)
    ax.set_xlabel('ml["prog"].value_counts()', fontsize=7)
    return fig


PAGES = [[
    dict(title="1 · Get data in, and out",
         intro="One line from a file to a DataFrame. Say which sheet, which columns.",
         items=[
             dict(code='pd.read_csv("file.csv")', text="a comma-separated file.",
                  ex='d = pd.read_csv("data/my_data.csv")'),
             dict(code='pd.read_parquet(path)', text="the course's own format: fast, keeps types.",
                  ex='core = pd.read_parquet("data/spine/core.parquet")'),
             dict(code='pd.read_stata(path, columns=[...])', text="an author's Stata `.dta` file; read only the columns you need.",
                  ex='d = pd.read_stata(path, columns=["iso", "F0_index"])'),
             dict(code='pd.read_excel(path, sheet_name=1)', text="an Excel workbook; sheets count from 0."),
             dict(code='qmib.load("core")', text="a course dataset by name: downloaded once, cached."),
             dict(code='d.to_csv("out.csv", index=False)', text="write a table out; `index=False` drops the row numbers."),
         ]),
    dict(title="2 · Look before you model",
         figure_top=anatomy,
         items=[
             dict(code="d.head()  ·  d.shape  ·  d.dtypes", text="the first rows · (rows, columns) · the type of each column."),
             dict(code="d.describe()", text="count, mean, sd, min, quartiles, max of every numeric column."),
             dict(code="d.isna().sum()", text="how many values are missing, column by column."),
             dict(code='d["iso"].nunique()', text="how many distinct values — countries, firms, groups."),
             dict(code='d["prog"].value_counts()', text="how often each category occurs; `normalize=True` for shares."),
         ],
         figure=bars_counts),
    dict(title="3 · Select rows and columns",
         figure_top=selecting,
         items=[
             dict(code='d["gdp"]  ·  d[["gdp", "pop"]]', text="one column (a Series) · several (a DataFrame): note the double brackets."),
             dict(code="d[d.gdp > 30000]", text="the rows that meet a condition; combine with `&` (and) and `|` (or), each in brackets."),
             dict(code='d.loc[rows, cols]', text="select by **label** and by condition at once.",
                  ex='d.loc[d.time == 2022, ["geo", "gdp"]]'),
             dict(code="d.iloc[0:5, 0:3]", text="select by **position**: rows 0–4, columns 0–2."),
             dict(code='d[d["event"].isin(["growing", "shrinking"])]', text="the rows whose value is in a list."),
         ],
         warn="Select a subset, then add columns? Take `.copy()` first, or pandas warns you are writing on a view."),
    dict(title="4 · Clean",
         items=[
             dict(code='d.dropna(subset=["y", "x"])', text="drop rows missing **those** columns. Without `subset=`, a gap in *any* column drops the row."),
             dict(code='d["x"].astype(float)', text="change a column's type: text to number, number to category."),
             dict(code='d.rename(columns={"old": "new"})', text="rename columns."),
             dict(code='d.sort_values("gdp", ascending=False)', text="sort the rows."),
         ],
         tip="Count rows before and after every cleaning step: what you dropped is part of your result."),
], [
    dict(title="5 · Make new columns",
         items=[
             dict(code='d["log_gdp"] = np.log(d["gdp"])', text="a new column from old ones; arithmetic works column by column."),
             dict(code='d["up"] = (d["ret"] > 0).astype(int)', text="a 0/1 column from a condition — the outcome of a logit."),
             dict(code='d.loc[d.foreign == 1, "owner"] = "foreign"', text="set a value only on the rows that meet a condition."),
             dict(code='pd.qcut(d["tfp"], 3, labels=["low", "mid", "high"])', text="cut a number into equal-sized groups."),
             dict(code='pd.Categorical(x, categories=order, ordered=True)', text="categories **with an order** — what an ordinal logit needs."),
             dict(code='pd.get_dummies(d["region"], drop_first=True)', text="one 0/1 column per category, minus a reference — for a model without a formula."),
         ]),
    dict(title="6 · Summarise",
         figure_top=hist_describe,
         items=[
             dict(code='d["gdp"].mean()  .median()  .std()', text="centre and spread of one column (session 2)."),
             dict(code='d["gdp"].quantile([0.25, 0.5, 0.75])', text="quartiles: the IQR is the third minus the first."),
             dict(code='d[["gdp", "pop"]].corr()', text="the correlation matrix — before a regression, look for near-twins."),
             dict(code='pd.crosstab(d["ses"], d["prog"])', text="a contingency table: counts of each combination."),
         ]),
    dict(title="7 · Split, apply, combine — groupby",
         figure_top=split_apply,
         items=[
             dict(code='d.groupby("geo")["gdp"].mean()', text="one summary per group: here, each country's mean GDP."),
             dict(code='d.groupby("yr")[["tariff", "input"]].mean()', text="several columns at once: the average tariffs by year."),
             dict(code='d.groupby("event")[X].median()', text="compare the groups before modelling them."),
         ]),
    dict(title="8 · Combine tables",
         figure_top=merge_pic,
         items=[
             dict(code='left.merge(right, on=["geo", "time"], how="inner")', text="join on key columns; `inner` keeps matches only, `left` keeps every left row."),
             dict(code="pd.concat([a, b])  ·  pd.concat([a, b], axis=1)", text="stack tables on top of each other · side by side."),
         ],
         warn="After a merge, check the number of rows: a duplicated key silently multiplies them."),
    dict(title="9 · A first script, in order",
         intro="The shape of almost every analysis in this course.",
         items=[
             dict(code="1 · load", text="", ex='core = qmib.load("core")'),
             dict(code="2 · keep what you need", text="", ex='d = core.dropna(subset=["gdp_pc_eur", "productivity_idx"])'),
             dict(code="3 · look", text="", ex='print(d.shape); print(d.describe().round(1))'),
             dict(code="4 · summarise by group", text="", ex='d.groupby("geo")["gdp_pc_eur"].median()'),
             dict(code="5 · model (statsmodels, scikit-learn)", text="", ex='smf.ols("gdp_pc_eur ~ productivity_idx", data=d).fit()'),
         ]),
    dict(title="10 · When pandas complains",
         items=[
             dict(code="KeyError: 'gdp'", text="no column by that name: check `d.columns` for the exact spelling."),
             dict(code="SettingWithCopyWarning", text="you added a column to a slice: take `.copy()` when you select."),
             dict(code="ValueError: ... NaN ...", text="missing values where a number is needed: `dropna` first, or `fillna`."),
             dict(code="... in the printout", text="pandas hid columns or rows: `pd.set_option` below, or select fewer."),
         ]),
    dict(title="11 · Display",
         items=[
             dict(code='pd.set_option("display.max_columns", 10)', text="how many columns print before pandas shows `...`."),
             dict(code="d.round(3)", text="round every number for reading — not for computing."),
         ]),
]]
