"""The course, as data.

Sessions 02 to 11 were re-mapped onto the published warin.ca lecture sequence.
Nine sessions' READMEs, pre-sessions and practice briefs still described the
previous curriculum, which is how a repository ends up contradicting itself.

This module is the single description of what each session teaches. The root
README, SYLLABUS.md and the per-session pages are generated from it, so they
cannot drift apart again.

    python scripts/build_course_pages.py
"""

# The cohort folder under groups/. Autumn 2026; a winter term would be H2026.
# Every submission path in the generated pages is built from this, so changing
# it here moves the whole course's group work to a new directory.
COHORT = "A2026"

# The QMIB Lab App: the optional at-home knowledge check that is the third
# route to participation marks. Live since September 2026; the course pages
# said "the link is announced in class" until then.
LAB_URL = "https://warin.ca/qmib-labs/"
# One lab per session, sessions 02 to 11. Session 01 installs the workstation
# and session 12 is the presentations, so neither has one.
LAB_SESSIONS = tuple(f"{n:02d}" for n in range(2, 12))


def lab_url(num):
    """The lab for one session, or None where there is no lab."""
    return f"{LAB_URL}qmib-lab-{num}.html" if num in LAB_SESSIONS else None

# Harvard Dataverse puts a guestbook on some deposits, and a guestbook cannot
# be answered from the terminal: the access API returns HTTP 400 whatever you
# send it. Those sessions get this note instead of a broken curl recipe.
GUESTBOOK_NOTE = (
    "This deposit sits behind a Dataverse **guestbook**, so the `curl` recipe above returns an "
    "error for this session. Open the DOI in a browser, click **Access Dataset -> Download ZIP**, "
    "accept the terms once, and unzip it to the same folder. Everything after that is identical."
)

SESSIONS = {
    "01": dict(
        dir="01-foundations-scenarios-and-tools",
        title="Foundations: Scenarios, Tools, and the Syllabus",
        short="Syllabus and Europe 2031",
        question="Before we model the future, what are we claiming to know?",
        methods="the syllabus, the toolchain, and a conversation",
        theme="*(no practice; a discussion of Europe 2031 and what AI is)*",
        generated=False,          # session 01 is hand-written; leave it alone
    ),
    "02": dict(
        dir="02-exploratory-data-analysis",
        title="Exploratory Data Analysis, and the First Model",
        short="Exploratory data analysis",
        question="Before you model anything, what does the data actually look like?",
        methods="mean/median/trimmed, variance, IQR, skewness, kurtosis, the empirical rule",
        theme="Which summary of your key variable would you defend in print?",
        generated=False,          # pages written by hand; decks still generated
        objectives=[
            "Compute the **mean, median and trimmed mean**, and say which question each answers",
            "Explain why the sample variance divides by $n-1$",
            "Apply the **empirical rule**, and state the precondition that makes it valid",
            "Compute **skewness** and **excess kurtosis**, and test each against its threshold",
            "Say which summary you would defend in print, and why the other two mislead",
        ],
        reading="Fraiberger et al. (2021), *Media sentiment and international asset prices*",
        reading_url="https://doi.org/10.1016/j.jinteco.2021.103526",
        dataverse="10.7910/DVN/QNKFJF",
        dataset="core",
        dataset_note="the course spine — thirty European countries, 2010–2024",
        deliverable=("a profile of your project's three key variables — centre, spread and shape, "
                     "thresholds tested — and the summary you would defend in print"),
        pre_session_extra="git",   # Session 02 is where the group repository is set up
        loses_marks=[
            "`df.describe()` pasted with no interpretation",
            "A skewness reported without its threshold",
            "Calling a variable normal because it is symmetric",
            "Applying the empirical rule to a variable you have shown to be skewed",
        ],
    ),
    "03": dict(
        dir="03-regression-adequacy-and-validity",
        title="Regression: Adequacy, Validity, and Robustness",
        short="Regression diagnostics",
        question="You have fitted a regression. Can it be trusted?",
        methods="least squares, residual diagnostics, influence and Cook's distance, information criteria",
        theme="Which model would survive a referee?",
        objectives=[
            "Fit a simple and a multiple regression, and state the slope **in units**",
            "Read a **residuals-versus-fitted** plot and say what structure it reveals",
            "Diagnose non-constant variance from a **scale–location** plot",
            "Tell an outlier, a **leverage point** and an **influential point** apart",
            "Use **Cook's distance** to find the observations that move the answer",
            "Compare candidate models on **AIC and BIC**, and say why that is not model selection",
        ],
        reading="Amsili, van Es & Schindelbeck (2024), *Pedotransfer Functions for Field Capacity, Permanent Wilting Point, and Available Water Capacity*",
        reading_url="https://doi.org/10.1080/00103624.2024.2336573",
        dataverse="10.7910/DVN/U5DAEP",
        data_extra=(
            "This deposit is **about 220 MB** — much the largest in the course. Start the download "
            "before you sit down to read, not while the room is waiting for you."
        ),
        dataset="core",
        dataset_note="the regression fitted at the top of the lecture — GDP per capita on productivity",
        practice_extra="regtable",   # the practice ends with two models to compare
        deliverable=("a diagnostic report on your group's own regression: four plots, the "
                     "observations you investigated, and a 250-word note on which conclusions "
                     "survived the diagnostics and which did not"),
        loses_marks=[
            "Reporting $R^2$ without a single diagnostic plot",
            "Deleting an influential point without saying what it was",
            "Reading a residual plot as \"looks fine\" with no statement of what you looked for",
            "Choosing a model on AIC and reporting it as though the data selected it",
        ],
    ),
    "04": dict(
        dir="04-logistic-ordinal-multinomial",
        title="Logistic Regression: Binary, Ordinal, and Multinomial",
        short="Logistic regression",
        question="The outcome is a category, not a number. Now what?",
        methods="maximum likelihood, odds ratios, pseudo-$R^2$, likelihood-ratio tests",
        theme="Can we predict a discrete outcome honestly?",
        objectives=[
            "Say why the **linear probability model** fails, and where it fails worst",
            "Interpret a logistic coefficient as a **log-odds**, and its exponential as an odds ratio",
            "Compute a fitted probability by hand from $x^\\top\\hat\\beta$",
            "Extend the model to **ordinal** and **multinomial** outcomes, and say what each assumes",
        ],
        reading="Saganowski et al. (2019), *Analysis of group evolution prediction in complex networks*",
        reading_url="https://doi.org/10.1371/journal.pone.0224194",
        dataverse="10.7910/DVN/ONOFS7",
        dataset="loans",
        dataset_note="Lending Club — 9,578 three-year loans, FICO scores and default",
        practice_extra="regtable",   # two logits side by side, before and after the broken assumption
        deliverable=("a logistic model of a binary outcome in your own project data, with the "
                     "odds ratios interpreted in words, and a note on what the model does not "
                     "license you to say"),
        loses_marks=[
            "Reporting log-odds as though they were probabilities",
            "Interpreting an odds ratio as a relative risk",
            "Reporting accuracy on an imbalanced outcome with no base rate",
        ],
    ),
    "05": dict(
        dir="05-ridge-lasso-elastic-net",
        title="Regularisation: Ridge, Lasso, and the Elastic Net",
        short="Regularisation",
        question="When is a deliberately biased estimator the better one?",
        methods="stepwise selection and why it fails, soft-thresholding, coordinate descent, the grouping effect",
        theme="Of many indicators, which few actually carry the signal?",
        generated=False,          # repository-native pages; decks still generated
        objectives=[
            "Say why a greedy **stepwise** search is unstable, and what that instability argues for",
            "State the ridge and lasso objectives and say **what each penalty buys**",
            "Explain why ridge shrinkage is **targeted** rather than blunt",
            "Derive **soft-thresholding** and use it to explain the lasso's exact zeros",
            "Choose between lasso and elastic net from the **correlation structure**",
            "Report $\\lambda$ by cross-validation, and know why post-selection inference is invalid",
        ],
        reading="Blonigen & Piger (2014), *Determinants of foreign direct investment*, Canadian Journal of Economics 47(3)",
        reading_url="https://doi.org/10.1111/caje.12091",
        dataverse=None,           # no package published; rebuilt by scripts/build_fdi_determinants.py
        dataset="fdi",
        dataset_note=("56 candidate determinants of bilateral FDI, 2019 — the paper's design "
                      "rebuilt from OECD, CEPII, World Bank and Freedom House"),
        deliverable=("a penalised fit on your own angle: the path, the chosen $\\lambda$, what "
                     "survived, and what that does not license you to claim"),
        loses_marks=[
            "Penalising unstandardised predictors",
            "Standardising before the cross-validation split",
            "Reporting the selected set as \"the variables that matter\"",
            "Reporting post-selection p-values with no caveat",
            "Presenting a stepwise selection as though the data had chosen it",
            "Reading a dropped variable as evidence of no effect",
        ],
    ),
    "06": dict(
        dir="06-advanced-regression",
        title="Regression: Advanced Considerations",
        short="Panel data and interactions",
        question="Does the relationship hold across countries, and across years?",
        methods="panel data, fixed and random effects, non-linearity, interactions",
        theme="Does your finding survive the structure of your data?",
        objectives=[
            "State what a **panel** is, and why pooling it with OLS understates uncertainty",
            "Distinguish **fixed** from **random** effects, and say what each assumes",
            "Fit a quadratic term and interpret a **non-linear** relationship in units",
            "Read an **interaction** as a slope that differs between groups",
            "Compare non-nested models on information criteria rather than an F-test",
        ],
        reading="Topalova & Khandelwal (2011), *Trade Liberalization and Firm Productivity*",
        reading_url="https://doi.org/10.1162/REST_a_00095",
        dataverse="10.7910/DVN/8WEXYD",
        dataset="panel",
        dataset_note="a country panel of government debt and economic-freedom indices",
        deliverable=("a panel specification of your project's core relationship, fitted with both "
                     "fixed and random effects, plus a 250-word note on which you would report "
                     "and why"),
        loses_marks=[
            "Pooling a panel with ordinary standard errors",
            "Choosing fixed or random effects because one gave the significant answer",
            "Reporting an interaction without stating the slope in each group",
            "Adding a quadratic term and interpreting only its coefficient",
        ],
    ),
    "07": dict(
        dir="07-pca-and-factor-analysis",
        title="Principal Component and Factor Analyses",
        short="PCA and factor analysis",
        question="How many independent things are actually being measured?",
        methods="eigenvalues, loadings, scree plots, rotation, FAMD",
        theme="How many distinct dimensions does your angle really have?",
        objectives=[
            "Explain why PCA requires **standardised** inputs, and what happens if you forget",
            "Read a **scree plot** and defend the number of components you retained",
            "Distinguish a **loading** from a **score**, and say what each is for",
            "State the difference between **PCA** and **factor analysis**, and when each applies",
            "Say why a factor is identified only **up to rotation**",
        ],
        reading=("Gygli, Haelg, Potrafke & Sturm (2019), *The KOF Globalisation Index — revisited*, "
                 "Review of International Organizations 14(3)"),
        reading_url="https://doi.org/10.1007/s11558-019-09344-2",
        dataverse=None,           # the index itself is the data, published by KOF ETH Zurich
        dataset="kof",
        dataset_note=("the KOF Globalisation Index — 180 countries, 1970–2023, six sub-dimensions "
                      "each split into de facto and de jure"),
        deliverable=("a dimension-reduction of your project's indicators: the scree plot, the "
                     "number retained with its justification, the loadings interpreted, and a "
                     "note on what you are *not* entitled to call the components"),
        loses_marks=[
            "Running PCA on unstandardised columns",
            "Retaining components by a rule you did not state",
            "Naming a component (\"this is competitiveness\") with no rotation caveat",
            "Reporting variance explained as though it measured correctness",
        ],
    ),
    "08": dict(
        dir="08-knn-and-bias-variance",
        title="K-Nearest Neighbours and the Bias–Variance Trade-off",
        short="KNN and bias–variance",
        question="Flexible, or just unstable?",
        methods="the Bayes classifier, distance, choosing $k$ by cross-validation",
        theme="Does flexibility buy you anything on your own data?",
        objectives=[
            "State the **Bayes classifier** and say why no rule can beat it",
            "Compute a Euclidean distance and find nearest neighbours **by hand**",
            "Explain why KNN requires **standardised** predictors",
            "Choose $k$ by cross-validation, and read the trade-off the curve shows",
            "Say what happens to KNN as the number of predictors grows",
        ],
        reading=("Bluwstein, Buckmann, Joseph, Kapadia & Şimşek (2023), *Credit growth, the yield "
                 "curve and financial crisis prediction: evidence from a machine learning approach*, "
                 "Journal of International Economics 145"),
        reading_url="https://doi.org/10.1016/j.jinteco.2023.103773",
        dataverse=None,           # built on the public Macrohistory database
        dataset="jst",
        dataset_note=("the Jordà–Schularick–Taylor Macrohistory Database — 18 economies, 1870–2020, "
                      "88 financial crises, with the paper's predictors already derived"),
        deliverable=("a KNN classifier on a binary outcome from your angle, with $k$ chosen by "
                     "cross-validation, compared against a sensible benchmark, and a note on "
                     "whether the flexibility earned its keep"),
        loses_marks=[
            "Running KNN on unstandardised predictors",
            "Choosing $k$ on the test set",
            "Reporting accuracy with no benchmark",
            "Treating a low training error as evidence of anything",
        ],
    ),
    "09": dict(
        dir="09-structural-equation-modelling",
        title="Structural Equation Modelling",
        short="Structural equation modelling",
        question="Can you measure something you cannot observe?",
        methods="measurement and structural models, latent variables, fit indices",
        theme="What is the construct behind your indicators?",
        objectives=[
            "Distinguish the **measurement** model from the **structural** model",
            "Write a model description and read `=~` as \"is measured by\"",
            "Interpret a **standardised loading**, and say when an indicator is weak",
            "Report **CFI, TLI and RMSEA**, and say what each would have to be",
            "State why good fit is not evidence that the model is correct",
        ],
        reading="Bennani & Romelli (2024), *Exploring the informativeness and drivers of tone during committee meetings*",
        reading_url="https://doi.org/10.1016/j.jimonfin.2024.103161",
        dataverse="10.7910/DVN/TZEN38",
        dataset="efa",
        dataset_note="a 14-item questionnaire on purchase decisions, plus semopy's bundled examples",
        deliverable=("a measurement model for one construct in your project, with the loadings "
                     "reported, the fit indices stated, and a note on the indicators you would "
                     "drop and why"),
        loses_marks=[
            "Reporting fit indices without saying which threshold you applied",
            "Treating good fit as confirmation of the causal structure",
            "Adding correlated residuals until the model fits",
            "Naming a latent variable without defending the name",
        ],
    ),
    "10": dict(
        dir="10-causal-inference-foundations",
        title="Causal Inference I: Counterfactuals, Randomisation, Matching",
        short="Causal inference (1/2)",
        question="Did the policy do anything, or were the groups different to begin with?",
        methods="potential outcomes, randomisation, propensity scores, matching",
        theme="Can your project support a causal claim at all?",
        objectives=[
            "State the **fundamental problem of causal inference**",
            "Explain why **randomisation** solves it, and what it costs",
            "Estimate a **propensity score** and use it to match treated to control units",
            "Check **overlap** and **balance**, and say what to do when they fail",
            "Report an **ATT**, and state the assumption it rests on",
        ],
        reading=("Atkin, Khandelwal & Osman (2017), *Exporting and Firm Performance: Evidence from a "
                 "Randomized Experiment*, Quarterly Journal of Economics 132(2)"),
        reading_url="https://doi.org/10.1093/qje/qjx002",
        dataverse="10.7910/DVN/QOGMVI",
        data_extra=GUESTBOOK_NOTE,
        dataset="core",
        dataset_note="the spine's documented treatment, with a known effect to recover",
        practice_extra="regtable",   # an outcome model before and after matching
        deliverable=("a matched comparison on your own data: the naive difference, the overlap "
                     "check, the balance table, the matched estimate, and the paragraph defending "
                     "conditional ignorability — that paragraph carries the marks"),
        loses_marks=[
            "Reporting a matched estimate with no overlap diagnostic",
            "Matching on a variable affected by the treatment",
            "Calling an association causal because you controlled for something",
            "Omitting the balance table",
        ],
    ),
    "11": dict(
        dir="11-causal-inference-did",
        title="Causal Inference II: Difference-in-Differences",
        short="Causal inference (2/2)",
        question="What would have happened otherwise?",
        methods="parallel trends, the interaction as the estimate, instrumental variables",
        theme="What is your counterfactual, and would anyone believe it?",
        objectives=[
            "Set up a **difference-in-differences** design and identify the four cells",
            "Read the **interaction coefficient** as the estimate",
            "State the **parallel-trends** assumption and how you would probe it",
            "Explain what an **instrument** must satisfy, and why good ones are rare",
            "Say what neither design can rescue",
        ],
        reading=("Cavallo, Gopinath, Neiman & Tang (2021), *Tariff Passthrough at the Border and at "
                 "the Store: Evidence from US Trade Policy*, American Economic Review: Insights 3(1)"),
        reading_url="https://doi.org/10.1257/aeri.20190536",
        dataverse="10.7910/DVN/JV7FCH",
        data_extra=GUESTBOOK_NOTE,
        dataset="core",
        dataset_note="the spine's post-2021 structural break, treated as a policy change",
        practice_extra="regtable",   # two DiD specifications side by side
        deliverable=("a difference-in-differences estimate on your angle, with the parallel-trends "
                     "evidence shown rather than asserted, and a note on the threat you consider "
                     "most serious"),
        loses_marks=[
            "A DiD with no evidence on parallel trends",
            "Reading the post-treatment dummy as the effect",
            "An instrument justified only by its first stage",
            "Claiming a causal effect the design cannot deliver",
        ],
    ),
    "12": dict(
        dir="12-group-presentations",
        title="Final Group Presentations",
        short="Final group presentations, and the closing address",
        question="Can you make a decision-maker act on this — and say what would change your mind?",
        methods="Closing address: what the twelve weeks established",
        theme="—",
        generated=False,
    ),
}

# The timetable, as published. Wednesdays 15:30–18:30, Décelles — Victoriaville,
# except where noted. Two Wednesdays have no class: 30 September and 21 October.
# The midterm is written on 28 October.
WHEN = "Wednesdays 15:30–18:30"
ROOM = "Décelles — Victoriaville"

DATES = {
    "01": "2026-08-26",
    "02": "2026-09-02",
    "03": "2026-09-09",
    "04": "2026-09-16",
    "05": "2026-09-23",
    "06": "2026-10-07",   # asynchronous
    "07": "2026-10-14",
    "08": "2026-11-04",
    "09": "2026-11-11",
    "10": "2026-11-18",
    "11": "2026-11-25",
    "12": "2026-12-02",
}

ASYNCHRONOUS = {"06"}

NO_CLASS = ["2026-09-30", "2026-10-21"]

# The midterm sits after Session 07 in the calendar but examines Sessions 1–6:
# Session 07 is taught before it and is not on the paper.
MIDTERM_DATE = "2026-10-28"
MIDTERM_ROOM = "room to be announced"

ORAL_EXAM = "Monday 14 December 2026 (to be confirmed)"

MIDTERM_AFTER = "07"   # written 28 Oct; examines everything taught before it


def ordered():
    return [(k, SESSIONS[k]) for k in sorted(SESSIONS)]


def generated():
    return [(k, v) for k, v in ordered() if v.get("generated", True)]
