"""numpy — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import grid, arrow, svg, text, small  # noqa: E402

ACCENT = "#013243"
BLUE, RED, GREEN, SAND = "#cfe0f5", "#f8d3cd", "#d4ecd9", "#f2efe8"

META = dict(
    title="numpy",
    color=ACCENT,
    tagline="Numbers in arrays: fast arithmetic, logs and exponentials, grids, random draws, linear algebra",
    sessions="2 to 13",
)
META["import"] = "import numpy as np"
META["version_note"] = "pandas columns are numpy arrays underneath"


def shapes():
    b = text(30, 12, "1-D  shape (4,)", 7.5, "middle", ACCENT, "bold")
    b += grid(4, 20, 1, 4, 13, fills={("row", 0): BLUE})
    b += text(130, 12, "2-D  shape (3, 4)", 7.5, "middle", ACCENT, "bold")
    b += grid(104, 20, 3, 4, 13, fills={("row", 0): BLUE, ("row", 1): BLUE, ("row", 2): BLUE})
    b += text(130, 72, "rows × columns", 7)
    b += text(240, 12, "a.mean(axis=0)", 7.5, "middle", ACCENT, "bold")
    b += grid(214, 20, 3, 4, 13, fills={("col", 0): RED, ("col", 1): GREEN, ("col", 2): BLUE, ("col", 3): SAND})
    b += arrow(240, 62, 240, 74)
    b += grid(214, 76, 1, 4, 13, fills={(0, 0): RED, (0, 1): GREEN, (0, 2): BLUE, (0, 3): SAND})
    b += text(240, 100, "down the rows: one value per column", 6.5)
    b += text(30, 46, "a[0], a[-1]", 7, "middle")
    b += text(30, 56, "first, last", 6.5, "middle", "#666")
    return svg(300, 106, b)


def broadcast():
    b = text(32, 10, "a  (3, 4)", 7.5, "middle", ACCENT, "bold")
    b += grid(6, 16, 3, 4, 13, fills={("row", 0): BLUE, ("row", 1): BLUE, ("row", 2): BLUE})
    b += text(76, 38, "−", 12)
    b += text(118, 10, "a.mean(axis=0)  (4,)", 7.5, "middle", ACCENT, "bold")
    b += grid(92, 16, 1, 4, 13, fills={("row", 0): RED})
    b += "".join(grid(92, 16 + 13 * r, 1, 4, 13, fills={("row", 0): "#fbe9e6"}, stroke="#bbb") for r in (1, 2))
    b += text(118, 66, "stretched to (3, 4)", 6.5, "middle", "#666")
    b += text(162, 38, "=", 12)
    b += text(205, 10, "centred  (3, 4)", 7.5, "middle", ACCENT, "bold")
    b += grid(178, 16, 3, 4, 13, fills={("row", 0): GREEN, ("row", 1): GREEN, ("row", 2): GREEN})
    b += text(150, 84, "shapes are matched from the right; a length-1 side repeats", 6.8)
    return svg(250, 90, b)


def odds_curve():
    import numpy as np
    fig, ax = small(3.0, 1.5)
    b = np.linspace(-2.5, 2.5, 200)
    ax.plot(b, np.exp(b), color=ACCENT, lw=2, label="odds ratio  np.exp(b)")
    ax.axhline(1, color="#888", lw=0.8, ls=":")
    ax.axvline(0, color="#888", lw=0.8, ls=":")
    for v, off in ((-0.5, (-48, 14)), (0.5, (8, 14))):
        ax.plot(v, np.exp(v), "o", color="#e3120b", ms=4)
        ax.annotate(f"e^({v:+.1f}) = {np.exp(v):.2f}", (v, np.exp(v)), fontsize=6,
                    xytext=off, textcoords="offset points",
                    arrowprops=dict(arrowstyle="-", color="#999", lw=0.6))
    ax.set_ylim(0, 8)
    ax.set_xlabel("logit coefficient b (log-odds)", fontsize=7)
    ax.legend(fontsize=6, frameon=False, loc="upper left")
    return fig


def lam_grid():
    import numpy as np
    fig, ax = small(3.0, 0.9)
    g = np.logspace(-3, 3, 13)
    ax.semilogx(g, np.zeros_like(g), "o", color=ACCENT, ms=4)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("np.logspace(-3, 3, 13): evenly spaced on a log axis", fontsize=7)
    return fig


def draws():
    import numpy as np
    rng = np.random.default_rng(1)
    x = rng.normal(0, 1, 2000)
    fig, ax = small(3.0, 1.3)
    ax.hist(x, bins=40, color="#6f8fa6")
    ax.set_xlabel("rng.normal(0, 1, 2000) — the same every run with seed 1", fontsize=7)
    return fig


def sim_fig():
    import numpy as np
    rng = np.random.default_rng(3)
    cov = [[1, .95], [.95, 1]]
    ols, rdg = [], []
    for _ in range(400):
        Xs = rng.multivariate_normal([0, 0], cov, 30)
        ys = Xs @ [1, 1] + rng.normal(0, 1, 30)
        Xc, yc = Xs - Xs.mean(0), ys - ys.mean()
        ols.append(np.linalg.solve(Xc.T @ Xc, Xc.T @ yc)[0])
        rdg.append(np.linalg.solve(Xc.T @ Xc + 10 * np.eye(2), Xc.T @ yc)[0])
    fig, ax = small(3.0, 1.45)
    bins = np.linspace(-1.5, 3.5, 41)
    ax.hist(ols, bins, color="#e3120b", alpha=.5, label="OLS")
    ax.hist(rdg, bins, color=ACCENT, alpha=.75, label="ridge, λ = 10")
    ax.axvline(1, color="black", lw=1)
    ax.set_xlabel("slope estimate in 400 samples (truth = 1)", fontsize=7)
    ax.legend(fontsize=6, frameon=False)
    return fig


PAGES = [[
    dict(title="1 · Arrays and their shape",
         intro="An array is a grid of numbers of one type. Its shape says how many rows and columns.",
         figure_top=shapes,
         items=[
             dict(code="np.array([1.0, 2.5, 4.0])", text="an array from a list."),
             dict(code='np.asarray(d["gdp"])  ·  d.to_numpy()', text="a pandas column or table as a plain array — what scikit-learn works on.",
                  ex='X = d[XCOLS].to_numpy(float)'),
             dict(code="a.shape  ·  a.ndim  ·  len(a)", text="(rows, columns) · number of dimensions · number of rows."),
             dict(code="a[0]  ·  a[-1]  ·  a[1:3]  ·  a[:, 0]", text="first · last · positions 1–2 · the first column of a 2-D array."),
             dict(code="a[a > 0]", text="keep the elements that meet a condition."),
         ]),
    dict(title="2 · Make arrays",
         items=[
             dict(code="np.arange(0, 10, 2)", text="0, 2, 4, 6, 8 — steps of 2, the end excluded."),
             dict(code="np.linspace(-3, 3, 200)", text="200 evenly spaced points: the x-axis of a smooth curve."),
             dict(code="np.logspace(-3, 3, 60)", text="60 values from 0.001 to 1000, even on a **log** scale: the grid of λ for ridge and lasso."),
             dict(code="np.zeros(5)  ·  np.ones((3, 2))  ·  np.full_like(y, y.mean())", text="filled arrays; the last one is a \"predict the mean\" benchmark."),
         ],
         figure=lam_grid),
    dict(title="3 · Arithmetic, element by element",
         intro="Operators and functions act on every element at once — no loop.",
         items=[
             dict(code="a + b  ·  a * 2  ·  a ** 2", text="element by element; arrays of different shapes are **broadcast**."),
             dict(code="np.sqrt(a)  ·  np.abs(a)  ·  np.sign(a)", text="square root · absolute value · −1, 0 or +1.",
                  ex="rmse = np.sqrt(np.mean((y - y_hat) ** 2))"),
             dict(code="np.round(a, 3)  ·  np.clip(a, 0, None)", text="round · cap below at 0 (the lasso's \"keep only what is above λ\")."),
         ],
         figure=broadcast),
    dict(title="4 · Summaries, and the axis",
         items=[
             dict(code="np.mean(a)  ·  np.median(a)  ·  np.std(a, ddof=1)", text="centre and spread; `ddof=1` divides by n − 1, as the sample SD does."),
             dict(code="np.sum(a)  ·  np.cumsum(a)", text="total · running total."),
             dict(code="a.mean(axis=0)  ·  a.mean(axis=1)", text="down the rows (one per column) · across the columns (one per row)."),
             dict(code="np.sum(coef != 0)", text="count what is True: here, how many coefficients the lasso kept.",
                  ex="kept = int(np.sum(np.abs(pipe[-1].coef_) > 1e-8))"),
             dict(code="np.argmax(a)  ·  np.argsort(-np.abs(a))", text="position of the largest · positions from largest to smallest in size."),
         ]),
    dict(title="5 · Logs and exponentials",
         figure_top=odds_curve,
         items=[
             dict(code="np.log(x)", text="natural log. A skewed outcome on a log scale: a slope then reads in %.",
                  ex="y = np.log(d.fdi_stock_musd)"),
             dict(code="np.exp(b)", text="undo the log. On a logit coefficient: log-odds → **odds ratio**.",
                  ex='np.exp(m2.params["fico"])     # 0.988: odds 1.2% lower per point'),
             dict(code="np.exp(xb) / (1 + np.exp(xb))", text="the logistic function: a linear index → a probability between 0 and 1."),
         ],
         tip="An odds ratio above 1 raises the odds; below 1 lowers them. It multiplies the odds, not the probability."),
], [
    dict(title="6 · Conditions",
         items=[
             dict(code='np.where(x > 0, "up", "down")', text="one value where the condition holds, another elsewhere."),
             dict(code="np.maximum(a, 0)", text="element by element, the larger of two: here, negative values become 0."),
         ]),
    dict(title="7 · Random draws, reproducibly",
         intro="Simulations make the bias–variance trade-off visible. Fix the seed, so a run can be repeated.",
         items=[
             dict(code="rng = np.random.default_rng(7)", text="a random generator with a seed: the same numbers on every machine."),
             dict(code="rng.normal(0, 1, size=n)", text="n draws from a normal distribution, mean 0, sd 1."),
             dict(code="rng.integers(0, n, n)", text="n row numbers drawn with replacement — a bootstrap resample.",
                  ex="idx = rng.integers(0, len(d), len(d)); d.iloc[idx]"),
             dict(code="rng.multivariate_normal(mean, cov, n)", text="correlated draws: two predictors at 0.95, for the ridge picture."),
         ],
         figure=draws),
    dict(title="8 · Correlation and linear algebra",
         intro="The arithmetic behind a regression, when you want to see it.",
         items=[
             dict(code="np.corrcoef(x, y)", text="the correlation matrix of two (or more) variables.",
                  ex="np.corrcoef(rd, patents)[0, 1]   # 0.95: near-twins"),
             dict(code="X.T @ X  ·  X.T @ y", text="`.T` transposes, `@` multiplies matrices — the pieces of OLS."),
             dict(code="np.linalg.solve(X.T @ X, X.T @ y)", text="the OLS coefficients, (XᵀX)⁻¹Xᵀy, without forming the inverse."),
             dict(code="np.linalg.solve(XtX + lam * np.eye(p), Xty)", text="ridge: add λ on the diagonal — solvable even when XᵀX is not."),
             dict(code="np.linalg.inv(A)  ·  np.linalg.pinv(A)", text="inverse · pseudo-inverse, which works on a nearly singular matrix."),
             dict(code="np.linalg.eigvalsh(np.corrcoef(Z, rowvar=False))", text="eigenvalues of a correlation matrix: the scree plot of PCA."),
         ]),
    dict(title="9 · A simulation in a few lines",
         intro="Why ridge helps, shown with numpy alone: re-draw the data many times, re-fit, look at the spread.",
         items=[
             dict(code="for _ in range(S): ...", text="draw a sample, fit OLS and ridge, keep the slope.",
                  ex="Xs = rng.multivariate_normal([0, 0], cov, 30)\nys = Xs @ [1, 1] + rng.normal(0, 1, 30)"),
         ],
         figure=sim_fig),
    dict(title="10 · Combine and reshape",
         items=[
             dict(code="np.vstack([a, b])  ·  np.c_[x, y]", text="stack rows on top of each other · put arrays side by side as columns."),
             dict(code="a.reshape(3, 4)  ·  a.ravel()", text="the same numbers in a new shape · flattened back to 1-D."),
             dict(code="G1, G2 = np.meshgrid(g, g)", text="every pair of two grids: the canvas for a contour plot (ridge and lasso budgets)."),
             dict(code="np.diag(a)  ·  np.eye(p)", text="a diagonal matrix · the identity, as in XᵀX + λI."),
         ]),
    dict(title="11 · numpy and pandas",
         intro="Most of the time pandas holds the data and numpy does the arithmetic on its columns.",
         items=[
             dict(code='np.log(d["gdp"])', text="numpy functions accept a pandas column and return one, index kept."),
             dict(code="d.to_numpy()  ·  pd.DataFrame(a, columns=[...])", text="table → array · array → table with names."),
             dict(code="m.predict(X).values", text="`.values` takes the plain array out of a pandas result."),
         ],
         tip="Prefer pandas while the column names help you; drop to numpy for maths that has no name."),
    dict(title="12 · When numpy complains",
         items=[
             dict(code="ValueError: operands could not be broadcast", text="the shapes do not line up: print `a.shape` and `b.shape`."),
             dict(code="nan in the result", text="a missing value spreads: `np.nanmean(a)` skips it, or drop it in pandas first."),
             dict(code="RuntimeWarning: divide by zero in log", text="`np.log(0)` is −inf: keep positive values only, or use `np.log1p`."),
         ]),
]]
