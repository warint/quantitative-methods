"""scikit-learn — the content of the cheatsheet. Built by scripts/build_package_cheatsheets.py."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _draw import grid, arrow, svg, text, small  # noqa: E402

ACCENT = "#c45f00"
BLUE, RED, GREEN, SAND, ORANGE = "#cfe0f5", "#f8d3cd", "#d4ecd9", "#f2efe8", "#fbe0c3"

META = dict(
    title="scikit-learn",
    color=ACCENT,
    tagline="Models that learn from data: fit, predict, penalise, cross-validate, score",
    sessions="5 to 8, 10 and 13",
)
META["import"] = "from sklearn.linear_model import LassoCV"
META["version_note"] = "import each tool from its module: linear_model, preprocessing, …"


def _rect(x, y, w, h, fill, label, size=7.5, stroke="#555"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="0.9"/>' + text(x + w / 2, y + h / 2 + 3, label, size))


def api():
    b = _rect(4, 26, 70, 26, ORANGE, "model = Lasso()", 7)
    b += arrow(76, 39, 104, 39, label="")
    b += _rect(106, 26, 74, 26, BLUE, ".fit(X, y)", 7.5)
    b += arrow(182, 39, 208, 39)
    b += _rect(210, 18, 86, 18, GREEN, ".predict(X_new)", 7)
    b += _rect(210, 42, 86, 18, SAND, ".coef_  .alpha_", 7)
    b += text(39, 18, "1 · choose", 7, "middle", ACCENT, "bold")
    b += text(143, 18, "2 · learn", 7, "middle", ACCENT, "bold")
    b += text(253, 12, "3 · use", 7, "middle", ACCENT, "bold")
    b += text(150, 76, "X: a table of predictors (rows × columns) · y: the outcome, one value per row", 6.8)
    return svg(300, 84, b)


def split_pic():
    b = ""
    for i in range(10):
        f = BLUE if i < 7 else RED
        b += f'<rect x="{20 + i * 24}" y="14" width="22" height="18" fill="{f}" stroke="#555" stroke-width="0.8"/>'
    b += text(103, 46, "X_tr, y_tr — 70%: the model learns here", 7, "middle", "#2b5d9c")
    b += text(250, 46, "X_te, y_te — 30%", 7, "middle", "#b03a2e")
    b += text(150, 60, "scored once, at the very end", 6.8, "middle", "#b03a2e")
    return svg(300, 66, b)


def kfold():
    b = ""
    for k in range(5):
        y = 6 + k * 14
        for j in range(5):
            f = RED if j == k else BLUE
            b += f'<rect x="{70 + j * 34}" y="{y}" width="32" height="11" fill="{f}" stroke="#555" stroke-width="0.7"/>'
        b += text(62, y + 9, f"fit {k + 1}", 6.8, "end")
    b += text(250, 30, "fit on blue,", 6.8, "start") + text(250, 40, "score on red,", 6.8, "start")
    b += text(250, 50, "average the", 6.8, "start") + text(250, 60, "5 scores", 6.8, "start")
    return svg(300, 80, b)


def leakage():
    b = text(75, 10, "WRONG", 7.5, "middle", "#b03a2e", "bold")
    b += _rect(10, 16, 130, 16, RED, "scaler.fit(ALL rows)", 6.8)
    b += arrow(75, 33, 75, 44)
    b += _rect(10, 46, 130, 16, SAND, "then cross-validate", 6.8)
    b += text(75, 74, "the held-out fold has been seen", 6.5, "middle", "#b03a2e")
    b += text(225, 10, "RIGHT", 7.5, "middle", "#2e8b57", "bold")
    b += _rect(160, 16, 130, 16, GREEN, "make_pipeline(scaler, model)", 6.5)
    b += arrow(225, 33, 225, 44)
    b += _rect(160, 46, 130, 16, SAND, "CV refits the scaler per fold", 6.5)
    b += text(225, 74, "each fold scaled on its own training rows", 6.5, "middle", "#2e8b57")
    return svg(300, 80, b)


def confusion():
    b = text(150, 9, "predicted", 7, "middle", "#333", "bold")
    b += text(115, 22, "Down", 7) + text(185, 22, "Up", 7)
    b += text(55, 40, "actual Down", 7, "end") + text(55, 66, "actual Up", 7, "end")
    cells = [(80, 28, GREEN, "TN"), (150, 28, RED, "FP"), (80, 54, RED, "FN"), (150, 54, GREEN, "TP")]
    for x, y, f, lab in cells:
        b += _rect(x, y, 68, 22, f, lab, 8)
    b += text(270, 40, "precision", 6.8, "middle", ACCENT, "bold") + text(270, 50, "TP/(TP+FP)", 6.5)
    b += text(270, 64, "recall", 6.8, "middle", ACCENT, "bold") + text(270, 74, "TP/(TP+FN)", 6.5)
    return svg(300, 82, b)


def paths():
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import Ridge, lasso_path
    from sklearn.preprocessing import StandardScaler
    root = Path(__file__).resolve().parents[2]
    raw = pd.read_parquet(root / "data" / "spine" / "angle_c_country.parquet")
    ycol = "rd_pct_gdp"
    xcols = [c for c in raw.columns if c not in ("geo", "time", "flag", ycol)]
    d = raw.dropna(subset=[ycol] + xcols)
    Z = StandardScaler().fit_transform(d[xcols].to_numpy(float))
    y = d[ycol].to_numpy(float)
    grid_ = np.logspace(-3, 0.3, 60)
    fig, axes = small(3.1, 1.5)
    fig.clf()
    a1, a2 = fig.subplots(1, 2, sharey=True)
    B = np.array([Ridge(alpha=g * len(y)).fit(Z, y).coef_ for g in grid_])
    al, cl, _ = lasso_path(Z, y, alphas=grid_)
    for k in range(len(xcols)):
        a1.plot(grid_, B[:, k], lw=0.9, color="#7a8fbf")
        a2.plot(al, cl[k], lw=0.9, color="#d9730d")
    for a, t in ((a1, "Ridge: shrinks"), (a2, "Lasso: hits zero")):
        a.set_xscale("log"); a.axhline(0, color="#222", lw=0.6)
        a.set_title(t, fontsize=7); a.tick_params(labelsize=6)
        a.set_xlabel("λ (alpha) →", fontsize=6.5)
        for side in ("top", "right"):
            a.spines[side].set_visible(False)
    a1.set_ylabel("coefficient", fontsize=6.5)
    fig.tight_layout(pad=0.3)
    return fig


def cv_curve():
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LassoCV
    from sklearn.preprocessing import StandardScaler
    root = Path(__file__).resolve().parents[2]
    raw = pd.read_parquet(root / "data" / "spine" / "angle_c_country.parquet")
    ycol = "rd_pct_gdp"
    xcols = [c for c in raw.columns if c not in ("geo", "time", "flag", ycol)]
    d = raw.dropna(subset=[ycol] + xcols)
    Z = StandardScaler().fit_transform(d[xcols].to_numpy(float))
    lc = LassoCV(alphas=np.logspace(-3, 0.2, 50), cv=5, random_state=0, max_iter=50_000).fit(Z, d[ycol])
    err = lc.mse_path_.mean(axis=1)
    fig, ax = small(3.0, 1.25)
    ax.semilogx(lc.alphas_, err, color="#d9730d", lw=1.8)
    ax.axvline(lc.alpha_, color="#2e8b57", ls="--", lw=1.2)
    ax.text(lc.alpha_ / 1.3, err.max() * 0.8, "alpha_: the best λ", fontsize=6.5, color="#2e8b57", ha="right")
    ax.set_xlabel("λ (alpha)", fontsize=6.5); ax.set_ylabel("CV error", fontsize=6.5)
    return fig


PAGES = [[
    dict(title="1 · One pattern for every model",
         intro="Every estimator works the same way: create it, fit it, use it.",
         figure_top=api,
         items=[
             dict(code="model.fit(X, y)", text="learn from the predictors `X` (a table) and the outcome `y` (one column)."),
             dict(code="model.predict(X_new)", text="the model's prediction for new rows."),
             dict(code="model.coef_  ·  model.intercept_", text="the fitted coefficients — scikit-learn's spelling of statsmodels' `.params`."),
             dict(code="model.score(X, y)", text="R² for a regression, accuracy for a classifier."),
         ],
         tip="scikit-learn gives coefficients, not p-values or standard errors. For inference, use statsmodels."),
    dict(title="2 · Hold something back",
         figure_top=split_pic,
         items=[
             dict(code="train_test_split(X, y, test_size=0.3, random_state=7)",
                  text="cut the rows once: learn on 70%, judge on 30% the model never saw.",
                  ex="Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=7)"),
             dict(code="random_state=7", text="the same cut every run, so your numbers reproduce."),
         ]),
    dict(title="3 · Same scale for every predictor",
         intro="A penalty compares coefficient sizes, so units must not decide them.",
         items=[
             dict(code="StandardScaler()", text="rescales each column to mean 0, standard deviation 1."),
             dict(code="make_pipeline(StandardScaler(), model)", text="chains the steps: fit scales then fits; predict scales then predicts.",
                  ex="pipe = make_pipeline(StandardScaler(), LassoCV(cv=5)).fit(Xtr, ytr)"),
             dict(code="pipe[-1]", text="the last step — the model itself: `pipe[-1].coef_`, `pipe[-1].alpha_`."),
         ],
         figure=leakage,
         warn="Standardise **inside** the pipeline. Scaling all rows first lets the test rows leak into training."),
    dict(title="4 · Ridge, lasso, elastic net",
         intro="OLS plus a price on big coefficients. In scikit-learn, λ is called **alpha**.",
         items=[
             dict(code="LinearRegression()", text="plain OLS: the benchmark, no penalty."),
             dict(code="Ridge(alpha=10)", text="shrinks every coefficient, keeps them all."),
             dict(code="Lasso(alpha=0.8)", text="shrinks, and sets the weak ones to exactly 0: it selects."),
             dict(code="ElasticNet(alpha=1, l1_ratio=0.5)", text="a mix: `l1_ratio` 1 is the lasso, 0 is ridge. Keeps correlated predictors together."),
         ],
         figure=paths),
], [
    dict(title="5 · Let cross-validation choose λ",
         figure_top=kfold,
         items=[
             dict(code="RidgeCV(alphas=np.logspace(-3, 3, 60))", text="tries 60 values of λ, keeps the best."),
             dict(code="LassoCV(cv=5, random_state=0, max_iter=50_000)", text="5-fold CV over its own grid of λ."),
             dict(code="ElasticNetCV(l1_ratio=[.1, .5, .9, 1], cv=5)", text="chooses λ **and** the mix."),
             dict(code=".alpha_  ·  .l1_ratio_  ·  .mse_path_", text="the chosen λ, the chosen mix, the CV error at every λ."),
         ],
         figure=cv_curve),
    dict(title="6 · Score on rows the model never saw",
         items=[
             dict(code="mean_squared_error(yte, pipe.predict(Xte)) ** 0.5", text="RMSE: the typical miss, in the units of y."),
             dict(code="cross_val_score(model, X, y, cv=5, scoring=...)", text="five fits, five scores: their mean is the CV estimate.",
                  ex='-cross_val_score(m, X, y, cv=5, scoring="neg_root_mean_squared_error").mean()'),
             dict(code="KFold(n_splits=5, shuffle=True, random_state=7)", text="the folds themselves, to pass as `cv=`."),
         ],
         warn="Choose λ (or k) by cross-validation on the training rows. Touch the test set **once**."),
    dict(title="7 · Classify: neighbours and a grid (session 8)",
         items=[
             dict(code="KNeighborsClassifier(n_neighbors=5)", text="the class most common among the k closest training rows. `KNeighborsRegressor` averages them."),
             dict(code='GridSearchCV(pipe, {"kneighborsclassifier__n_neighbors": range(1, 26)}, cv=5)',
                  text="tries every k by CV; step name, two underscores, parameter."),
             dict(code=".best_params_  ·  .best_score_", text="the chosen k and its CV accuracy."),
             dict(code="confusion_matrix(y_te, y_hat)  ·  classification_report(...)", text="right and wrong, by class; precision and recall."),
         ],
         figure=confusion),
    dict(title="8 · Also in the course",
         items=[
             dict(code="NearestNeighbors(n_neighbors=1).fit(X)", text="session 10: find each treated unit's closest control, for matching."),
             dict(code="PCA().fit(Z)  ·  .explained_variance_ratio_", text="session 13: components of standardised columns, and the variance each explains."),
         ]),
    dict(title="9 · Read what the penalty kept",
         items=[
             dict(code="pipe[-1].coef_", text="one coefficient per column of X, on the **standardised** scale: compare sizes, not units."),
             dict(code="kept = [c for c, b in zip(XCOLS, coef) if b != 0]", text="the predictors the lasso or elastic net kept.",
                  ex='print(f"lasso kept {len(kept)} of {len(XCOLS)}")'),
         ],
         warn="A zero means \"not needed for prediction here\", never \"no effect\"."),
    dict(title="10 · The whole workflow, in one cell",
         intro="As in sessions 5 and 6: four models, scored on held-out rows.",
         items=[
             dict(code="def test_rmse(model): …", text="fit on 70% inside a pipeline, return (kept, RMSE on 30%).",
                  ex="""pipe = make_pipeline(StandardScaler(), model).fit(Xtr, ytr)
kept = int(np.sum(np.abs(pipe[-1].coef_) > 1e-8))
rmse = mean_squared_error(yte, pipe.predict(Xte)) ** 0.5"""),
             dict(code='results = {"ridge": test_rmse(RidgeCV(...)), …}', text="one entry per model; then a table.",
                  ex='pd.DataFrame(results, index=["kept", "test RMSE"]).T'),
         ]),
    dict(title="11 · When scikit-learn complains",
         items=[
             dict(code="ConvergenceWarning", text="the lasso stopped before settling: raise `max_iter=50_000`."),
             dict(code="ValueError: Input X contains NaN", text="drop or fill missing values first; scikit-learn will not."),
             dict(code="Expected 2D array, got 1D", text="X must be a table: `d[[\"x\"]]` (double brackets), not `d[\"x\"]`."),
         ]),
]]
