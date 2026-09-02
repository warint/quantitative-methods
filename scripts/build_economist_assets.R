# Rebuilds third-party teaching figures as original, course-owned PNG graphics.
# The visual language is inspired by restrained economic-journalism graphics:
# warm paper, charcoal type, one red accent, direct labels, and minimal grids.

BG <- "#F7F4ED"
INK <- "#222222"
MUTED <- "#6B6B67"
RED <- "#E3120B"
BLUE <- "#356B8C"
TEAL <- "#2A8C82"
GOLD <- "#D49A00"
GRID <- "#D8D3C8"
PALE_RED <- "#F7C9C6"
PALE_BLUE <- "#C9DCE8"
PALE_TEAL <- "#C6E2DE"

# The session codes below are the ones this script has always used; the
# directories are the current ones. Seven of these eight paths still named
# folders from an earlier syllabus — 03-inference-diagnostics-interpretation,
# 07-trees-forests-boosting and so on — so re-running the script created
# orphans and left the assets the decks actually load untouched. Each path here
# is the directory that references the files that code generates; verified by
# grepping the decks for every filename.
paths <- c(
  S02 = "02-exploratory-data-analysis/01-lecture/economist-assets",
  S03 = "03-regression-adequacy-and-validity/01-lecture/economist-assets",
  S04 = "04-logistic-ordinal-multinomial/01-lecture/economist-assets",
  S07 = "07-pca-and-factor-analysis/01-lecture/economist-assets",
  S08 = "08-knn-and-bias-variance/01-lecture/economist-assets",
  S09 = "09-structural-equation-modelling/01-lecture/economist-assets",
  S10 = "10-causal-inference-foundations/01-lecture/economist-assets",
  S11 = "11-causal-inference-did/01-lecture/economist-assets"
)
invisible(lapply(paths, dir.create, recursive = TRUE, showWarnings = FALSE))

generated_assets <- character()

asset <- function(session, filename) {
  filename <- sub("\\.svg$", ".png", filename)
  path <- file.path(paths[[session]], filename)
  generated_assets <<- c(generated_assets, path)
  path
}

open_svg <- function(path, width = 10, height = 5.625) {
  # Prefer Quartz on macOS (it avoids an external X11 dependency) and Cairo on
  # headless Linux runners such as GitHub Actions.
  device_type <- if (capabilities("aqua")) "quartz" else "cairo"
  png(path, width = round(width * 144), height = round(height * 144),
      res = 144, bg = BG, pointsize = 13, family = "sans", type = device_type)
  par(bg = BG, fg = INK, col.axis = INK, col.lab = INK, col.main = INK,
      las = 1, bty = "n", mar = c(3.4, 4.1, 3.6, 1.2),
      mgp = c(2.15, 0.65, 0), tcl = -0.22)
}

headline <- function(title, subtitle = NULL) {
  mtext(title, side = 3, adj = 0, line = 1.55, font = 2, cex = 1.05, col = INK)
  segments(par("usr")[1], par("usr")[4] + 0.025 * diff(par("usr")[3:4]),
           par("usr")[1] + 0.07 * diff(par("usr")[1:2]),
           par("usr")[4] + 0.025 * diff(par("usr")[3:4]), col = RED, lwd = 4,
           xpd = NA)
  if (!is.null(subtitle))
    mtext(subtitle, side = 3, adj = 0, line = 0.25, cex = 0.68, col = MUTED)
}

direct_label <- function(x, y, label, col = INK, pos = 4, ...) {
  text(x, y, label, col = col, pos = pos, font = 2, cex = 0.72, ...)
}

box <- function(x, y, w, h, label, fill = "white", border = GRID,
                col = INK, cex = 0.72, font = 2, radius = 0) {
  rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2,
       col = fill, border = border, lwd = 1.5)
  text(x, y, label, col = col, cex = cex, font = font)
}

node_circle <- function(x, y, r, label, fill = PALE_BLUE, border = BLUE,
                        col = INK, cex = 0.72) {
  symbols(x, y, circles = r, inches = FALSE, add = TRUE, bg = fill,
          fg = border, lwd = 1.6)
  text(x, y, label, col = col, cex = cex, font = 2)
}

link <- function(x0, y0, x1, y1, col = MUTED, lwd = 1.7, label = NULL) {
  arrows(x0, y0, x1, y1, length = 0.08, angle = 22, col = col, lwd = lwd)
  if (!is.null(label)) text((x0 + x1) / 2, (y0 + y1) / 2 + 2.2,
                            label, col = col, cex = 0.64, font = 2)
}

# Session 02 -----------------------------------------------------------------

open_svg(asset("S02", "percentile.svg"))
x <- seq(-3.6, 3.6, length.out = 500); y <- dnorm(x)
plot(x, y, type = "n", axes = FALSE, xlab = "Observed value", ylab = "Density",
     ylim = c(0, max(y) * 1.08)); abline(h = 0, col = INK)
# The cut sits at one standard deviation above the mean, so the figure shows
# the same number the slide's code computes -- pnorm(1) = 0.8413 -- and the same
# number the 68-95-99.7 rule implies two slides later: 68% within 1 SD leaves
# 16% in the upper tail, so 84% below. An arbitrary cut taught none of that.
cut <- 1; xs <- x[x <= cut]
polygon(c(xs, rev(xs)), c(dnorm(xs), rep(0, length(xs))), col = PALE_RED, border = NA)
lines(x, y, col = INK, lwd = 2.4); abline(v = cut, col = RED, lwd = 2)
axis(1, at = c(-2, 0, cut, 2.4), labels = c("low", "mean", "mean + 1 SD", "high"), col = NA)
text(cut, dnorm(cut) + .035, "84th percentile", col = RED, pos = 4, font = 2)
text(-1.4, .12, "84% of observations", col = INK, font = 2)
headline("A percentile turns a value into a position")
dev.off()

open_svg(asset("S02", "mean-median.svg"))
x <- seq(0.02, 8, length.out = 700); y <- dlnorm(x, meanlog = .55, sdlog = .55)
plot(x, y, type = "n", axes = FALSE, xlab = "Value", ylab = "Density",
     ylim = c(0, max(y) * 1.12)); abline(h = 0, col = INK)
polygon(c(x, rev(x)), c(y, rep(0, length(x))), col = PALE_BLUE, border = NA)
lines(x, y, col = BLUE, lwd = 2.6)
med <- exp(.55); mn <- exp(.55 + .55^2 / 2)
abline(v = med, col = INK, lwd = 2); abline(v = mn, col = RED, lwd = 2)
direct_label(med, max(y) * .73, "median", col = INK, pos = 2)
direct_label(mn, max(y) * .48, "mean", col = RED, pos = 4)
text(5.4, max(y) * .22, "A long right tail pulls\nthe mean farther right", adj = 0,
     cex = .78, col = MUTED)
headline("Skewness separates the mean from the median")
dev.off()

open_svg(asset("S02", "shape.svg"), width = 11, height = 5.6)
par(mfrow = c(1, 2), mar = c(3.1, 3.2, 3.7, .8))
x <- seq(-4, 4, length.out = 500)
plot(x, dnorm(x), type = "n", axes = FALSE, xlab = "", ylab = "Density",
     ylim = c(0, .55)); abline(h = 0, col = INK)
lines(x, dnorm(x), col = INK, lwd = 2)
right <- dlnorm(x + 4.1, 1, .48); right <- right / max(right) * .43
left <- rev(right)
lines(x, right, col = RED, lwd = 2.2); lines(x, left, col = BLUE, lwd = 2.2)
# Each label beside its own curve. They sat on the opposite side of the panel
# from the curve they name — colour-matched, but reading as swapped.
direct_label(-2.15, .30, "right-skewed", RED, 2)
direct_label(2.15, .30, "left-skewed", BLUE, 4)
title("Skewness: which tail is longer?", adj = 0, line = 1.3, font.main = 2)
plot(x, dnorm(x), type = "n", axes = FALSE, xlab = "", ylab = "Density",
     ylim = c(0, .65)); abline(h = 0, col = INK)
# All three curves have variance 1, so the only thing differing is shape. This
# matters: "lighter tails" used to be dnorm(sd = 1.35), which has *identical*
# kurtosis to the standard normal — kurtosis is scale-invariant — and visibly
# more mass in the tails, so the picture claimed the opposite of what it showed.
#   heavy: t(5) scaled to unit variance, excess kurtosis +5.3
#   light: Beta(2,2) mapped to unit variance, excess kurtosis -0.86, and
#          compactly supported, so its tails visibly stop rather than thin out.
s_t <- sqrt(3 / 5); a_b <- sqrt(5)
normal <- dnorm(x)
heavy  <- dt(x / s_t, df = 5) / s_t
light  <- ifelse(abs(x) < a_b, dbeta((x + a_b) / (2 * a_b), 2, 2) / (2 * a_b), NA)
lines(x, normal, col = INK, lwd = 2); lines(x, heavy, col = RED, lwd = 2.2)
lines(x, light, col = BLUE, lwd = 2.2)
direct_label(.35, .53, "heavier tails", RED, 4)
direct_label(-2.05, .105, "lighter tails", BLUE, 2)
title("Kurtosis: how much mass reaches the tails?", adj = 0, line = 1.3, font.main = 2)
dev.off()

# Session 03: diagnostics -----------------------------------------------------

open_svg(asset("S03", "regression-table.svg"), width = 11, height = 5.9)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("A regression table is a compact set of comparisons")
cols <- c(4, 48, 65, 82, 97); rows <- seq(78, 20, length.out = 7)
rect(3, 80, 97, 88, col = INK, border = NA)
headers <- c("Predictor", "Model 1", "Model 2", "Model 3")
for (i in seq_along(headers)) text((cols[i] + cols[i + 1]) / 2, 84, headers[i], col = "white", font = 2, cex = .74)
labels <- c("Age at entry", "Knowledge intensity", "Similarity", "Legal protection", "Firm age", "International sales")
values <- rbind(c("−0.20**", "−0.37***", "−0.15*"), c("0.29**", "0.19**", "0.29**"),
                c("0.17*", "0.09*", "0.08*"), c("0.01", "−0.12", "0.08"),
                c("0.11", "0.02", "0.04"), c("0.69***", "0.56***", "0.60***"))
for (r in seq_along(labels)) {
  if (r %% 2 == 0) rect(3, rows[r] - 3.8, 97, rows[r] + 3.8, col = "#ECE8DE", border = NA)
  text(5, rows[r], labels[r], adj = 0, cex = .72, col = INK)
  for (j in 1:3) text((cols[j + 1] + cols[j + 2]) / 2, rows[r], values[r, j],
                       cex = .72, col = if (grepl("\\*", values[r, j])) RED else INK, font = 2)
}
segments(3, 14, 97, 14, col = RED, lwd = 3); text(3, 9, "Stars show statistical evidence; columns show specification sensitivity.", adj = 0, cex = .68, col = MUTED)
dev.off()

set.seed(12)
open_svg(asset("S03", "r-squared.svg"))
x <- seq(0.4, 9.6, length.out = 38); y <- 1.1 + .72 * x + rnorm(length(x), 0, 1.0)
fit <- lm(y ~ x); yh <- fitted(fit); idx <- 29
plot(x, y, pch = 16, col = adjustcolor(BLUE, .7), xlab = "Predictor", ylab = "Outcome", axes = FALSE)
axis(1); axis(2); abline(fit, col = INK, lwd = 2.4); abline(h = mean(y), col = MUTED, lty = 2)
segments(x[idx], mean(y), x[idx], yh[idx], col = TEAL, lwd = 4)
segments(x[idx], yh[idx], x[idx], y[idx], col = RED, lwd = 4)
direct_label(x[idx], (mean(y) + yh[idx]) / 2, "explained", TEAL, 4)
direct_label(x[idx], (yh[idx] + y[idx]) / 2, "residual", RED, 4)
headline("R² compares explained variation with what remains")
dev.off()

set.seed(22)
open_svg(asset("S03", "nonlinearity.svg"), width = 10.5, height = 6)
par(mfrow = c(2, 1), mar = c(2.5, 4, 2.4, 1))
x <- seq(0, 10, length.out = 90); y <- 1 + .72 * x - .06 * x^2 + rnorm(90, 0, .48); fit <- lm(y ~ x)
plot(x, y, pch = 16, col = adjustcolor(BLUE, .65), axes = FALSE, xlab = "", ylab = "Outcome")
axis(2); abline(fit, col = RED, lwd = 2.2); lines(x, 1 + .72 * x - .06 * x^2, col = INK, lwd = 2.4)
legend("topleft", c("linear fit", "underlying curve"), col = c(RED, INK), lwd = 2, bty = "n", horiz = TRUE)
title("A straight line misses systematic curvature", adj = 0, font.main = 2)
plot(x, resid(fit), pch = 16, col = adjustcolor(BLUE, .7), axes = FALSE, xlab = "Predictor", ylab = "Residual")
axis(1); axis(2); abline(h = 0, col = INK); lines(lowess(x, resid(fit), f = .45), col = RED, lwd = 2.4)
dev.off()

set.seed(33)
open_svg(asset("S03", "heteroskedasticity.svg"), width = 10.5, height = 6)
par(mfrow = c(2, 1), mar = c(2.5, 4, 2.4, 1))
x <- seq(0.2, 10, length.out = 110); y <- 1 + .55 * x + rnorm(110, 0, .18 + .12 * x); fit <- lm(y ~ x)
plot(x, y, pch = 16, col = adjustcolor(BLUE, .65), axes = FALSE, xlab = "", ylab = "Outcome")
axis(2); abline(fit, col = INK, lwd = 2.4); title("Uncertainty grows with the fitted value", adj = 0, font.main = 2)
plot(fitted(fit), resid(fit), pch = 16, col = adjustcolor(RED, .58), axes = FALSE, xlab = "Fitted value", ylab = "Residual")
axis(1); axis(2); abline(h = 0, col = INK); text(max(fitted(fit)) * .82, max(resid(fit)) * .8, "fan shape", col = RED, font = 2)
dev.off()

open_svg(asset("S03", "small-samples.svg"))
x <- seq(-1.5, 1.5, length.out = 500); ns <- c(5, 20, 100); cols <- c(RED, GOLD, BLUE)
plot(x, dnorm(x, sd = 1 / sqrt(5)), type = "n", axes = FALSE, xlab = "Sample-mean error", ylab = "Density",
     ylim = c(0, max(dnorm(x, sd = 1 / sqrt(100))) * 1.04)); axis(1); axis(2)
for (i in seq_along(ns)) lines(x, dnorm(x, sd = 1 / sqrt(ns[i])), col = cols[i], lwd = 2.5)
legend("topright", paste("n =", ns), col = cols, lwd = 3, bty = "n")
headline("Small samples make estimates unstable", "The sampling distribution narrows at the familiar 1/√n rate")
dev.off()

# Session 04: logistic regression -------------------------------------------

open_svg(asset("S04", "logistic-curves.svg"), width = 10.5, height = 5.8)
par(mfrow = c(1, 2), mar = c(3.3, 3.7, 3.6, .8))
x <- seq(-6, 6, length.out = 400)
for (sign in c(1, -1)) {
  p <- plogis(sign * x)
  plot(x, p, type = "n", ylim = c(0, 1), axes = FALSE, xlab = "Predictor x", ylab = "Probability")
  axis(1); axis(2, at = c(0, .5, 1)); abline(h = c(0, .5, 1), col = GRID, lty = c(1, 2, 1))
  lines(x, p, col = if (sign == 1) RED else BLUE, lwd = 3)
  title(if (sign == 1) "Positive coefficient" else "Negative coefficient", adj = 0, font.main = 2)
  text(if (sign == 1) 3.5 else -3.5, .82, if (sign == 1) "odds rise" else "odds fall",
       col = if (sign == 1) RED else BLUE, font = 2)
}
dev.off()

# Session 07: PCA and factor analysis ---------------------------------------

set.seed(48)
open_svg(asset("S07", "bayes-classifier.svg"))
n <- 90; x1 <- rnorm(n, rep(c(-1.2, 1.25), each = n / 2), .75); x2 <- rnorm(n, rep(c(.6, -.4), each = n / 2), .8)
grp <- rep(c(0, 1), each = n / 2)
plot(x1, x2, pch = 21, bg = ifelse(grp == 0, PALE_RED, PALE_BLUE), col = ifelse(grp == 0, RED, BLUE),
     axes = FALSE, xlab = "Feature 1", ylab = "Feature 2", cex = 1.05); axis(1); axis(2)
curve(.18 * x^2 - .35 * x + .05, from = -3.2, to = 3.2, add = TRUE, col = INK, lwd = 2.7)
text(-2.4, -1.4, "class A", col = RED, font = 2); text(2.1, 1.35, "class B", col = BLUE, font = 2)
headline("The Bayes boundary assigns the most probable class")
dev.off()

open_svg(asset("S07", "cross-validation.svg"), width = 11, height = 5.6)
plot.new(); plot.window(xlim = c(0, 12), ylim = c(0, 10)); headline("Ten-fold cross-validation rotates the test set")
for (r in 1:6) {
  for (k in 1:10) rect(k, 8.4 - r, k + .78, 8.92 - r, col = if (k == r) RED else "white", border = GRID)
  text(.65, 8.65 - r, paste0("fold ", r), adj = 1, cex = .68, col = MUTED)
}
text(5.9, 1.35, "Every observation is tested once; training never sees its own test fold.", cex = .76, col = INK, font = 2)
dev.off()

open_svg(asset("S07", "learning-taxonomy.svg"), width = 11, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("Learning problems differ by the signal available")
box(50, 82, 28, 9, "Machine learning", fill = INK, border = INK, col = "white", cex = .82)
box(22, 60, 25, 9, "Supervised", fill = PALE_RED, border = RED)
box(50, 60, 25, 9, "Unsupervised", fill = PALE_BLUE, border = BLUE)
box(78, 60, 25, 9, "Reinforcement", fill = PALE_TEAL, border = TEAL)
segments(50, 77.5, c(22, 50, 78), c(64.5, 64.5, 64.5), col = MUTED, lwd = 1.5)
box(14, 35, 20, 8, "Classification", fill = "white", border = GRID)
box(31, 35, 20, 8, "Regression", fill = "white", border = GRID)
box(44, 35, 20, 8, "Clustering", fill = "white", border = GRID)
box(61, 35, 20, 8, "Dimension reduction", fill = "white", border = GRID)
box(78, 35, 20, 8, "Policy learning", fill = "white", border = GRID)
segments(22, 55.5, c(14, 31), c(39, 39), col = MUTED)
segments(50, 55.5, c(44, 61), c(39, 39), col = MUTED)
segments(78, 55.5, 78, 39, col = MUTED)
text(50, 18, "PCA and factor analysis live in the unsupervised branch.", col = RED, font = 2, cex = .82)
dev.off()

set.seed(54)
open_svg(asset("S07", "pca-axes.svg"))
z1 <- rnorm(95, 0, 1.35); z2 <- .55 * z1 + rnorm(95, 0, .48)
plot(z1, z2, pch = 21, bg = PALE_BLUE, col = BLUE, axes = FALSE, xlab = "Original variable x", ylab = "Original variable y")
axis(1); axis(2); arrows(-2.8, -1.5, 2.9, 1.65, col = RED, lwd = 3, length = .1)
arrows(1.0, -2.0, -1.0, 2.0, col = INK, lwd = 2, length = .1)
direct_label(2.15, 1.5, "PC1: most variance", RED, 4)
direct_label(-.9, 1.9, "PC2", INK, 2)
headline("PCA rotates the axes toward maximum variation")
dev.off()

set.seed(60)
open_svg(asset("S07", "pca-biplot.svg"))
score1 <- rnorm(45); score2 <- .35 * score1 + rnorm(45, sd = .72)
plot(score1, score2, pch = 21, bg = PALE_BLUE, col = BLUE, axes = FALSE, xlab = "PC1", ylab = "PC2", xlim = c(-2.7, 2.7), ylim = c(-2.3, 2.3))
axis(1); axis(2); abline(h = 0, v = 0, col = GRID)
loads <- rbind(c(1.8, .6), c(1.3, -1.4), c(-1.2, 1.5), c(-1.7, -.6)); labs <- c("productivity", "investment", "skills", "energy")
for (i in 1:4) { arrows(0, 0, loads[i, 1], loads[i, 2], col = RED, lwd = 2, length = .09); direct_label(loads[i, 1], loads[i, 2], labs[i], RED, 4) }
headline("A biplot joins observations with variable loadings")
dev.off()

open_svg(asset("S07", "dimension-reduction-map.svg"), width = 11, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("Choose a method from the variables you actually have")
box(50, 82, 30, 9, "Multivariate data", fill = INK, border = INK, col = "white")
box(18, 59, 25, 9, "Quantitative", fill = PALE_BLUE, border = BLUE)
box(50, 59, 25, 9, "Qualitative", fill = PALE_TEAL, border = TEAL)
box(82, 59, 25, 9, "Mixed", fill = PALE_RED, border = RED)
segments(50, 77.5, c(18, 50, 82), c(63.5, 63.5, 63.5), col = MUTED)
box(11, 34, 17, 8, "PCA", fill = "white", border = BLUE)
box(29, 34, 17, 8, "Factor analysis", fill = "white", border = BLUE)
box(50, 34, 17, 8, "MCA", fill = "white", border = TEAL)
box(74, 34, 17, 8, "FAMD", fill = "white", border = RED)
box(91, 34, 14, 8, "MFA", fill = "white", border = RED)
segments(18, 54.5, c(11, 29), c(38, 38), col = MUTED); segments(50, 54.5, 50, 38, col = MUTED); segments(82, 54.5, c(74, 91), c(38, 38), col = MUTED)
dev.off()

# Session 08: KNN and bias-variance -----------------------------------------

open_svg(asset("S08", "bias-variance.svg"))
cplx <- seq(0.03, 1, length.out = 300); bias2 <- 1.05 * exp(-3.2 * cplx) + .05; variance <- .08 + .82 * cplx^2; total <- bias2 + variance + .13
plot(cplx, total, type = "n", axes = FALSE, xlab = "Model flexibility", ylab = "Expected test error", ylim = c(0, 1.25)); axis(1, at = c(.05, .5, .95), labels = c("simple", "balanced", "very flexible")); axis(2)
lines(cplx, bias2, col = BLUE, lwd = 2.5); lines(cplx, variance, col = RED, lwd = 2.5); lines(cplx, total, col = INK, lwd = 3)
best <- which.min(total); abline(v = cplx[best], col = GOLD, lty = 2, lwd = 2)
direct_label(.18, bias2[45], "bias²", BLUE, 4); direct_label(.82, variance[245], "variance", RED, 4); direct_label(cplx[best], total[best], "lowest total error", GOLD, 4)
headline("Good prediction balances bias against variance")
dev.off()

set.seed(72); x <- sort(runif(35, -3, 3)); truth <- sin(x) + .15 * x; y <- truth + rnorm(35, 0, .22)
open_svg(asset("S08", "underfit.svg"))
plot(x, y, pch = 21, bg = PALE_BLUE, col = BLUE, axes = FALSE, xlab = "x", ylab = "y"); axis(1); axis(2)
abline(lm(y ~ x), col = RED, lwd = 3); lines(x, truth, col = INK, lwd = 2, lty = 2)
headline("Underfitting leaves stable structure unexplained")
legend("topleft", c("linear fit", "signal"), col = c(RED, INK), lwd = c(3, 2), lty = c(1, 2), bty = "n")
dev.off()

open_svg(asset("S08", "overfit.svg"))
plot(x, y, pch = 21, bg = PALE_BLUE, col = BLUE, axes = FALSE, xlab = "x", ylab = "y"); axis(1); axis(2)
polyfit <- lm(y ~ poly(x, 10)); gridx <- seq(min(x), max(x), length.out = 500); lines(gridx, predict(polyfit, newdata = data.frame(x = gridx)), col = RED, lwd = 2.5)
lines(x, truth, col = INK, lwd = 2, lty = 2); headline("Overfitting follows noise as though it were signal")
dev.off()

set.seed(75)
open_svg(asset("S08", "knn-boundary.svg"))
a <- cbind(rnorm(70, -1.1, .7), rnorm(70, .4, .8)); b <- cbind(rnorm(70, 1.1, .75), rnorm(70, -.25, .75))
plot(a, pch = 21, bg = PALE_RED, col = RED, axes = FALSE, xlab = "Feature 1", ylab = "Feature 2", xlim = c(-3, 3), ylim = c(-2.6, 2.6)); points(b, pch = 21, bg = PALE_BLUE, col = BLUE); axis(1); axis(2)
curve(.18 * sin(2 * x) - .2 * x, from = -3, to = 3, add = TRUE, col = INK, lwd = 3)
headline("KNN lets nearby observations draw the boundary")
dev.off()

open_svg(asset("S08", "nearest-neighbours.svg"))
set.seed(79); pts <- cbind(runif(18, -2.4, 2.4), runif(18, -2, 2)); cl <- rep(c(RED, BLUE), 9)
plot(pts, pch = 21, bg = adjustcolor(cl, .22), col = cl, cex = 1.15, axes = FALSE, xlab = "Feature 1", ylab = "Feature 2", asp = 1); axis(1); axis(2)
symbols(0, 0, circles = 1.15, inches = FALSE, add = TRUE, fg = TEAL, lwd = 2.5); points(0, 0, pch = 4, lwd = 3, cex = 1.4, col = INK)
text(1.2, 1.15, "k-neighbourhood", col = TEAL, font = 2, pos = 4)
headline("A query inherits the majority label in its neighbourhood")
dev.off()

open_svg(asset("S08", "complexity-compare.svg"), width = 11, height = 5.7)
par(mfrow = c(1, 3), mar = c(3, 2.4, 3.5, .5))
set.seed(81); px <- runif(70, -2.5, 2.5); py <- runif(70, -2, 2); cls <- px + .35 * py + rnorm(70, 0, .65) > 0
for (i in 1:3) {
  plot(px, py, pch = 21, bg = ifelse(cls, PALE_BLUE, PALE_RED), col = ifelse(cls, BLUE, RED), axes = FALSE, xlab = "", ylab = "")
  if (i == 1) curve(.25 * sin(5 * x), add = TRUE, col = INK, lwd = 2.3)
  if (i == 2) curve(.12 * sin(1.4 * x), add = TRUE, col = INK, lwd = 2.3)
  if (i == 3) abline(v = 0, col = INK, lwd = 2.3)
  title(c("k = 1: jagged", "k = 10: balanced", "k = 100: blunt")[i], adj = 0, font.main = 2, cex.main = .9)
}
dev.off()

open_svg(asset("S08", "error-complexity.svg"))
cplx <- seq(.02, 1, length.out = 220); train <- .65 * exp(-3.3 * cplx) + .08; test <- .22 + 1.05 * (cplx - .48)^2
plot(cplx, test, type = "n", axes = FALSE, xlab = "Model flexibility", ylab = "Error", ylim = c(0, .82)); axis(1, at = c(.05, .5, .95), labels = c("simple", "balanced", "flexible")); axis(2)
lines(cplx, train, col = BLUE, lwd = 2.7); lines(cplx, test, col = RED, lwd = 2.7); abline(v = cplx[which.min(test)], col = GOLD, lty = 2)
direct_label(.72, train[160], "training", BLUE, 4); direct_label(.72, test[160], "test", RED, 4)
headline("Training error keeps falling after test error turns")
dev.off()

open_svg(asset("S08", "confusion-matrix.svg"), width = 8.4, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("A confusion matrix separates four kinds of decision")
rect(22, 16, 82, 76, border = INK, lwd = 2); segments(52, 16, 52, 76, col = INK); segments(22, 46, 82, 46, col = INK)
rect(22, 46, 52, 76, col = PALE_TEAL, border = NA); rect(52, 16, 82, 46, col = PALE_TEAL, border = NA)
rect(52, 46, 82, 76, col = PALE_RED, border = NA); rect(22, 16, 52, 46, col = PALE_RED, border = NA)
segments(52, 16, 52, 76, col = INK); segments(22, 46, 82, 46, col = INK); rect(22, 16, 82, 76, border = INK, lwd = 2)
text(c(37, 67, 37, 67), c(61, 61, 31, 31), c("TRUE\nPOSITIVE", "FALSE\nPOSITIVE", "FALSE\nNEGATIVE", "TRUE\nNEGATIVE"), font = 2, cex = .82, col = c(TEAL, RED, RED, TEAL))
text(52, 83, "PREDICTED", font = 2); text(14, 46, "ACTUAL", srt = 90, font = 2)
dev.off()

# Session 09: SEM ------------------------------------------------------------

open_svg(asset("S09", "cfa-model.svg"), width = 11, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("CFA links latent constructs to observed indicators")
lat <- c(20, 50, 80); labs <- c("Visual", "Textual", "Speed"); fills <- c(PALE_RED, PALE_BLUE, PALE_TEAL); borders <- c(RED, BLUE, TEAL)
for (i in 1:3) {
  node_circle(lat[i], 73, 8, labs[i], fills[i], borders[i])
  for (j in 1:3) { xx <- lat[i] + (j - 2) * 8; box(xx, 33, 7, 8, paste0(substr(labs[i], 1, 1), j), fill = "white"); link(lat[i] + (j - 2) * 1.2, 65, xx, 37, borders[i], 1.4) }
}
dev.off()

open_svg(asset("S09", "sem-model.svg"), width = 11, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("SEM estimates direct and indirect paths together")
node_circle(17, 62, 9, "Capabilities", PALE_BLUE, BLUE); node_circle(50, 62, 9, "Innovation", PALE_TEAL, TEAL); node_circle(83, 62, 9, "Performance", PALE_RED, RED)
link(26, 62, 41, 62, BLUE, label = "0.48"); link(59, 62, 74, 62, TEAL, label = "0.37"); link(23, 53, 77, 53, RED, label = "0.18 direct")
for (x0 in c(12, 17, 22)) box(x0, 28, 7, 7, paste0("x", (x0 - 7) / 5), fill = "white")
for (x0 in c(45, 50, 55)) box(x0, 28, 7, 7, paste0("m", (x0 - 40) / 5), fill = "white")
for (x0 in c(78, 83, 88)) box(x0, 28, 7, 7, paste0("y", (x0 - 73) / 5), fill = "white")
dev.off()

open_svg(asset("S09", "tpb-model.svg"), width = 11, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("A theory becomes testable when its paths are explicit")
box(16, 76, 22, 9, "Attitude", fill = PALE_RED, border = RED)
box(16, 52, 22, 9, "Subjective norms", fill = PALE_BLUE, border = BLUE)
box(16, 28, 22, 9, "Perceived control", fill = PALE_TEAL, border = TEAL)
box(53, 52, 22, 11, "Intention", fill = "white", border = INK)
box(84, 52, 22, 11, "Behaviour", fill = INK, border = INK, col = "white")
link(27, 76, 42, 57, RED, label = ".42"); link(27, 52, 42, 52, BLUE, label = ".28"); link(27, 28, 42, 47, TEAL, label = ".35"); link(64, 52, 73, 52, INK, label = ".61")
link(27, 28, 75, 46, TEAL, label = ".14 direct")
dev.off()

# Session 10: causal framework ----------------------------------------------

open_svg(asset("S10", "potential-outcomes.svg"), width = 11, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("Causal effects compare two outcomes for the same unit")
box(16, 54, 20, 11, "Unit i", fill = INK, border = INK, col = "white", cex = .84)
box(52, 72, 28, 12, "Yᵢ(1): treated", fill = PALE_RED, border = RED, col = INK)
box(52, 36, 28, 12, "Yᵢ(0): untreated", fill = PALE_BLUE, border = BLUE, col = INK)
link(26, 58, 38, 69, RED); link(26, 50, 38, 39, BLUE)
box(84, 72, 20, 10, "observed", fill = "white", border = RED, col = RED)
box(84, 36, 20, 10, "counterfactual", fill = "white", border = BLUE, col = BLUE)
text(52, 13, "Individual effect = Yᵢ(1) − Yᵢ(0)", cex = .92, font = 2, col = INK)
dev.off()

# Session 11: difference in differences -------------------------------------

open_svg(asset("S11", "did-basic.svg"))
plot(c(0, 1), c(35, 55), type = "n", axes = FALSE, xlab = "", ylab = "Outcome", xlim = c(-.12, 1.18), ylim = c(25, 95)); axis(1, at = c(0, 1), labels = c("Before", "After")); axis(2)
lines(c(0, 1), c(35, 55), col = BLUE, lwd = 3); points(c(0, 1), c(35, 55), pch = 16, col = BLUE)
lines(c(0, 1), c(50, 85), col = RED, lwd = 3); points(c(0, 1), c(50, 85), pch = 16, col = RED)
lines(c(0, 1), c(50, 70), col = RED, lwd = 2, lty = 2); segments(1.03, 70, 1.03, 85, col = GOLD, lwd = 4)
direct_label(.08, 38, "control", BLUE, 4); direct_label(.08, 53, "treated", RED, 4); direct_label(1.03, 78, "DiD = 15", GOLD, 4)
headline("Difference-in-differences isolates the change beyond the common trend")
dev.off()

open_svg(asset("S11", "did-table.svg"), width = 9.4, height = 6)
plot.new(); plot.window(xlim = c(0, 100), ylim = c(0, 100)); headline("The estimator is a difference of two changes")
xs <- c(8, 41, 65, 91); ys <- c(78, 60, 42, 24)
rect(8, 70, 91, 82, col = INK, border = NA)
for (i in 1:3) text((xs[i] + xs[i + 1]) / 2, 76, c("Group", "Before", "After")[i], col = "white", font = 2)
vals <- list(c("Control", "35", "55"), c("Treated", "50", "85"), c("Change", "+15", "+30"))
for (r in 1:3) for (j in 1:3) text((xs[j] + xs[j + 1]) / 2, ys[r + 1], vals[[r]][j], cex = .9, font = if (r == 3) 2 else 1, col = if (r == 3) RED else INK)
segments(8, 32, 91, 32, col = GRID, lwd = 2); text(50, 14, "DiD = 30 − 15 = 15", col = RED, font = 2, cex = 1.2)
dev.off()

open_svg(asset("S11", "did-coefficients.svg"), width = 11, height = 6)
plot(c(0, 1), c(35, 55), type = "n", axes = FALSE, xlab = "", ylab = "Outcome", xlim = c(-.18, 1.32), ylim = c(25, 95)); axis(1, at = c(0, 1), labels = c("Pre", "Post")); axis(2)
lines(c(0, 1), c(35, 55), col = BLUE, lwd = 3); lines(c(0, 1), c(50, 85), col = RED, lwd = 3)
points(rep(c(0, 1), 2), c(35, 55, 50, 85), pch = 16, col = rep(c(BLUE, RED), each = 2))
text(-.08, 35, "β₀", col = BLUE, font = 2); segments(-.04, 35, -.04, 50, col = GOLD, lwd = 3); text(-.08, 43, "β₁", col = GOLD, font = 2)
segments(1.08, 35, 1.08, 55, col = BLUE, lwd = 3); text(1.12, 45, "β₂", col = BLUE, font = 2, pos = 4)
segments(1.18, 70, 1.18, 85, col = RED, lwd = 3); text(1.22, 78, "β₃", col = RED, font = 2, pos = 4)
headline("Each DiD coefficient maps to one visible contrast")
dev.off()

open_svg(asset("S11", "did-counterfactual.svg"))
plot(c(0, 1), c(35, 55), type = "n", axes = FALSE, xlab = "", ylab = "Outcome", xlim = c(-.12, 1.2), ylim = c(25, 95)); axis(1, at = c(0, 1), labels = c("Before", "After")); axis(2)
lines(c(0, 1), c(35, 55), col = BLUE, lwd = 3); lines(c(0, 1), c(50, 85), col = RED, lwd = 3)
lines(c(0, 1), c(50, 70), col = RED, lwd = 3, lty = 2); segments(1.03, 70, 1.03, 85, col = GOLD, lwd = 4)
direct_label(.72, 67, "counterfactual", RED, 2); direct_label(.7, 85, "observed treated", RED, 2); direct_label(.72, 52, "control trend", BLUE, 2)
headline("Parallel trends supply the missing counterfactual")
dev.off()

count <- length(unique(generated_assets))
cat("Built", count, "Economist-style assets.\n")
