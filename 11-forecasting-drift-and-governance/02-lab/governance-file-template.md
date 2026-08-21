# Model governance file — group XX

> Template for the Session 11 lab and the Session 12 deliverable (30% of the final mark).
> Replace every bracketed prompt. A section left as a placeholder scores zero for that section.
>
> **The test:** could a competent analyst who has never met you pick this up in three years and
> know what the model does, whether to trust it, and when to retire it?

---

## 1. Intended use and out-of-scope uses

- **Decision supported:** [what specific decision does this model inform? who makes it?]
- **Users:** [who reads the output?]
- **Out of scope:** [name at least two uses this model must NOT be put to, and why]

## 2. Data lineage

| Item | Detail |
|---|---|
| Source(s) | [institution, dataset name] |
| URL | [ ] |
| Vintage / collection date | [ ] |
| Licence | [ ] |
| Checksum | [sha256] |
| Known quality issues | [missingness, revisions, breaks in series, coverage gaps] |

**Revisions:** [is this series revised? did you use real-time vintages? if not, say so plainly]

## 3. Preprocessing

Every transformation, in order, with the function that performs it.

| # | Step | Implemented in | Inside the CV loop? |
|---|---|---|---|
| 1 | [ ] | [file:function] | yes / no |
| 2 | [ ] | [ ] | yes / no |

**Any step marked "no" must be justified here:** [ ]

## 4. Validation

- **CV / backtest design:** [scheme, and *why it mirrors deployment*]
- **Purge / embargo:** [ ] periods, because [ ]
- **Benchmark:** [random walk / AR(p) / consensus / prior model]
- **Headline metric vs. benchmark:** [ ]
- **Diebold–Mariano (or equivalent):** statistic [ ], p-value [ ], variance estimator [ ]
- **Subgroup performance:** [table — performance by the groups that matter for this decision]
- **Calibration:** [reliability diagram summary, if probabilities are used]

## 5. Limitations

> Weighted heavily. Be specific; "the model may not generalise" scores nothing.

- **Worst performance on:** [which regime, period, or subpopulation, with numbers]
- **Under-represented in training:** [ ]
- **Load-bearing assumptions:** [which assumption, if wrong, changes the conclusion?]
- **Causal status:** [is this predictive or causal? if causal, what identifies it? name one plausible unmeasured confounder]
- **Goodhart exposure:** [could agents change behaviour once this is used? which feature is most at risk?]

## 6. Monitoring plan

| Quantity tracked | Frequency | Review trigger | Owner |
|---|---|---|---|
| [e.g. train-vs-deploy classifier AUC] | [monthly] | [> 0.65] | [ ] |
| [prediction distribution drift] | [ ] | [ ] | [ ] |
| [realised error vs. backtest error] | [ ] | [ ] | [ ] |

**Retraining policy:** [when, on what data, who approves]

## 7. Ownership

- **Accountable:** [ ]
- **Reviewed by:** [ ]
- **Retirement criterion:** [what observation would mean this model should be switched off?]

---

## Reproducibility statement

```bash
git clone <repo> && cd <repo>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python <entry point>
```

- Random seeds set in: [ ]
- Data cached at: [ ] (not downloaded at runtime)
- Approximate runtime: [ ]

## LLM use

Per the standing rule: describe at least one instance where your local model was wrong,
unverifiable, or misleading, and how you established that.

[ ]
