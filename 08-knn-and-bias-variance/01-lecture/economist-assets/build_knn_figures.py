"""
Session 08 · the KNN figures, computed rather than drawn.

Every boundary in these pictures is the one the method actually produces on one
simulated data set, so what a slide says about a figure is true of the figure.
The simulation is the two-class Gaussian mixture of Hastie, Tibshirani &
Friedman (ESL, section 2.3.3), which is also the one behind ISLR's figures: the
two classes overlap, so some blue points sit among the orange and the reverse,
and the true (Bayes) boundary is a curve.

    .venv/bin/python 08-knn-and-bias-variance/01-lecture/economist-assets/build_knn_figures.py

Writes, next to this file:
    bayes-classifier.png     the Bayes boundary and the regions it defines
    nearest-neighbours.png   K = 3 at one point, then K = 3 everywhere
    knn-boundary.png         K = 11 against the Bayes boundary
    complexity-compare.png   K = 1 against K = 100, with their error rates
    error-complexity.png     training and test error as 1/K grows
    confusion-matrix.png     the four cells, rows = actual, columns = predicted

scripts/build_economist_assets.R no longer writes these files.
"""

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
    """One map: shaded regions, the Bayes line, a method's boundary, the data."""
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
               Line2D([], [], color=PURPLE, ls="--", lw=2, label="Bayes boundary (the truth)"),
               *extra]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False, fontsize=11)


def save(fig, name):
    fig.savefig(OUT / name, dpi=144)
    plt.close(fig)
    print("wrote", name)


# 1 · The Bayes classifier ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.9))
fig.subplots_adjust(top=0.80, bottom=0.14, left=0.06, right=0.98)
panel(ax, region=(BAYES > 0.5).astype(float))
headline(fig, "The Bayes classifier: each point goes to its most likely class",
         f"200 simulated observations. Shading = the class the Bayes rule assigns.\n"
         f"Even this rule errs on {bayes_error:.0%} of new points, because the classes overlap.")
legend(fig)
save(fig, "bayes-classifier.png")

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


# 3 · K = 11 against Bayes (odd, so the vote cannot tie) ----------------------------------------------------
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
headline(fig, "KNN with K = 11 lands close to the Bayes boundary",
         f"Solid black = KNN boundary, dashed purple = Bayes. "
         f"Test error: KNN {te10:.1%}, Bayes {bayes_error:.1%}.")
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
         f"For comparison, the Bayes error rate is {bayes_error:.0%}.")
legend(fig, [Line2D([], [], color=INK, lw=1.8, label="KNN boundary")])
save(fig, "complexity-compare.png")

# 5 · Training and test error against 1/K -------------------------------------
ks = np.array([1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 50, 75, 100, 150])
tr_err, te_err = np.array([errors(k) for k in ks]).T
fig, ax = plt.subplots(figsize=(10, 5.6))
fig.subplots_adjust(top=0.84, bottom=0.13, left=0.08, right=0.97)
ax.plot(1 / ks, tr_err, "o-", color=BLUE, lw=2.2, label="training error (200 obs.)")
ax.plot(1 / ks, te_err, "o-", color=ORANGE, lw=2.2, label="test error (5,000 obs.)")
ax.axhline(bayes_error, color=INK, ls="--", lw=1.4, label="Bayes error rate")
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

print(f"Bayes error {bayes_error:.3f}; K=11 test error {te10:.3f}")
