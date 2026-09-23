# Why these tools

The toolchain for this course is a text editor without telemetry, a language
model that runs on your own laptop, and a version control system. Every one of
them is open source, and none of them requires an account, a subscription or a
network connection to work. That is not frugality. Each choice teaches
something the alternative would obscure, and the reasons are worth stating
before you spend ninety minutes installing them.

## VS Codium, rather than VS Code

Visual Studio Code is developed in the open, under a permissive licence. The
build Microsoft distributes is not the same artefact: the binary adds telemetry
and ships under a proprietary licence, and its extension marketplace is a
Microsoft service with terms of its own. VS Codium is the identical source,
compiled without the telemetry and the branding.

The practical reason for preferring it is that in this course you will open
data you do not own. The teaching data are public, but the habit is not about
these data — it is about the working file you will one day open under a
non-disclosure agreement or a research ethics protocol. An editor that reports
usage to a third party is a decision you should make deliberately, once, rather
than by default.

The larger reason is that it makes visible something students consistently
underestimate: how much of the commercial software estate is open source
underneath. This is not a marginal phenomenon. The servers that host almost
every service you use run Linux. Every Android phone runs a Linux kernel. Every
browser you are likely to open is built on Chromium or WebKit, both open source.
SQLite — public domain, maintained by three people — is embedded in essentially
every phone, browser and operating system in the world. The scientific stack
this course runs on, Python and NumPy and pandas and scikit-learn and
statsmodels, is open source without exception, and the commercial data science
platforms sold at considerable expense are, in large part, packaging around
exactly those libraries.

The point for a business student is not ideological. It is that the capability
you are buying when you buy a platform is frequently available directly, that
the difference in price is buying convenience and support rather than
capability, and that knowing which is which is a procurement skill.

## Qwen 2.5 Coder, running locally

The model you install is Chinese, developed by Alibaba. It is worth being
direct about that, because the reflex is to treat provenance as the security
question, and here it is not.

What matters is that the weights are open and the model runs on your machine.
An open-weight model downloaded to your laptop and run offline cannot send your
data anywhere; it has no network connection to send it over. A closed model
behind an API, wherever the company is domiciled, receives everything you type
by construction. On the dimension people actually care about — does my work
leave this room — local open weights are the stronger guarantee, and the
nationality of the developer does not enter into it. You can verify this claim
rather than trust it: disconnect from the network and watch the model keep
working.

This is also your first encounter with a distinction the course returns to.
Qwen 2.5 Coder is a *vertical* model: specialised for code, and consequently
far better at code, for its size, than a general assistant many times larger.
A three-billion-parameter model on a laptop is not competitive with a frontier
system at open-ended reasoning. At completing a pandas idiom it is entirely
adequate. Choosing a small specialised model over a large general one — and
knowing which tasks admit that trade — is the applied judgement that separates
a sensible AI deployment from an expensive one, and it is the same judgement
that chapter 5 will make about a deliberately biased estimator.

The course installs the 3-billion variant rather than the 7, and the reason is
worth stating because it is the same reasoning in miniature. Most student
laptops have no dedicated graphics card, so the model runs on the processor. On
a processor the 7B is not a better model: it produces a comparable answer to the
same question at roughly a quarter of the speed, and a tool slow enough to
interrupt your thinking is a tool you stop using. The binding constraint is not
quality, it is whether you will actually reach for it.

The standing rule of the course applies to it from the first day: every
deliverable must document at least one instance where you identified a model
output as wrong, unverifiable or misleading, and explain how you established
that. You are never penalised for using the model. You are penalised for using
it uncritically.

## Two ways of using it, deliberately

The same model is reached through two different tools, and the split is not
redundancy.

**Continue** puts the model in the editor. You select code and ask about it, and
the answer arrives beside the file. This is the mode that matters most in a
course where you will read far more code than you write — the session decks, the
authors' replication packages, your group's scripts. The friction of copying
code into a browser is small, and it is enough to stop most people asking.

**aider** puts the model in the terminal, inside your repository, where it can
change files and commit what it changed. That is a different kind of act, and
the course treats it as one. You see every command it proposes before it runs,
and whatever it writes is committed under your name — which is the point, since
the commit history is one of the records used to check that all three members of
a group did the work. Delegating the typing does not delegate the answerability.

The honest limitation, stated once: on a machine without a graphics card, a
small model is a capable reader and an unreliable editor. It will explain a
function correctly and then fail to produce a well-formed multi-file edit,
because emitting a precise diff is a harder task than describing code. That is
a fact about small models rather than about you, and the practical response is
to use aider for understanding and do the editing yourself — which is, in any
case, the position the course would prefer you were in.

## git

git is the least glamorous item on the list and the one most likely to matter
to your career.

Its immediate function is to make your work reproducible. This book takes the
position that a result which does not reproduce from a clean clone is not a
result — and that standard is empty without a mechanism. git is the mechanism.
It records what the analysis was at the moment the number was produced, so that
"we got 1,111" becomes a claim someone can check rather than one they must
accept.

Its second function is provenance under disagreement. In group work, the log
answers questions that memory cannot: who changed the specification, when, and
what the estimate was before. That is why the individual multiplier on group
work is gated on the git history rather than on assertion. It is not
surveillance; it is the same reason laboratory notebooks are dated.

Its third function is that it is how the rest of the field works. The
replication packages you will download are distributed as repositories. The
libraries you rely on develop in public, and their issue trackers are often the
only accurate documentation of a bug you have just hit. Being able to read a
diff, open an issue and submit a fix is a professional literacy, and the
distance between using open source and contributing to it is one commit.

You will not become fluent in git this term. You need four commands — `clone`,
`add`, `commit`, `push` — and the understanding that a commit is a checkpoint
you can return to. The rest can wait.

## What they have in common

Open source, no account required, and everything running on hardware you
control. It means the whole course works with no internet in the room, that
nothing you do is contingent on a vendor's pricing decision, and that every
result in this book can be reproduced by anyone, on a modest machine, without
paying for the privilege.

That last property is not a convenience. It is what makes the work checkable,
and checkability is the only thing that separates quantitative analysis from
assertion with numbers in it.
