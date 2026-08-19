# Final exam — research paper and oral

**40% of the final grade** · paper in teams of three, English, academic format · **oral examined
individually, 15 minutes per student**

> You will write for a reader who exists, who is not your professor, and who will use what you
> write — and then you will answer for it, alone.

| Component | Weight | Form |
|---|---|---|
| **Research paper** | 25 | Teams of three |
| **Oral examination** | 15 | Individual, 15 minutes |

---

## Contents

1. [The commission](#1-the-commission)
2. [Why transfer, and not extension](#2-why-transfer-and-not-extension)
3. [Why a literature review](#3-why-a-literature-review)
4. [Choosing your question](#4-choosing-your-question)
5. [Data](#5-data)
6. [Structure of the paper](#6-structure-of-the-paper)
7. [The implementation note](#7-the-implementation-note)
8. [Authorship and LLM statements](#8-authorship-and-llm-statements)
9. [Rubric — the paper](#9-rubric--the-paper)
10. [The oral examination](#10-the-oral-examination)
11. [Timeline and submission](#11-timeline-and-submission)

---

## 1. The commission

[**Science des Données au Féminin en Afrique**](https://sdafrique.org) (SDAfrique) trains one
hundred young women from francophone Africa each year in data science. It runs over three years and
ten courses, led by Dr Bernice Bancole and Prof. Thierry Warin, with partners including
OWSD-Benin, HEC Montréal, the Digital Data Design Institute at Harvard, CIRANO and the R Consortium.

Its pedagogy is experiential and problem-first. Students work in teams of three to five. **Each team
identifies a societal problem in their own community and builds a project that addresses one
dimension of it** — past cohorts have worked on speech recognition, disinformation detection and
health service delivery. They work in R and Markdown, and present their findings as dynamic reports.

**Your commission is to write a methods paper that an SDAfrique student in her second or third year
could pick up and use.**

Concretely: take the method your group spent eleven weeks mastering on European data, carry it to a
problem in Africa, and write the paper that makes the method usable by someone who works in R, on a
modest machine, with limited bandwidth, on a problem she chose herself.

**This is not a simulated client.** The papers judged strong will be offered to the SDAfrique
programme. Write accordingly.

---

## 2. Why transfer, and not extension

The obvious alternative would be to extend your semester work: more countries, more years, a
further robustness check. We are not asking for that, and the reason is worth stating plainly.

> **Re-running a method on more of the same data demonstrates that you can run code. Carrying it
> somewhere else is the only evidence that you understood the method rather than the pipeline.**

Every method you learned this term arrived wrapped in assumptions you absorbed without noticing,
because the European data satisfied them quietly. Move to African data and the wrapping becomes
visible:

- **Your panel gets shorter and wider.** Eurostat gives you fifteen annual observations for
  twenty-seven countries. Afrobarometer gives you survey rounds at irregular intervals. What happens
  to your cross-validation scheme when $T = 6$?
- **Missingness stops being incidental.** In the European spine you could drop the flagged cells.
  Drop them here and you have dropped the countries the paper is about. Missingness is now part of
  the phenomenon.
- **Measurement changes character.** You move from administrative registers to household surveys
  and satellite imagery. Sampling error is no longer negligible, and weights are no longer optional.
- **Your outcome may not be measured at all.** Several of the most important questions in African
  development economics have no direct outcome variable, only proxies — and choosing a proxy is a
  modelling decision you now have to defend.
- **Your reader's constraints are real.** No GPU. A dataset that must be downloadable. A language,
  R, that is not the one you wrote your code in.

None of this is an obstacle to the assignment. **All of it is the assignment.** A paper that
reports honestly that a method fails to transfer, and diagnoses precisely why, is worth more than
one that reports a clean result by quietly choosing the only African dataset that behaves like a
European one.

---

## 3. Why a literature review

You are asked for a literature review of at least **fifteen** substantive sources. Here is the
argument for it, because "because papers have them" is not an argument.

### The old reason, which no longer holds

Literature reviews used to exist largely because finding out what was already known was hard and
slow. That is no longer true. Your assistant will summarise a field in seconds.

### The reason that now matters

**The scarce skill is no longer retrieving an answer. It is asking the right question and
recognising a wrong answer.** Both are functions of expertise, and a literature review is the most
efficient way to acquire expertise in a domain you did not previously know.

Consider what a review actually gives you:

- **A prior over magnitudes.** After fifteen papers on agricultural yield prediction you know that
  a rainfall elasticity of 0.3 is ordinary and one of 3.0 is a bug. Without that prior, 3.0 is just
  a number your code produced.
- **The standard controls.** You learn which variables every serious paper in the field includes,
  and therefore which omission a referee will ask about first.
- **The known data pathologies.** Someone has already discovered that this survey changed its
  sampling frame in 2016. Reading their footnote costs you five minutes; rediscovering it costs
  you a week and possibly a wrong result.
- **The live disagreements.** Knowing what the field argues about tells you where your contribution
  can sit, and stops you from confidently re-deriving a settled point.

### And now the part that concerns your assistant

Here is the concrete mechanism, and it is worth reading twice.

> You run your model and get a coefficient of 3.0.
>
> **Without the review**, you ask your assistant: *"Interpret this coefficient."* It will. Fluently,
> plausibly, and — because you gave it nothing to be suspicious about — without any indication that
> the number is absurd.
>
> **With the review**, you ask: *"The literature on this relationship reports elasticities between
> 0.2 and 0.4. Mine is 3.0. What are the five most likely causes, in order?"*
>
> The second question gets you a useful answer. The first gets you a confident wrong one. **The
> difference between the two questions is the literature review.**

This generalises past this assignment, and it is the single most transferable thing this course has
to teach you. A language model is a superb instrument in the hands of someone who knows enough to
interrogate it, and a confident error-generator in the hands of someone who does not. The review is
what puts you in the first category.

You will also, in the course of it, discover that your assistant invents citations. Finding one is
a required element of your LLM statement (§8).

**Minimum:** fifteen substantive sources, of which at least eight peer-reviewed and at least four
concerning the African context specifically. A source you cite is a source you have read.

---

## 4. Choosing your question

Your paper takes **the method from your semester angle** and applies it to **an African problem**.
Each angle has a natural counterpart. These are starting points, not a menu you must choose from —
a proposed alternative is welcome and often better.

| Your angle | Method you own | Natural African counterpart | Illustrative question |
|---|---|---|---|
| **A** Compute & energy | regression on structure; forecasting | Electricity access and reliability | What predicts grid reliability across sub-Saharan regions, and how much of the variation is composition? |
| **B** Work & skills | task-based exposure; classification | Labour, education, gender gaps | Which occupational or educational transitions predict women's labour force participation? |
| **C** AI adoption | penalised regression; stability selection | Mobile money, internet and firm digitalisation | Of the many candidate correlates of mobile money adoption, which few are robustly selected? |
| **D** Trade & dependence | concentration measures; clustering | Intra-African trade and import dependence | How concentrated is dependence on non-African suppliers in essential goods, and is it falling? |
| **E** Policy language | text as data; validity | African policy, media or open-ended survey text | Can an attention index built from national policy text be validated against outcomes? |

**Whatever you choose, the question must satisfy four tests.**

1. **Public and downloadable.** Someone in Cotonou with an intermittent connection must be able to
   obtain your data. No institutional subscriptions, no datasets over a few hundred megabytes.
2. **Locally meaningful.** The question should be one an SDAfrique student might plausibly have
   chosen herself. If it is only interesting from Montréal, choose again.
3. **Answerable with your method.** Do not bend the question to fit a method you like. If the honest
   answer is that your method is the wrong tool, that is a paper — but say so in the introduction,
   not the conclusion.
4. **Modest in compute.** Must run on a laptop without a GPU, in under an hour.

Confirm your question with the instructor by the date in §10.

---

## 5. Data

### Where to look

All open, all reachable from most of Africa.

| Source | What it has | Access |
|---|---|---|
| **World Bank Open Data / WDI** | development indicators, all countries, long series | open API, `wbdata`, R `WDI` |
| **Afrobarometer** | survey micro-data, 39 countries, francophone Africa well covered | free registration |
| **FAOSTAT** | agriculture, food security, land use | open API |
| **ILOSTAT** | labour force, employment, informality | open API |
| **DHS Program** | health, education, household demographics | free with registration |
| **Humanitarian Data Exchange (HDX)** | very wide, Africa-heavy, often the only source for a country | fully open |
| **WorldPop** | gridded population estimates | fully open |
| **CHIRPS** | rainfall, 1981–present, gridded | fully open |
| **ACLED** | conflict events | free for academic use |
| **UN Comtrade** | bilateral trade | open API |
| **ITU / GSMA** | telecoms, mobile money penetration | ITU open; GSMA partly |
| **Our World in Data** | curated, cleaned, well-documented | fully open |

### What is required of you

- **Provenance for every series**: source, identifier, download date, licence, checksum. Same
  standard as the course spine.
- **Confront the missingness.** State the pattern, state your handling, and state inside which part
  of the pipeline the handling happens. "We dropped incomplete rows" is acceptable only if you also
  report which countries that removed and what it does to your claim.
- **Respect the survey design** if you use survey data. Weights, strata and clustering are not
  optional, and ignoring them is the most common error in student work with Afrobarometer and DHS.
- **Cache it.** Your repository must run from a local cache, not a live download.

---

## 6. Structure of the paper

**6,000 words ± 1,000**, excluding references, tables and appendices. Standard academic format.

| § | Section | Guidance |
|---|---|---|
| — | **Title, authors, abstract** | Abstract 150–200 words: question, data, method, finding, limitation. Write it last. |
| 1 | **Introduction** | The question, why it matters, what you contribute, and — in the last paragraph — what you found. Do not withhold the finding for suspense; this is not a novel. |
| 2 | **Literature** | Fifteen+ sources. Organised by argument, not by author. It must end with the gap your paper addresses. |
| 3 | **Data** | Sources, construction, provenance table, missingness, limitations. Include the descriptive table a referee will ask for. |
| 4 | **Method** | **Derive it.** Not "we use elastic net (Zou and Hastie 2005)" but the objective function, what the penalty does, why the tuning parameter is chosen as it is. Assume a reader who knows regression but not your method. |
| 5 | **Results** | Main result with uncertainty and against a named benchmark. Figures with captions that say what they *show*. |
| 6 | **Robustness and limitations** | What you tested, what moved, what did not. The paragraph naming what would change your conclusion. |
| 7 | **Implementation note for R users** | See §7. This is graded separately and heavily. |
| 8 | **Conclusion** | What an SDAfrique team should take from this, and what they should not. |
| — | **References** | Consistent style. APA or Chicago; choose one. |
| — | **Statements** | CRediT authorship and LLM use. See §8. |

**Accompanying repository**, submitted with the paper: code, cached data, `README.md` with a
one-command reproduction, seeds set, and the provenance file.

---

## 7. The implementation note

**Section 7 of the paper, and 15% of the mark.** This is the section that makes the paper a
deliverable rather than an exercise.

Your reader works in **R**. You worked in Python. Write the bridge.

It must contain:

1. **The method restated free of implementation.** What the procedure *is*, in equations and steps,
   with no reference to any library. If your description only works if the reader has scikit-learn,
   you have not separated method from tooling.
2. **The R route.** Which packages accomplish each step — `glmnet`, `tidymodels`, `ranger`, `caret`,
   `factoextra`, `quanteda` as applicable — and precisely where their defaults differ from the ones
   you used. *(A worked example: `glmnet` standardises by default and returns coefficients on the
   original scale; scikit-learn does neither. A reader who does not know that will not reproduce
   your numbers and will not know why.)*
3. **The pitfalls that cost you time.** Whatever you got wrong, and how you noticed. Be specific.
   This is the most useful paragraph in the paper.
4. **A minimal reproducible example.** Twenty to forty lines of R that run on a small extract and
   produce one interpretable output. It must actually run — test it.
5. **Resource requirements.** Download size, RAM, runtime. Say it plainly.

> **Why this is worth 15%.** Because a method you can only apply inside your own environment is not
> a method you have understood — it is a script you have. Explaining a procedure to someone using
> different tools forces you to separate what is essential from what is incidental, and that
> separation *is* the understanding. It is also, incidentally, the single most valuable professional
> skill on this list: the ability to hand your work to somebody else.

---

## 8. Authorship and LLM statements

### CRediT authorship statement

Required, exactly as a journal would require it. Use the
[CRediT taxonomy](https://credit.niso.org/) and name each author against each role they held:

> **Author contributions.** *Conceptualization:* A.B., C.D. — *Data curation:* C.D. —
> *Formal analysis:* A.B., E.F. — *Methodology:* A.B. — *Software:* E.F., C.D. —
> *Validation:* E.F. — *Visualization:* C.D. — *Writing – original draft:* A.B., C.D. —
> *Writing – review & editing:* all authors.

All three authors must be named in at least three roles, and all three must appear under
*Writing – review & editing*. The statement is signed by all authors and is binding: if questioned,
each author must be able to speak to the roles listed against their name.

> **Why.** Because this is how authorship actually works in academic publishing, and because a
> statement each of you has signed is a more honest instrument than a peer rating collected in
> confidence afterwards. It puts the attribution in the paper, where it belongs.

### LLM use statement

Required. Two paragraphs.

**First**, what you used and for what — drafting, debugging, literature search, translation,
whatever it was. Specificity is expected; "we used AI for assistance" is not a statement.

**Second**, and this is the graded part: **at least one documented instance where the model was
wrong, unverifiable or misleading, and how you established that.** Name the claim, name the check,
name the outcome.

The single most likely candidate is a **fabricated citation**. Verify every reference your
assistant gives you against the actual publisher record. Report what you found.

> A paper submitted with no LLM statement is returned ungraded. A paper whose statement says the
> model was never wrong will be read with interest.

---

## 9. Rubric — the paper

Out of 100, for the 25 points the paper carries.

| Component | Weight | What earns full marks |
|---|---|---|
| **Question and contribution** | 10 | A specific, answerable question that matters locally, with the contribution stated plainly in the introduction |
| **Literature review** | 15 | Fifteen+ read sources organised by argument; establishes priors on magnitudes and known data problems; ends with a genuine gap |
| **Data and provenance** | 10 | Full provenance; missingness confronted rather than concealed; survey design respected |
| **Method** | 20 | Derived, not cited. Assumptions stated. Choice of method defended against the obvious alternative |
| **Results and honest evaluation** | 20 | Uncertainty reported; named benchmark; evaluation design matching the data's dependence structure; no leakage |
| **Implementation note** | 15 | An SDAfrique student could follow it in R without contacting you. The MRE runs |
| **Writing, references, statements** | 10 | Clear prose; consistent references; CRediT and LLM statements complete and specific |

### What earns credit that students do not expect

- **A method that fails to transfer, diagnosed precisely.** Full marks are available for a negative
  result. They are not available for a negative result you did not investigate.
- **A limitation you found yourself** before a referee could.
- **An implementation note that reports what went wrong** rather than presenting a frictionless path.
- **A refusal to make a causal claim** where the design cannot support one.

### What loses marks reliably

- Citing a method without deriving it.
- A literature review that is a list of summaries rather than an argument.
- Preprocessing outside the cross-validation loop.
- A result with no benchmark.
- Prose written for a marker rather than for the reader named in §1.
- An unverified citation. Check every one.

---

## 10. The oral examination

**15 minutes, one student at a time, no documents.**

The paper is written by three people. The oral is where the course establishes what **each** of
them understands. It is not a presentation and there are no slides — you sit down and answer
questions.

### What is examined

Two things, roughly half the time each:

1. **The methods used in your paper.** Why that estimator and not the obvious alternative. What
   the assumptions are. What would break the result. Where the uncertainty comes from and what it
   covers.
2. **The course content.** Anything from Sessions 02 to 11. Derive something on paper if asked.

### What this is designed to catch

> A paper can be written by a team in which one person did the modelling, one wrote the prose and
> one watched. The paper cannot tell me which. Fifteen minutes can.

It is also the reason the individual multiplier does **not** apply here: the oral already measures
the individual directly, so there is nothing to correct for.

### Questions you should expect

- *Derive the estimator you used. You may use the board.*
- *Your paper reports X. What would have to be true about the data for that to be wrong?*
- *You chose method A over method B. Defend that against someone who prefers B.*
- *Where in your paper is a claim your design cannot support? There is usually one.*
- *Explain [some result from Session 0N] and why it mattered for your paper — or why it did not.*

### How it is marked

| | What earns full marks |
|---|---|
| **Command of your own method** | Derives it, states the assumptions, knows what breaks it |
| **Command of the course** | Connects your paper to the methods you did not use, and says why |
| **Honesty under pressure** | Concedes precisely what cannot be claimed, and says how you would find out |

> **Saying "I do not know" costs you very little.** Defending an indefensible claim costs you a
> great deal. That has been true in every lab this term and it is true here.

### Practical

- Scheduled in the two weeks after the paper deadline; slots circulated in advance.
- Bring nothing. Your paper is in front of the examiner.
- Conducted in English or French, your choice — state it when you book.

---

## 11. Timeline and submission

| When | What |
|---|---|
| **After Session 7** | Teams formed (three authors; they need not be your lab group). Registered with the instructor. |
| **After Session 8** | One-page proposal: question, data sources with links, method, why it matters locally. Approved before you proceed. |
| **After Session 10** | Literature review draft — the sources and the argument, not yet polished prose. Formative feedback returned. |
| **Session 12 week** | Full draft optional, for comment. Take this up; it is free. |
| **Two weeks after Session 12** | **Final submission** of the paper. |
| **The two weeks following** | **Oral examinations**, 15 minutes per student. |

**Submit:** the paper as PDF, and the repository as a link or archive. The repository must run from
a clean clone. If it does not run, the analysis component cannot be marked.

Late: 10% per day to a maximum of three days.

---

## A closing note

Most graduate papers are read once, by one person, who is paid to read them.

This one has a chance of being read by someone who needs it — a student in Cotonou, Dakar or
Yaoundé, working on a problem in her own community, with a method she does not yet know and tools
that are not yours. That is a rare thing to be handed in a course, and it changes what "good"
means. Good is no longer "correct and complete". Good is **usable**.

Write it for her.

---

*Related: [syllabus](../../SYLLABUS.md) · [research mandates](../../RESEARCH-MANDATES.md) ·
[SDAfrique](https://sdafrique.org)*
