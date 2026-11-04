"""
Session 08 · the KNN figures, computed rather than drawn.

Every boundary in these pictures is the one the method actually produces on one
simulated data set, so what a slide says about a figure is true of the figure.
The simulation is the two-class Gaussian mixture of Hastie, Tibshirani &
Friedman (ESL, section 2.3.3), which is also the one behind ISLR's figures: the
two classes overlap, so some blue points sit among the orange and the reverse,
and the true boundary between them is a curve.

    .venv/bin/python 08-knn-and-bias-variance/01-lecture/economist-assets/build_knn_figures.py

Writes, next to this file:
    nearest-neighbours.png   K = 3 at one point, then K = 3 everywhere
    knn-boundary.png         K = 11 against the true boundary
    complexity-compare.png   K = 1 against K = 100, with their error rates
    error-complexity.png     training and test error as 1/K grows
    confusion-matrix.png     the four cells, rows = actual, columns = predicted
    cv-folds.png             5-fold cross-validation, round by round
    cv-curve.png             one validation split against 10-fold cross-validation
    cv-time.png              cross-validation on a time series: the past predicts the next block
    bias-variance.png, underfit.png, overfit.png   near-square, shown side by side
    k-choice.png             K = 1, 11 and 100 side by side
    train-validate-test.png  the three roles a data set plays

scripts/build_economist_assets.R no longer writes these files.
"""

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle
from sklearn.neighbors import KNeighborsClassifier

OUT = Path(__file__).resolve().parent

# The course's figure palette (scripts/build_economist_assets.R)
BG, INK, MUTED, RED = "#F7F4ED", "#222222", "#6B6B67", "#E3120B"
BLUE, ORANGE, PURPLE = "#356B8C", "#E08A1E", "#7B3FA0"
REGION = ListedColormap(["#F6DDBB", "#CFE0EC"])  # pale orange (class 0), pale blue (class 1)

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "font.family": "sans-serif", "font.size": 12, "axes.edgecolor": INK,
    "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
})

# --- the simulation ---------------------------------------------------------
rng = np.random.default_rng(60033)
MEANS_BLUE = rng.multivariate_normal([1, 0], np.eye(2), 10)
MEANS_ORANGE = rng.multivariate_normal([0, 1], np.eye(2), 10)
SD = np.sqrt(1 / 5)


def draw(n_per_class):
    """n points per class: pick one of the class's ten centres, add noise."""
    blue = MEANS_BLUE[rng.integers(0, 10, n_per_class)] + rng.normal(0, SD, (n_per_class, 2))
    orange = MEANS_ORANGE[rng.integers(0, 10, n_per_class)] + rng.normal(0, SD, (n_per_class, 2))
    X = np.vstack([blue, orange])
    y = np.r_[np.ones(n_per_class, int), np.zeros(n_per_class, int)]   # 1 = blue, 0 = orange
    return X, y


def p_blue(X):
    """The true Pr(Y = blue | X = x), known here because we wrote the simulation."""
    def dens(means):
        d2 = ((X[:, None, :] - means[None, :, :]) ** 2).sum(-1)
        return np.exp(-d2 / (2 * SD**2)).mean(1)
    b, o = dens(MEANS_BLUE), dens(MEANS_ORANGE)
    return b / (b + o)


X_train, y_train = draw(100)    # 200 training points, as in ISLR
X_test, y_test = draw(2500)     # 5,000 test points

pad = 0.4
x_lo, x_hi = X_train[:, 0].min() - pad, X_train[:, 0].max() + pad
y_lo, y_hi = X_train[:, 1].min() - pad, X_train[:, 1].max() + pad
gx, gy = np.meshgrid(np.linspace(x_lo, x_hi, 400), np.linspace(y_lo, y_hi, 400))
GRID = np.c_[gx.ravel(), gy.ravel()]
BAYES = p_blue(GRID).reshape(gx.shape)
bayes_error = np.mean((p_blue(X_test) > 0.5).astype(int) != y_test)


def knn(k):
    return KNeighborsClassifier(n_neighbors=k).fit(X_train, y_train)


def headline(fig, title, subtitle=None):
    fig.text(0.02, 0.955, title, fontsize=15, fontweight="bold", color=INK, va="top")
    if subtitle:
        fig.text(0.02, 0.895, subtitle, fontsize=11, color=MUTED, va="top")
    fig.add_artist(plt.Line2D([0.02, 0.075], [0.985, 0.985], color=RED, lw=4,
                              transform=fig.transFigure))


def panel(ax, region=None, bayes=True, boundary=None, points=True, title=None):
    """One map: shaded regions, the true boundary, a method's boundary, the data."""
    if region is not None:
        ax.pcolormesh(gx, gy, region, cmap=REGION, shading="auto", vmin=0, vmax=1)
    if bayes:
        ax.contour(gx, gy, BAYES, levels=[0.5], colors=PURPLE, linestyles="--", linewidths=2)
    if boundary is not None:
        ax.contour(gx, gy, boundary, levels=[0.5], colors=INK, linewidths=1.8)
    if points:
        for cls, col in [(1, BLUE), (0, ORANGE)]:
            m = y_train == cls
            ax.scatter(X_train[m, 0], X_train[m, 1], s=26, facecolor="white",
                       edgecolor=col, linewidth=1.6, zorder=3)
    ax.set_xlim(x_lo, x_hi); ax.set_ylim(y_lo, y_hi)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("$X_1$"); ax.set_ylabel("$X_2$", rotation=0, labelpad=12)
    if title:
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=INK)


def legend(fig, extra=()):
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker="o", ls="", mfc="white", mec=BLUE, mew=1.6, label="blue class"),
               Line2D([], [], marker="o", ls="", mfc="white", mec=ORANGE, mew=1.6, label="orange class"),
               Line2D([], [], color=PURPLE, ls="--", lw=2, label="true boundary (known: we simulated the data)"),
               *extra]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False, fontsize=11)


def save(fig, name):
    fig.savefig(OUT / name, dpi=144)
    plt.close(fig)
    print("wrote", name)


# 2 · K = 3 at one point, then everywhere -------------------------------------
# A small, readable training set of 12 points, and a test point (the cross).
small_X = np.array([[-1.6, 1.3], [-0.6, 1.6], [0.5, 1.5], [1.6, 1.1], [-1.9, -0.2],
                    [-0.5, 0.45], [0.55, 0.25], [1.5, -0.4], [-1.3, -1.4], [-0.1, -0.75],
                    [0.9, -1.5], [1.9, 0.6]])
small_y = np.array([0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0])     # 1 = blue, 0 = orange
x0 = np.array([0.0, 0.0])
d = np.sqrt(((small_X - x0) ** 2).sum(1))
nn = np.argsort(d)[:3]
radius = d[nn].max() + 0.12
share_blue = small_y[nn].mean()

sx, sy = np.meshgrid(np.linspace(-2.5, 2.5, 300), np.linspace(-2.2, 2.2, 300))
small_fit = KNeighborsClassifier(n_neighbors=3).fit(small_X, small_y)
small_region = small_fit.predict(np.c_[sx.ravel(), sy.ravel()]).reshape(sx.shape)

fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
fig.subplots_adjust(top=0.78, bottom=0.04, left=0.04, right=0.98, wspace=0.08)
for i, ax in enumerate(axes):
    if i == 1:
        ax.pcolormesh(sx, sy, small_region, cmap=REGION, shading="auto", vmin=0, vmax=1)
        ax.contour(sx, sy, small_region, levels=[0.5], colors=INK, linewidths=1.8)
        ax.scatter(*x0, marker="x", s=140, color=INK, linewidth=3, zorder=4)
    for cls, col in [(1, BLUE), (0, ORANGE)]:
        m = small_y == cls
        ax.scatter(small_X[m, 0], small_X[m, 1], s=110, facecolor="white",
                   edgecolor=col, linewidth=2.4, zorder=3)
    if i == 0:
        ax.add_patch(Circle(x0, radius, fill=False, color="#2A8C82", lw=2.2))
        for j in nn:
            ax.plot([0, small_X[j, 0]], [0, small_X[j, 1]], color=MUTED, lw=1, zorder=2)
        ax.scatter(*x0, marker="x", s=140, color=INK, linewidth=3, zorder=4)
        ax.set_title(f"Left: the 3 nearest to the cross are {int(3 * share_blue)} blue, "
                     f"{3 - int(3 * share_blue)} orange\n→ Pr(blue) = {int(3 * share_blue)}/3, predict blue",
                     loc="left", fontsize=12, color=INK)
    else:
        ax.set_title("Right: the same vote at every point of the plane\n→ the K = 3 decision boundary",
                     loc="left", fontsize=12, color=INK)
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.2, 2.2); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
headline(fig, "KNN with K = 3: a point takes the majority class of its three nearest neighbours")
save(fig, "nearest-neighbours.png")


# 3 · K = 11 against the true boundary (odd, so the vote cannot tie) ----------------------------------------------------
def prob_map(k):
    """1 where KNN predicts blue, 0 where orange. Taken from the predicted class,
    not the probability: with an even K a 5-5 tie is exactly 0.5, and a contour
    at 0.5 would trace the tie as a stray line."""
    return knn(k).predict(GRID).reshape(gx.shape).astype(float)


def errors(k):
    m = knn(k)
    return 1 - m.score(X_train, y_train), 1 - m.score(X_test, y_test)


from matplotlib.lines import Line2D  # noqa: E402

p10 = prob_map(11)
tr10, te10 = errors(11)
fig, ax = plt.subplots(figsize=(10, 5.9))
fig.subplots_adjust(top=0.84, bottom=0.14, left=0.06, right=0.98)
panel(ax, region=(p10 > 0.5).astype(float), boundary=p10)
headline(fig, "KNN with K = 11 lands close to the true boundary",
         f"Solid black = KNN boundary, dashed purple = the truth. "
         f"Test error: KNN {te10:.1%}; the best any rule can do here: {bayes_error:.1%}.")
legend(fig, [Line2D([], [], color=INK, lw=1.8, label="KNN boundary, K = 11")])
save(fig, "knn-boundary.png")

# 4 · K = 1 against K = 100 ---------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 6.4))
fig.subplots_adjust(top=0.72, bottom=0.14, left=0.04, right=0.99, wspace=0.10)
for ax, k, label in [(axes[0], 1, "too flexible"), (axes[1], 100, "too rigid")]:
    pk = prob_map(k)
    tr, te = errors(k)
    panel(ax, region=(pk > 0.5).astype(float), boundary=pk,
          title=f"K = {k}: {label}\ntraining error {tr:.0%} · test error {te:.0%}")
headline(fig, "K = 1 chases every point; K = 100 ignores the curve",
         f"The same 200 points. Low K: low bias, high variance. High K: high bias, low variance.\n"
         f"For comparison, the best any rule can do on these data is {bayes_error:.0%} error: the classes overlap.")
legend(fig, [Line2D([], [], color=INK, lw=1.8, label="KNN boundary")])
save(fig, "complexity-compare.png")

# 5 · Training and test error against 1/K -------------------------------------
ks = np.array([1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 50, 75, 100, 150])
tr_err, te_err = np.array([errors(k) for k in ks]).T
fig, ax = plt.subplots(figsize=(10, 5.6))
fig.subplots_adjust(top=0.84, bottom=0.13, left=0.08, right=0.97)
ax.plot(1 / ks, tr_err, "o-", color=BLUE, lw=2.2, label="training error (200 obs.)")
ax.plot(1 / ks, te_err, "o-", color=ORANGE, lw=2.2, label="test error (5,000 obs.)")
ax.axhline(bayes_error, color=INK, ls="--", lw=1.4, label="lowest possible error (the classes overlap)")
best = ks[np.argmin(te_err)]
ax.axvline(1 / best, color=MUTED, ls=":", lw=1.2)
ax.annotate(f"lowest test error\nat K = {best}", (1 / best, te_err.min()), xytext=(12, 30),
            textcoords="offset points", fontsize=11, color=MUTED,
            arrowprops=dict(arrowstyle="-", color=MUTED))
ax.set_xscale("log")
ax.set_xticks(1 / np.array([100, 30, 10, 3, 1]))
ax.set_xticklabels(["1/100", "1/30", "1/10", "1/3", "1"])
ax.set_xlabel("flexibility, 1/K  (left: K large, rigid · right: K = 1, flexible)")
ax.set_ylabel("error rate")
ax.set_ylim(-0.01, max(te_err.max(), tr_err.max()) + 0.05)
ax.legend(frameon=False, loc="upper left")
headline(fig, "Training error falls to zero; test error is U-shaped",
         "KNN on the simulated data, K from 150 down to 1.")
save(fig, "error-complexity.png")

# 6 · Confusion matrix --------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.4, 6))
fig.subplots_adjust(top=0.86, bottom=0.04, left=0.04, right=0.98)
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
cells = {  # (x, y): (label, good?)  rows = actual, columns = predicted
    (30, 45): ("TRUE POSITIVE\nTP", True), (60, 45): ("FALSE NEGATIVE\nFN", False),
    (30, 10): ("FALSE POSITIVE\nFP", False), (60, 10): ("TRUE NEGATIVE\nTN", True),
}
for (x, y), (lab, good) in cells.items():
    ax.add_patch(plt.Rectangle((x, y), 30, 35, color="#C6E2DE" if good else "#F7C9C6", ec=INK))
    ax.text(x + 15, y + 17.5, lab, ha="center", va="center", fontweight="bold",
            color="#2A8C82" if good else RED, fontsize=12)
ax.text(60, 92, "PREDICTED", ha="center", fontweight="bold")
ax.text(45, 83, "positive", ha="center"); ax.text(75, 83, "negative", ha="center")
ax.text(8, 45, "ACTUAL", rotation=90, va="center", fontweight="bold")
ax.text(26, 62.5, "positive", ha="right", va="center"); ax.text(26, 27.5, "negative", ha="right", va="center")
headline(fig, "A confusion matrix: rows are the truth, columns the prediction")
save(fig, "confusion-matrix.png")

print(f"lowest possible error {bayes_error:.3f}; K=11 test error {te10:.3f}")


# 7 · How 5-fold cross-validation works ---------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 4.9))
fig.subplots_adjust(top=0.84, bottom=0.02, left=0.02, right=0.98)
ax.set_xlim(0, 106); ax.set_ylim(5, 62); ax.axis("off")
x0_, w = 14, 13.2                      # left edge and width of one fold
for r in range(5):                     # round r: fold r is held out
    y = 50 - r * 10.5
    ax.text(x0_ - 1.5, y + 3.5, f"round {r + 1}", ha="right", va="center", fontsize=12, color=INK)
    for f in range(5):
        held = f == r
        ax.add_patch(plt.Rectangle((x0_ + f * w, y), w - 0.6, 7,
                                   color=ORANGE if held else "#CFE0EC", ec=INK, lw=0.8))
        ax.text(x0_ + f * w + (w - 0.6) / 2, y + 3.5, "validate" if held else "train",
                ha="center", va="center", fontsize=11,
                color="white" if held else BLUE, fontweight="bold" if held else None)
    ax.annotate("", (85, y + 3.5), (x0_ + 5 * w + 0.5, y + 3.5),
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(86, y + 3.5, f"error$_{r + 1}$", va="center", fontsize=13, color=INK)
ax.plot([92.5, 93.5, 93.5, 92.5], [57, 57, 6, 6], color=RED, lw=1.5)
ax.text(99.5, 31.5, "average\nof the 5\n= CV error", ha="center", va="center", fontsize=12,
        fontweight="bold", color=RED)
ax.text(x0_ + 2.5 * w, 59.5, "the training data, cut into 5 folds", ha="center",
        fontsize=12, color=MUTED)
headline(fig, "5-fold cross-validation: every observation is held out exactly once",
         "Fit on four folds, measure the error on the fifth, rotate, and average the five errors.")
save(fig, "cv-folds.png")

# 8 · One validation split is noisy; cross-validation is not ------------------
from sklearn.model_selection import cross_val_score, train_test_split  # noqa: E402

ks_cv = np.array([1, 3, 5, 7, 9, 13, 17, 21, 29, 39, 51, 71])
true_test = np.array([errors(k)[1] for k in ks_cv])
fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), sharey=True)
fig.subplots_adjust(top=0.74, bottom=0.14, left=0.07, right=0.99, wspace=0.06)
for seed in range(10):                 # ten different random 50/50 validation splits
    Xa_, Xb_, ya_, yb_ = train_test_split(X_train, y_train, test_size=0.5, random_state=seed)
    err = [1 - KNeighborsClassifier(n_neighbors=min(k, len(Xa_))).fit(Xa_, ya_).score(Xb_, yb_)
           for k in ks_cv]
    axes[0].plot(1 / ks_cv, err, color=MUTED, lw=1.1, alpha=0.8)
for seed in range(10):                 # ten different random 10-fold cross-validations
    from sklearn.model_selection import KFold  # noqa: E402
    folds_ = KFold(10, shuffle=True, random_state=seed)
    err = [1 - cross_val_score(KNeighborsClassifier(n_neighbors=k), X_train, y_train,
                               cv=folds_).mean() for k in ks_cv]
    axes[1].plot(1 / ks_cv, err, color=BLUE, lw=1.1, alpha=0.8)
for ax, t in [(axes[0], "One validation set (half the data), 10 random splits:\n"
                        "the curves disagree on which K is best"),
              (axes[1], "10-fold cross-validation, 10 random shuffles:\n"
                        "the curves agree with each other, and stay close to the truth")]:
    ax.plot(1 / ks_cv, true_test, color=ORANGE, lw=3, label="true test error (5,000 new points)")
    ax.set_xscale("log")
    ax.set_xticks(1 / np.array([70, 30, 10, 3, 1]))
    ax.set_xticklabels(["1/70", "1/30", "1/10", "1/3", "1"])
    ax.set_xlabel("flexibility, 1/K")
    ax.set_title(t, loc="left", fontsize=12, color=INK)
axes[0].set_ylabel("error rate")
axes[1].legend(frameon=False, loc="upper left", fontsize=11)
headline(fig, "Why cross-validation: the same 200 points, two ways to estimate test error",
         "Grey/blue: estimates from the training data alone. Orange: the truth, known only because we simulated it.")
save(fig, "cv-curve.png")


# 9 · Cross-validation on a time series ---------------------------------------
# What the finance example does: the folds respect time. Each round fits on
# everything up to a date and validates on the block that comes right after.
fig, ax = plt.subplots(figsize=(11.5, 5.2))
fig.subplots_adjust(top=0.82, bottom=0.02, left=0.02, right=0.98)
ax.set_xlim(0, 106); ax.set_ylim(0, 66); ax.axis("off")
x0_, w = 16, 11.0                      # six blocks of training data, then the test year
for r in range(5):                     # round r: fit on blocks 0..r, validate on block r+1
    y = 50 - r * 10
    ax.text(x0_ - 1.5, y + 3.5, f"round {r + 1}", ha="right", va="center", fontsize=12, color=INK)
    for f in range(6):
        if f <= r:
            col, lab, tc = "#CFE0EC", "fit", BLUE
        elif f == r + 1:
            col, lab, tc = ORANGE, "validate", "white"
        else:
            col, lab, tc = "white", "not yet", "#B5B2AA"
        ax.add_patch(plt.Rectangle((x0_ + f * w, y), w - 0.6, 7, color=col, ec=INK, lw=0.8))
        ax.text(x0_ + f * w + (w - 0.6) / 2, y + 3.5, lab, ha="center", va="center",
                fontsize=10.5, color=tc, fontweight="bold" if lab == "validate" else None)
    ax.add_patch(plt.Rectangle((x0_ + 6 * w + 2, y), 14, 7, color="#E4E1D9", ec=INK, lw=0.8))
    ax.text(x0_ + 6 * w + 9, y + 3.5, "locked", ha="center", va="center", fontsize=10.5, color=MUTED)
ax.annotate("", (x0_ + 6 * w - 0.6, 61), (x0_, 61), arrowprops=dict(arrowstyle="->", color=MUTED))
ax.text(x0_ + 3 * w, 63, "training years, 2001 → 2004, cut into 6 blocks in time order",
        ha="center", fontsize=11.5, color=MUTED)
ax.text(x0_ + 6 * w + 9, 63, "test: 2005", ha="center", fontsize=11.5, color=MUTED)
ax.text(x0_ + 6 * w + 9, 2.5, "opened once,\nat the very end", ha="center", fontsize=11,
        color=RED, fontweight="bold")
headline(fig, "Cross-validation on a time series: the past predicts the block that comes next",
         "Never fit on the future to predict the past. The test year stays locked until K is chosen.")
save(fig, "cv-time.png")


warnings.simplefilter("ignore", np.exceptions.RankWarning if hasattr(np, 'exceptions') else Warning)

# 10 · Bias and variance, three near-square panels shown side by side --------
# (moved here from scripts/build_economist_assets.R, so the three share a shape)
GOLD, PALE_BLUE = "#D49A00", "#C9DCE8"


def square(name, title, subtitle, draw_fn):
    fig, ax = plt.subplots(figsize=(6, 6.3))
    fig.subplots_adjust(top=0.80, bottom=0.15, left=0.13, right=0.96)
    draw_fn(ax)
    headline(fig, title, subtitle)
    save(fig, name)


def draw_bias_variance(ax):
    c = np.linspace(0.03, 1, 300)
    bias2 = 1.05 * np.exp(-3.2 * c) + 0.05
    variance = 0.08 + 0.82 * c**2
    total = bias2 + variance + 0.13
    ax.plot(c, bias2, color=BLUE, lw=2.5)
    ax.plot(c, variance, color=RED, lw=2.5)
    ax.plot(c, total, color=INK, lw=3)
    b = np.argmin(total)
    ax.axvline(c[b], color=GOLD, ls="--", lw=2)
    ax.text(0.10, bias2[20] + 0.06, "bias²", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(0.80, variance[240] - 0.16, "variance", color=RED, fontsize=13, fontweight="bold")
    ax.text(0.52, 1.12, "total error", color=INK, fontsize=13, fontweight="bold")
    ax.text(c[b] + 0.03, 0.04, "lowest\ntotal error", color=GOLD, fontsize=12, fontweight="bold")
    ax.set_ylim(0, 1.25)
    ax.set_xticks([0.05, 0.5, 0.95]); ax.set_xticklabels(["simple", "balanced", "very\nflexible"])
    ax.set_xlabel("model flexibility"); ax.set_ylabel("expected test error")


rng_bv = np.random.default_rng(72)
xs = np.sort(rng_bv.uniform(-3, 3, 14))      # few points, so a flexible fit can chase each one
truth = np.sin(xs) + 0.15 * xs
ys = truth + rng_bv.normal(0, 0.25, 14)
gridx = np.linspace(xs.min(), xs.max(), 500)


def draw_fit(degree, label):
    def fn(ax):
        ax.scatter(xs, ys, s=40, facecolor=PALE_BLUE, edgecolor=BLUE, zorder=3)
        coef = np.polyfit(xs, ys, degree)            # may warn: the fit is deliberately extreme
        ax.plot(gridx, np.polyval(coef, gridx), color=RED, lw=2.6, label=label)
        ax.plot(gridx, np.sin(gridx) + 0.15 * gridx, color=INK, lw=2, ls="--", label="true signal")
        ax.set_ylim(-2.3, 2.6)
        ax.set_xlabel("x"); ax.set_ylabel("y", rotation=0, labelpad=10)
        ax.legend(frameon=False, loc="upper left", fontsize=11)
    return fn


square("bias-variance.png", "Balance bias against variance",
       "Too simple: high bias. Too flexible: high variance.\nThe best model sits in between.",
       draw_bias_variance)
square("underfit.png", "Underfitting: too simple",
       "A straight line misses the curve that is\nreally there. High bias, low variance.",
       draw_fit(1, "straight-line fit"))
square("overfit.png", "Overfitting: follows the noise",
       "A degree-12 polynomial bends to every point,\nnoise included. Low bias, high variance.",
       draw_fit(12, "degree-12 fit"))


# 11 · K = 1, K = 11, K = 100 in one row: the choice-of-K slide, without tabs ----
fig, axes = plt.subplots(1, 3, figsize=(15, 6.0))
fig.subplots_adjust(top=0.76, bottom=0.13, left=0.03, right=0.99, wspace=0.08)
for ax, k, label in [(axes[0], 1, "too flexible"), (axes[1], 11, "about right"),
                     (axes[2], 100, "too rigid")]:
    pk = prob_map(k)
    tr, te = errors(k)
    panel(ax, region=(pk > 0.5).astype(float), boundary=pk,
          title=f"K = {k}: {label}\ntraining error {tr:.0%} · test error {te:.0%}")
headline(fig, "K = 1 chases every point, K = 100 ignores the curve, K = 11 follows it",
         f"The same 200 points, three values of K. The best any rule can do on these data is "
         f"{bayes_error:.0%} error: the classes overlap.")
legend(fig, [Line2D([], [], color=INK, lw=1.8, label="KNN boundary")])
save(fig, "k-choice.png")


# 12 · Train, validate, test: three roles for one data set ---------------------
fig, ax = plt.subplots(figsize=(12, 3.9))
fig.subplots_adjust(top=0.78, bottom=0.02, left=0.02, right=0.98)
ax.set_xlim(0, 100); ax.set_ylim(18, 38); ax.axis("off")
# the whole data set, one bar
ax.add_patch(plt.Rectangle((2, 20), 60, 10, color="#CFE0EC", ec=INK, lw=1))
ax.add_patch(plt.Rectangle((62, 20), 16, 10, color=ORANGE, ec=INK, lw=1))
ax.add_patch(plt.Rectangle((78, 20), 20, 10, color="#E4E1D9", ec=INK, lw=1))
ax.text(32, 25, "TRAIN\nthe model learns from it", ha="center", va="center", fontsize=12.5,
        color=BLUE, fontweight="bold")
ax.text(70, 25, "VALIDATE\nchoose K", ha="center", va="center", fontsize=12.5,
        color="white", fontweight="bold")
ax.text(88, 25, "TEST\njudge, once", ha="center", va="center", fontsize=12.5,
        color=INK, fontweight="bold")
# brace over train + validate: the training data, which cross-validation re-cuts
ax.plot([2, 2, 78, 78], [32, 34, 34, 32], color=BLUE, lw=1.5)
ax.text(40, 35.5, "the training data: cross-validation rotates which part plays \"validate\"",
        ha="center", fontsize=11.5, color=BLUE)
ax.plot([78, 78, 98, 98], [32, 34, 34, 32], color=MUTED, lw=1.5)
ax.text(88, 35.5, "locked until the end", ha="center", fontsize=11.5, color=MUTED)
headline(fig, "Train, validate, test: one data set, three jobs",
         "Each observation has one job at a time. The test set never helps to choose anything.")
save(fig, "train-validate-test.png")
