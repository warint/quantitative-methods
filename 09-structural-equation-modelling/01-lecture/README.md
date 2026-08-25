# Session 09 — Lecture (first half, ~90 min)

# Unsupervised Learning II: Clustering, Embeddings, and Text as Data

> **How do you measure something that only exists as words?**

---

### 9.1 k-means

Partition observations into $k$ clusters $C_1,\dots,C_k$ minimising within-cluster sum of squares:

$$\min_{C_1,\dots,C_k} \sum_{j=1}^{k} \sum_{i \in C_j} \|x_i - \mu_j\|^2, \qquad
\mu_j = \frac{1}{|C_j|}\sum_{i\in C_j} x_i .$$

The problem is NP-hard. **Lloyd's algorithm** alternates two steps, each of which weakly decreases
the objective:

1. **Assign:** $c_i \leftarrow \arg\min_j \|x_i - \mu_j\|^2$.
2. **Update:** $\mu_j \leftarrow$ mean of points assigned to $j$.

Step 2 is optimal given assignments (differentiate the objective in $\mu_j$ and set to zero); step 1
is optimal given centroids. Since the objective decreases monotonically and there are finitely many
partitions, the algorithm terminates - **at a local minimum**. Run it many times from different
starts (`n_init`), or use **k-means++** initialisation, which seeds centroids with probability
proportional to squared distance from the nearest existing centroid and gives an
$O(\log k)$-competitive guarantee in expectation.

**What the Euclidean objective assumes.** Because clusters are defined by nearest-centroid, the
decision boundaries are the perpendicular bisectors between centroids - a Voronoi tessellation.
This *forces* convex, roughly spherical, similarly-sized clusters. Elongated or nested structures
will be cut incorrectly no matter how well you optimise. If that assumption is wrong, use a
Gaussian mixture (which allows covariance structure and gives soft assignments via EM), or
DBSCAN / spectral clustering for non-convex shapes.

### 9.2 Hierarchical clustering

Build a dendrogram bottom-up (agglomerative), merging the two closest clusters at each step. The
linkage function defines "closest":

| Linkage | $d(A,B)$ | Behaviour |
|---|---|---|
| Single | $\min_{a,b}\|a-b\|$ | Chaining; finds elongated shapes; unstable |
| Complete | $\max_{a,b}\|a-b\|$ | Compact, similar-diameter clusters |
| Average | mean pairwise distance | Compromise; not invariant to monotone transforms |
| **Ward** | increase in within-cluster SS from merging | Minimises the same criterion as k-means; usually the default to try |

The advantage over k-means is that you need not fix $k$ in advance; the dendrogram shows structure
at every resolution. The cost is $O(n^2)$ memory.

### 9.3 Choosing $k$

- **Elbow:** plot within-cluster SS against $k$; it always decreases, so look for a kink. Often no
  kink exists.
- **Silhouette:** for observation $i$, $s_i = (b_i - a_i)/\max(a_i,b_i)$ with $a_i$ the mean
  distance to its own cluster and $b_i$ the mean distance to the nearest other cluster. $s_i$ near
  1 is well-clustered, near 0 is on a boundary, negative means it is probably misassigned. Average
  over $i$ and maximise over $k$.
- **Gap statistic:** compare $\log W_k$ to its expectation under a null reference distribution
  (uniform over the data's bounding box or PCA-aligned box); choose the smallest $k$ where the gap
  exceeds the next $k$'s gap minus one standard error. This one can return $k=1$, i.e. "no cluster
  structure" - which is why it is worth the extra effort.

**Report at least two, and report disagreement.** A single elbow plot is not evidence.

### 9.4 Representing text

**Bag of words / TF-IDF.** Document $d$, term $t$:

$$\mathrm{tf\text{-}idf}(t,d) = \underbrace{f_{t,d}}_{\text{term frequency}} \times
\underbrace{\log\frac{N}{1 + n_t}}_{\text{inverse document frequency}} .$$

The idf factor downweights ubiquitous terms. Result: a very sparse, very high-dimensional matrix -
exactly the $p \gg n$ setting of Sessions 5 and 6, so penalised regression is the natural supervised
tool on top of it. Note the tradeoff: bag-of-words discards word order entirely. *"Inflation is not
a concern"* and *"a concern is not inflation"* are identical vectors.

**Dense embeddings.** A model maps each document to $v_d \in \mathbb{R}^m$ (typically $m$ = 384 to
1024), trained so that semantically similar texts have similar vectors. Similarity is measured by
cosine:

$$\cos(v_a, v_b) = \frac{v_a^\top v_b}{\|v_a\|\|v_b\|} \in [-1,1] .$$

Cosine ignores magnitude, which is what you want when documents differ in length. You will generate
embeddings **locally** in the practice session - the corpus never leaves your machine, which is both a
methodological and a governance point worth noting.

**Dictionary methods** (count terms from a pre-specified list) remain widely used in economics
precisely because they are transparent and auditable. Sophistication is not automatically an
improvement: an embedding-based index that no one can interrogate may be *less* useful for policy
than a word count that anyone can check.

### 9.5 Validity - the part that is actually hard

Four questions to answer about any text-derived measure:

1. **Face validity:** read a random sample of high-scoring and low-scoring documents. Do they look
   like what you claim to measure? (Do this. Actually read them.)
2. **Convergent validity:** does the index correlate with independent measures of the same
   construct?
3. **Predictive validity:** does it forecast something it should?
4. **Robustness:** does it survive changes in preprocessing, vocabulary, and model? If your finding
   depends on a stemming choice, you do not have a finding.

---

## Notation reminders used throughout the course

| Symbol | Meaning |
|---|---|
| $n$, $p$ | number of observations, number of predictors |
| $X$ | $n \times p$ design matrix (first column ones, unless stated) |
| $y$ | $n$-vector of outcomes |
| $\hat\beta$ | estimated coefficient vector |
| $\hat y = X\hat\beta$ | fitted values |
| $H = X(X^\top X)^{-1}X^\top$ | hat (projection) matrix |
| $\lambda$, $\alpha$ | penalty strength, elastic-net mixing parameter |
| $L(y,\hat y)$ | loss function |

> **Rendering the mathematics.** These notes use LaTeX. In VS Codium, install the
> *Markdown+Math* or *Markdown Preview Enhanced* extension and open the preview with
> `Ctrl/Cmd+K V`. See the [setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).

---

[Back to session 09](../README.md) · [On to the practice ->](../02-practice/README.md)
