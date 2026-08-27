---
title: "Introduction"
standalone: true
---

## The question underneath every method

When can a number about the past be used to make a claim about the future?

Every technique in this book is an answer to some version of that question, and
every one of them arrives with conditions attached. The conditions are the
subject. Anyone can run a regression; the software will not stop you, and it
will return coefficients to four decimal places whatever you feed it. What
distinguishes work worth acting on is the ability to say what would have to be
true for the number to mean what you want it to mean — and to notice when that
stops being the case.

This is harder than it sounds, because the failure is silent. A misspecified
model does not raise an error. A confidence interval computed from the wrong
formula looks exactly like one computed from the right formula. A coefficient
driven entirely by three observations is printed in the same typeface as one
supported by four hundred. The whole apparatus of diagnostics exists because
the arithmetic is indifferent to whether it is being used sensibly.

George Box put the useful version of this in a sentence that has been quoted
into meaninglessness: all models are wrong, but some are useful
[@box1976]. The half that gets repeated is the first. The half that matters is
the second, and the word doing the work in it is *some* — the claim is not that
usefulness is guaranteed but that it must be established, case by case, for a
stated purpose. "Useful for what?" is the question this book keeps returning
to, because a model that answers one question well is frequently worthless for
the question next to it.

## Three questions that look alike

Most confusion in applied quantitative work comes from running together three
things that are genuinely different. They use overlapping machinery, which is
why they get conflated, and they license completely different statements.

::: {.definition}
[**Description**]{.term} — what is in this data? Summaries, distributions,
correlations, visualisations. Description makes no claim beyond the sample. It
is the least glamorous of the three and the one most often skipped, which is
why so many analyses discover in week six a problem visible in a scatterplot in
week one.
:::

::: {.definition}
[**Prediction**]{.term} — given what I have seen, what will the next
observation look like? A predictive model is judged on out-of-sample accuracy
and by nothing else. It does not need to be interpretable, its coefficients
need not correspond to anything real, and a variable can earn its place purely
by being correlated with something that matters.
:::

::: {.definition}
[**Causal inference**]{.term} — if I intervene, what changes? This asks about a
world that does not exist: the same units, under a different policy. No amount
of data on the world as it is answers it automatically, because the comparison
required was never observed.
:::

The distinction between the second and the third is where careers and policies
go wrong. A model can predict superbly and be useless for choosing an action.
The standard example is a hospital model that predicts pneumonia patients with
asthma have *lower* mortality risk — true in the data, because asthmatic
patients were admitted directly to intensive care. As a prediction about the
observed system it is correct. As a basis for deciding whom to send home it
would kill people. The correlation is real; the intervention it appears to
recommend inverts the mechanism that produced it.

Leo Breiman's essay on the two cultures of statistical modelling is the classic
statement of how differently these communities think — one assuming a
data-generating model and interpreting its parameters, the other treating the
mechanism as unknown and optimising predictive accuracy [@breiman2001]. Both
cultures are represented in this book. Chapters 2 through 6 are largely the
first; chapters 7 and 8 are largely the second; chapters 11 and 12 are about
the third question, which neither culture answers on its own.

The credibility of empirical work in economics improved substantially once the
profession took the third question seriously as a design problem rather than an
estimation problem — the shift Angrist and Pischke call the credibility
revolution [@angrist2010]. Its lesson generalises well beyond economics: what
makes a causal claim believable is usually a feature of *how the comparison was
constructed*, not of how sophisticated the estimator was.

## Why international business is a hard case

The methods in this book are general. The setting is not, and the setting makes
particular trouble.

Start with the unit of analysis. Public discussion of trade is conducted in
country aggregates — a deficit with one country, a surplus with another — but
countries do not trade. Firms do [@warin-firms]. A bilateral flow is the sum of
decisions taken inside firms under constraints that the aggregate cannot
display: freight, insurance, policy wedges, the cost and risk of switching a
supplier [@warin-gravity]. Analysis conducted at the level where the decision
was not made will attribute to nations what happened in supply chains.

Then the observations are not independent, and this is not a technicality. The
data in this book are European countries observed annually. Germany in one year
and Germany in the next are not two independent draws from anything; countries
share shocks, policies and business cycles. Chapter 3 shows what this does to a
standard error — roughly a 74% understatement in the running example — and it
is the kind of error that makes a marginal finding look decisive.

The system also reorganises itself while you study it. Concentration that
nobody had measured becomes visible only under stress: Ukraine supplied around
seventy per cent of the world's neon, Russia some forty-four per cent of its
palladium, Taiwan close to two-thirds of its semiconductors, and firms learned
the shape of their own dependencies by watching them break
[@warin-supplychains]. And the deeper shift now under way is not digitisation
but a pivot from producing goods toward valuing the data generated in the
course of producing them, which changes where advantage accumulates and which
institutions can capture it [@warin-middlepowers].

Finally, the received account is not neutral. The claim that global value
chains are efficient — having been optimised for decades, how could they not be
— functions as an assumption rather than a finding, and it survives largely
because it is so rarely tested against data [@warin-notefficient]. Received
narratives fill gaps where measurement is absent. That is precisely the space
quantitative methods exist to occupy.

## What a model is, and what it is not

A model is a formal statement of what you believe about how the data arose. It
is not a summary of the data, and the difference matters. A summary cannot be
wrong — the mean is the mean. A model can be wrong, and its being falsifiable
is the whole of its value.

Every model has three parts, and confusion about which part is failing accounts
for most bad diagnosis:

1. **A structural claim** — the shape of the relationship. That income depends
   on productivity linearly, say. Get this wrong and your estimates are biased:
   the coefficient is answering a question you did not ask.
2. **A stochastic claim** — how the unexplained part behaves. Constant variance,
   independence, sometimes normality. Get this wrong and your estimates are
   generally *fine* while your uncertainty is not: the right number with the
   wrong error bar.
3. **A claim about scope** — the population and conditions under which the first
   two hold. This is the part written down least often and violated most.

Three of the twelve chapters are essentially about the first claim, three about
the second, and the running theme of all twelve is the third. The scope
condition is where "the model fits well" quietly becomes "the model applies
here", and nothing in the output flags the transition.

## How the book is organised

Twelve chapters, following an arc from describing data to defending a causal
claim.

**Chapters 2 to 6 build a model and test it.** Exploratory analysis and the
first regression; then the diagnostics that decide whether a fitted regression
can be trusted at all; then outcomes that are categories rather than numbers;
then regularisation, which asks when a deliberately biased estimator is the
better one; then what changes when the data have both a country and a time
dimension.

**Chapters 7 to 9 look for structure nobody labelled.** Principal component and
factor analysis, on how many independent things are actually being measured;
nearest neighbours and the bias–variance trade-off, on whether a flexible method
is genuinely flexible or merely unstable; structural equation modelling, on
whether something unobservable can be measured at all.

**Chapters 10 and 11 confront the question the first nine cannot answer** —
whether anything caused anything. Counterfactuals, randomisation and matching
first; then difference-in-differences, which asks what would have happened
otherwise and answers it with an assumption you must state and defend.

**Chapter 12** is about making a decision-maker act on the result, and saying
what would change your mind.

Each chapter takes a single question as its title question, derives the method
rather than asserting it, applies it to real European economic data, and ends
where a referee would begin — with what the result does not license.

## On the data, and on mess

Teaching quantitative methods in a business school pulls in two directions.
Real data are messy: missing values, structural breaks, definitional changes,
countries that join a series halfway through. Data constructed for teaching are
clean and therefore false, and they train an intuition that fails on contact
with anything real [@warin-statcan].

This book resolves the tension toward the mess, and does it in a specific way
that you need to understand before reading a single result.

The data used throughout are **teaching fixtures**, not observations. They are
generated from a known latent structure, and they carry the schema, the country
and year coverage, the observation flags, the missingness patterns and the
structural breaks of the real European sources they stand in for. What they do
not carry is the values. Poland does not have the GDP per capita this book
prints for it.

That is a deliberate trade, and it buys two things. Every method behaves as it
would on the real series — the missingness is awkward in the same places, the
panel structure bites in the same way, the influential observations are
influential for the same reasons — while the ground truth is known, so a
diagnostic can be checked against what actually generated the data. And nobody
is tempted to cite a course exercise as a finding about Europe.

::: {.warn}
**Do not cite any number in this book as a fact about Europe.** The tables in
`data/spine/` are fixtures. `scripts/build_spine/build.py` replaces them with
live Eurostat, Comtrade and ECB data, at which point every figure in the book
re-renders against the real thing — and the numbers change.
:::

The awkwardness is left in, because handling it *is* the skill. The influential
observation is not removed before you see it. The panel structure is not
flattened away. When a diagnostic reveals a problem in the running example —
and in chapter 3 it does, twice — the problem is reported rather than
engineered out.

::: {.step}
**A result that does not reproduce is not a result.** Every analysis in this
book runs from a clean clone of the repository it was written in, on open data,
with open tools. That is not a stylistic preference. It is the standard every
serious journal now applies, and it is the only way a reader can check you
rather than take your word.
:::

## What this book asks of you

Four habits, which are worth more than any individual technique.

**Say the units.** A coefficient without units is not a finding. "1,111" is not
an answer; "1,111 euros of GDP per capita per index point of productivity" is.

**Report the uncertainty.** A number without an interval invites a confidence
the data do not support, and the interval is frequently the more interesting
half.

**Say what the result does not license.** Every serious empirical claim has a
boundary. Stating it is not hedging; it is the part that tells a reader you
know what you did.

**Prefer a well-argued refusal to a confident answer.** "This cannot be
claimed from these data, and here is what would be needed" is a complete and
often correct result. The alternative — producing a number because a number was
requested — is how quantitative work loses its authority.

None of this makes the answers certain. It makes them *accountable*, which is
the most any empirical method offers and considerably more than the
alternatives on offer.
