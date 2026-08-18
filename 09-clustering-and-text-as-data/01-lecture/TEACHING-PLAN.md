# Session 09 — teaching plan (first half, 90 min)

# Unsupervised Learning II: Clustering, Embeddings, and Text as Data

> **Instructor page.** The student-facing derivations are in
> [`README.md`](README.md); this is how to deliver them.

`MATH60033A` · lecture 90 min · lab follows on
*Do European countries fall into types — and does the language of policy track them?*

---

## Opening

Run k-means with $k=4$ on 200 draws from a uniform square, projected live. Four tight, convincing clusters. Ask what they mean. **Nothing.** Every clustering algorithm returns clusters, including on noise.

---

## Board plan

| Minutes | |
|---|---|
| **0–07** | The hook. Establish that the burden of proof is entirely on the analyst. |
| **07–27** | k-means objective and Lloyd's algorithm. Show each step is optimal given the other, hence monotone decrease, hence convergence — to a **local** minimum. k-means++. |
| **27–40** | What the Euclidean objective assumes. Draw the Voronoi tessellation and note that convex, spherical, similarly-sized clusters are *forced* by the algorithm, not discovered. Alternatives when that is wrong. |
| **40–50** | Hierarchical clustering and the linkage table. Ward as the k-means criterion in agglomerative form. |
| **50–65** | Choosing $k$: elbow, silhouette, gap statistic. Stress that the gap statistic can return $k=1$, which is why it is worth the extra effort. |
| **65–82** | Text. TF-IDF and the fact that it is the $p \gg n$ setting of Session 05, so penalised regression is the natural supervised tool on top. Embeddings and cosine similarity. Dictionary methods and why transparency often wins. |
| **82–90** | **Validity.** The four criteria. This is what the lab is graded on. |

---

## Worked example — do this live

Compute one silhouette by hand: a point with $a_i = 1.2$ to its own cluster and $b_i = 2.0$ to the nearest other gives $s_i = 0.4$. Then show a point with $a_i = 2.0$, $b_i = 1.2$ giving $-0.4$ — probably misassigned.

> Working an example on the board is not a break from the derivation; it is what converts the
> derivation into something students can use under pressure. Do it slowly enough that they copy it.

---

## Put this to the room

*"What would count as evidence that a text-derived index measures what it claims?"* Do not accept 'it correlates with something'. Push to face validity — actually reading the documents.

---

## Misconception to pre-empt

> That clustering discovers structure. It imposes a structure and reports how well the data tolerate it. The permuted-data comparison in the lab exists to make this visceral.

Say it explicitly, early, and once more at the end. Misconceptions that go unnamed in the lecture
reappear in the deliverable.

---

## Leave on the board for the lab

The four validity criteria and the Voronoi picture.

---

## If you are running short

Compress hierarchical linkage to the table. Never cut the validity section — it is the graded part.

---

## Then hand over

The second half is the groups' own. Remind them:

- the presenter is **drawn at random** when their group is called — `python scripts/assess.py draw --session 9`
- the report is **one slide, three sentences**, and sentence three is the one that earns the slot
- the **role log** is filled in before they leave the room

---

[Student notes](README.md) · [Session 09](../README.md) · [Lab](../02-lab/README.md)
