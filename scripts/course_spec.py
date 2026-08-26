"""The course, as data.

Sessions 02 to 11 were re-mapped onto the published warin.ca lecture sequence.
Nine sessions' READMEs, pre-sessions and practice briefs still described the
previous curriculum, which is how a repository ends up contradicting itself.

This module is the single description of what each session teaches. The root
README, SYLLABUS.md and the per-session pages are generated from it, so they
cannot drift apart again.

    python scripts/build_course_pages.py
"""

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
        methods="mean/median/trimmed, variance, IQR, skewness, kurtosis, simple and multiple regression",
        theme="Which summary of your key variable would you defend in print?",
        generated=False,          # pages written by hand; decks still generated
        objectives=[
            "Compute the **mean, median and trimmed mean**, and say which question each answers",
            "Explain why the sample variance divides by $n-1$",
            "Apply the **empirical rule**, and state the precondition that makes it valid",
            "Compute **skewness** and **excess kurtosis**, and test each against its threshold",
            "Fit a simple regression and state the slope **in units**",
        ],
        dataset="core",
        dataset_note="the course spine — thirty European countries, 2010–2024",
        deliverable=("a profile of your project's three key variables — centre, spread and shape, "
                     "thresholds tested — and the summary you would defend in print"),
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
        methods="residual diagnostics, leverage, Cook's distance, information criteria",
        theme="Which model would survive a referee?",
        objectives=[
            "Read a **residuals-versus-fitted** plot and say what structure it reveals",
            "Diagnose non-constant variance from a **scale–location** plot",
            "Compute **leverage** and say which observations have the power to move the line",
            "Use **Cook's distance** to separate an outlier from an influential point",
            "Compare candidate models on **AIC**, and say why that is not model selection",
        ],
        dataset="core",
        dataset_note="the same regression Session 02 fitted — GDP per capita on productivity",
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
            "Compare nested models with a **likelihood-ratio test**",
            "Extend the model to **ordinal** and **multinomial** outcomes, and say what each assumes",
        ],
        dataset="loans",
        dataset_note="Lending Club — 9,578 three-year loans, FICO scores and default",
        deliverable=("a logistic model of a binary outcome in your own project data, with the "
                     "odds ratios interpreted in words, one nested comparison tested, and a note "
                     "on what the model does not license you to say"),
        loses_marks=[
            "Reporting log-odds as though they were probabilities",
            "Interpreting an odds ratio as a relative risk",
            "Comparing non-nested models with a likelihood-ratio test",
            "Reporting accuracy on an imbalanced outcome with no base rate",
        ],
    ),
    "05": dict(
        dir="05-ridge-lasso-elastic-net",
        title="Regularisation: Ridge, Lasso, and the Elastic Net",
        short="Regularisation",
        question="When is a deliberately biased estimator the better one?",
        methods="soft-thresholding, coordinate descent, the grouping effect",
        theme="Of many indicators, which few actually carry the signal?",
        generated=False,          # repository-native pages; decks still generated
        objectives=[
            "State the ridge and lasso objectives and say **what each penalty buys**",
            "Explain why ridge shrinkage is **targeted** rather than blunt",
            "Derive **soft-thresholding** and use it to explain the lasso's exact zeros",
            "Choose between lasso and elastic net from the **correlation structure**",
            "Report $\\lambda$ by cross-validation, and know why post-selection inference is invalid",
        ],
        dataset="core",
        dataset_note="a wide slice of the spine — more candidate indicators than usable rows",
        deliverable=("a penalised fit on your own angle: the path, the chosen $\\lambda$, what "
                     "survived, and what that does not license you to claim"),
        loses_marks=[
            "Penalising unstandardised predictors",
            "Standardising before the cross-validation split",
            "Reporting the selected set as \"the variables that matter\"",
            "Reporting post-selection p-values with no caveat",
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
        dataset="movies",
        dataset_note="45,000 films — budget, popularity, revenue, runtime and votes",
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
        dataset="core",
        dataset_note="the course spine, plus the Smarket returns used in the lecture",
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
        dataset="core",
        dataset_note="the spine's documented treatment, with a known effect to recover",
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
        dataset="core",
        dataset_note="the spine's post-2021 structural break, treated as a policy change",
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
        short="Final group presentations",
        question="Can you make a decision-maker act on this — and say what would change your mind?",
        methods="—",
        theme="—",
        generated=False,
    ),
}

MIDTERM_AFTER = "06"


def ordered():
    return [(k, SESSIONS[k]) for k in sorted(SESSIONS)]


def generated():
    return [(k, v) for k, v in ordered() if v.get("generated", True)]
