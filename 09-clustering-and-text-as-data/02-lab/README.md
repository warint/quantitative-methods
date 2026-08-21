# Session 09 — Group lab (second half, ~90 min)

# Building and validating an index from central bank language

---

## The theme of this session

> # Do European countries fall into types — and does the language of policy track them?

All ten groups attack this question. Each answers it with **its own angle** and its own slice of the
data spine, and the last twenty minutes assemble the five answers into one.

Angles A–D cluster their countries; Angle E builds the text indices. The class then compares cluster memberships pairwise with the adjusted Rand index.

Your angle, your unit of analysis and your data are fixed for the semester:
**[RESEARCH-MANDATES.md](../../RESEARCH-MANDATES.md)**.

> **If your angle cannot answer the theme this week, say so and show why.** That is a contribution,
> not a failure — and it is graded as one.

---

## Method exercise

The tasks below build the machinery. Do them on the teaching dataset if you need to see the method
work on known ground first, then turn it on your own angle. The reported result must be from **your
angle**.

## Brief

Groups of 3-4. Two halves: cluster European regions on economic indicators, then
construct a text-based uncertainty index and try seriously to break it.

---

## Tasks

1. Implement `lloyd(X, k, n_init)` yourself, with k-means++ initialisation. Verify against `sklearn.cluster.KMeans`. Show that different seeds give different objectives - report the spread.
2. Cluster European regions on GDP per capita, unemployment, and sectoral shares. Choose $k$ by elbow, silhouette **and** gap statistic. Report all three and any disagreement.
3. Map the clusters. Do they correspond to anything an economic geographer would recognise? Now run the same algorithm on permuted (structure-free) data - what does it return?
4. Compare Ward-linkage hierarchical clustering to your k-means solution using the adjusted Rand index. Where do they disagree, and which is more defensible?
5. Build a TF-IDF matrix over the central bank corpus. Report vocabulary size and sparsity.
6. Construct a dictionary-based uncertainty index (BBD-style: documents containing terms from *economy*, *policy* **and** *uncertainty* families). Plot the monthly series.
7. Generate **local** embeddings for each document. Cluster them and inspect the top terms per cluster. Build an embedding-based uncertainty score using cosine similarity to a set of seed sentences.
8. **Validate.** (a) Read 20 documents at each extreme of your index and report your face-validity judgement honestly. (b) Correlate with VSTOXX or an existing EPU series. (c) Test robustness to stemming, stopword lists, and $n$-gram range.

---

## Deliverable

`02-lab/submissions/group-XX/` with the cluster map, the three-criterion $k$
selection, the null-data comparison, both uncertainty indices plotted together, and a 500-word
validity report structured under the four headings in section 9.5. **A negative finding, clearly
demonstrated, receives full marks.**

Create your group's folder as `submissions/group-XX/` where `XX` is your group number.

---

## Working method

- **All work is local.** Data are already cached in `data/spine/`; the LLM runs on your machine.
  Nothing in this lab requires an internet connection.
- **One driver, rotating.** Change who types every 20 minutes. Everyone must be able to explain
  every line.
- **Commit as you go.** `git add -A && git commit -m "..."` at each task boundary. Your commit
  history is evidence of process.

## Suggested prompts for your local LLM

- "My silhouette score says k=2 and my gap statistic says k=6. How should I proceed, and what should I report?"
- "Explain why running k-means on random uniform data still produces tight-looking clusters."
- "I am building a text index of policy uncertainty. Play the referee: give me your three strongest objections to its validity."

**Required in every deliverable:** at least one instance where you identified an LLM output as
wrong, unverifiable, or misleading — with an explanation of how you established that.

---

## The two-minute report

> **The presenter is drawn at random when your group is called.** Any of the three of you may have
> to give this report, so all three must understand the analysis, the number, and what would
> undermine it. See [`GROUP-ASSESSMENT.md`](../../GROUP-ASSESSMENT.md).

**One slide. Three sentences.**

1. **What I did.** *"We regressed X on Y for [our unit], partialling out [Z]."*
2. **The number.** One figure or estimate, with its uncertainty or its benchmark.
3. **The catch.** What surprised you, what you cannot claim, or where your data failed you.

No method exposition — everyone learned it ninety minutes ago. No code on the slide. **Sentence 3
earns the slot:** a result plus what would undermine it is worth more than a result alone.

## Before you leave the room

**Every member commits and pushes from their own machine.** There are no assigned roles — work on
it together — but all three of you appear in the history, every week:

```bash
git add -A && git commit -m "..." && git push
```

`python scripts/assess.py contributions` prints a per-member, per-week grid. A week where you
pushed nothing is visible, and it is the kind of thing worth fixing in week four rather than week
eleven.

---

## Timing

| Minutes | Activity |
|---|---|
| 0–10 | Theme, brief, split the work |
| 10–65 | Analysis on your angle |
| 65–70 | Build the slide, agree the three sentences |
| 70–90 | Ten reports (2 min each) + instructor synthesis |

---

[Back to session 09](../README.md) · [<- Lecture notes](../01-lecture/README.md)
