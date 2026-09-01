# Setup guide — Git, GitHub, and how you submit work

**complete this before Session 02 · budget 45 minutes**

> Follows on from the [Session 01 setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).
> You should already have VS Codium, a Python environment, and Ollama serving a local model.

---

## ⚠️ `XX` is a placeholder — replace it

Wherever you see **`XX`** in a command on this page, or anywhere else in the course, it means
**your group's two-digit number**. Type your own; do not type the letters `XX`.

| If you are | you type |
|---|---|
| Group 1 | `group-01` |
| Group 7 | `group-07` |
| Group 10 | `group-10` |

So a student in **group 7** running the branch command types:

```bash
git checkout group-07
```

not `git checkout group-XX`. Same for folder paths:
`02-practice/submissions/group-07/`.

If you do not know your group number yet, you get it in Session 01. Do not guess.

---

## How submission works — read this first

There is **one repository for the whole course**, and you already have a copy of it as a ZIP from
Session 01. You are about to replace that snapshot with a real clone.

```
github.com/warint/quantitative-methods        ← the course repository
│
├── main                    ← the instructor's branch. You never push to it.
├── group-01                ← group 01 works here
├── group-02                ← group 02 works here
└── group-XX                ← your group works here
```

**Your group has one branch, named `group-XX`.** Everything your group produces is committed on
that branch and pushed to it. Your practice deliverables go in the session folder:

```
NN-session-name/02-practice/submissions/group-XX/
```

**Why one repository and not one per group.** Your commit history is one of the four records used
to check that all three of you did the work, and `scripts/assess.py contributions` reads it from
this repository. Work pushed somewhere else is invisible to it — and invisible work counts as work
you did not do.

**You do not need to create a repository.** You need an account, and the instructor adds you.

---

## Step 1 — Install Git

**Check first — you may already have it.** In the VS Codium terminal:

```bash
git --version
```

If that prints a version number, git is installed and you are done with this step.

**macOS.** Git ships with Apple's Command Line Tools, so most Macs already have it. If the command
above is not found, macOS will offer to install the tools itself — accept — or run:

```bash
xcode-select --install
```

You do **not** need Homebrew for this course.

**Windows.** Download from <https://git-scm.com/downloads> and accept every default. Restart VS
Codium afterwards so the new `PATH` is picked up.

**Linux.** `sudo apt install git`, or your distribution's equivalent.

All commands below go in the **VS Codium integrated terminal** (``View → Terminal``, or
``Ctrl+` ``), never the macOS Terminal app.

---

## Step 2 — Your identity

```bash
git --version
git config --global user.name  "Your Full Name"
git config --global user.email "your.name@hec.ca"
```

> **⚠️ Use your real name and your university email.** Commits under `unknown@localhost`, or under
> an email not on the roster, cannot be attributed to you. The contribution report will show you as
> having done nothing.

Check what you set, and **report both values to the instructor in Session 02**:

```bash
git config --global user.name
git config --global user.email
```

---

## Step 3 — A GitHub account

1. Go to <https://github.com> and choose **Sign up**.
2. Use an email you will still have after you graduate.
3. Choose a username you would put on a CV.
4. Verify the email GitHub sends you.
5. Enable **two-factor authentication** when prompted. GitHub requires it.

**Then send your GitHub username to the instructor.** You cannot push until you have been added as
a collaborator, and that is done by hand from the list of usernames.

---

## Step 4 — Clone the course repository

This replaces the Session 01 ZIP. Delete the unzipped folder afterwards so you do not edit the
wrong copy.

```bash
cd ~/Desktop                         # macOS / Linux
git clone https://github.com/warint/quantitative-methods.git quantitative-methods
cd quantitative-methods
```

On Windows PowerShell, use `Set-Location "$HOME\Desktop"` for the first line. Then
`File → Open Folder…` and choose the `quantitative-methods` folder on your Desktop.

Rebuild your environment inside the clone:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Authenticating

On your first push GitHub rejects your account password and asks for a token:

1. github.com → avatar → **Settings**
2. **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token**, tick the **`repo`** scope, set an expiry
4. Copy it — **it is shown once** — and paste it when git asks for your *password*

```bash
git config --global credential.helper store
```

stores it so you are asked once.

---

## Step 5 — Your group branch

**One person per group** creates it; the others just check it out.

```bash
# the first person, once   — group 7 shown; use your own number
git checkout -b group-07
git push -u origin group-07
```

```bash
# everyone else, after that
git fetch origin
git checkout group-07
```

> **⚠️ Never `git push` while on `main`.** `main` is protected, so the push will be refused rather
> than cause damage — but check where you are before you commit:
>
> ```bash
> git branch --show-current
> ```

---

## Step 6 — The round trip

```bash
# group 7 shown throughout — substitute your own number everywhere
mkdir -p 02-exploratory-data-analysis/02-practice/submissions/group-07
echo "# Group 07 — session 02" > 02-exploratory-data-analysis/02-practice/submissions/group-07/NOTES.md

git add 02-exploratory-data-analysis/02-practice/submissions/group-07/
git commit -m "Add group 07 notes for session 02"
git push
```

Refresh the repository page in your browser, switch to your group's branch, and your file is
there.

**Each of the three of you does this at least once, from your own machine.** Not one per group.

---

## If your group of three is already formed — do a trial run now

Groups are confirmed in Session 04, but if the three of you have already agreed to work together,
you can rehearse the whole cycle before class. It takes ten minutes and it removes the one thing
that reliably eats practice time: discovering in the room that two of you cannot push.

**One person, once.** Create the branch and push it:

```bash
git checkout -b group-07              # your number, not 07
git push -u origin group-07
```

**The other two, after that.** Fetch it and switch to it:

```bash
git fetch origin
git checkout group-07
```

**Then each of you, one at a time**, adds a line with your own name and pushes:

```bash
git pull                              # always pull before you start
echo "- Ana tested the push, 2 September" >> \
  02-exploratory-data-analysis/02-practice/submissions/group-07/NOTES.md

git add 02-exploratory-data-analysis/02-practice/submissions/group-07/NOTES.md
git commit -m "Ana: trial push"
git push
```

Wait for each person to finish before the next starts. When all three are done:

```bash
git pull
git log --oneline -5
```

> **You should see three commits, with three different author names.** That is exactly what the
> participation record looks like, and confirming it now is worth more than any amount of reading
> about git.

If someone's push is rejected, they almost certainly need to `git pull` first — someone else pushed
in between. That is normal, not a fault; see [Working together](#working-together) below.

---

## Working together

### Pull before you start

```bash
git pull
```

Most conflicts come from someone editing a stale copy for two hours.

### Getting the instructor's corrections

The course material lives on `main` and gets fixed during the term. To bring those fixes into your
branch:

```bash
git fetch origin
git merge origin/main
```

Do this at the start of each session.

### Reading a conflict

```
<<<<<<< HEAD
alpha = 0.05
=======
alpha = 0.01
>>>>>>> origin/main
```

Delete the markers, keep the version you agree on, then `git add` and `git commit`. A conflict is
git refusing to guess which of you was right.

### Commit messages

`git commit -m "update"` tells nobody anything. Write for whoever reads it in six weeks — usually
you:

```
Fix leakage: move scaler inside the CV pipeline
```

### Credit your pair

```bash
git commit -m "Add stability bootstrap

Co-authored-by: Partner Name <partner.name@hec.ca>"
```

The contribution report counts co-authors. One person typing does not mean one person working.

### aider and your history

aider commits automatically after each change it applies, and this course counts commits as
evidence of who did the work.

```bash
git log --oneline
aider --model ollama_chat/qwen2.5-coder:7b --no-auto-commits
```

What the agent writes is attributed to **you**. Read the diff before accepting: you are answerable
for every line on your branch.

---

## Everyone pushes

There are **no assigned roles**. All three of you work on the practice together — and all three commit
and push from your own machine, every week.

```bash
git add -A && git commit -m "..." && git push
```

`python scripts/assess.py contributions` prints a per-member, per-week grid built from the history.
A week in which you pushed nothing is visible to everyone, including you.

The presenter for the two-minute report is **drawn at random** when your group is called, which is
why all three of you must understand the whole analysis.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `git: command not found` | Reopen the terminal; on Windows restart VS Codium |
| Password rejected on push | Use a personal access token, not your password |
| `remote: Permission denied` | You have not been added as a collaborator yet — send your username |
| `protected branch` on push | You are on `main`. Check out your group branch |
| `rejected — non-fast-forward` | `git pull` first, resolve, then push |
| Committed under the wrong email | Fix `git config`, tell the instructor; past commits stay wrong |

---

## Before Session 02

- [ ] Git installed; `user.name` and `user.email` set to your real details
- [ ] GitHub account with two-factor authentication
- [ ] **GitHub username sent to the instructor**
- [ ] Course repository cloned; the Session 01 ZIP folder deleted
- [ ] Your `group-NN` branch checked out — your own number, not `XX`
- [ ] One commit pushed **by you personally** to your group branch, visible on github.com
- [ ] Your exact `user.name` and `user.email` written down to report

---

## For the instructor

Once the usernames are in:

1. **Settings → Collaborators → Add people** — add every student with **Write** access.
2. **Settings → Branches → Add branch protection rule** for `main`: require a pull request, and
   tick *"Do not allow bypassing"* off for yourself. Students then cannot push to `main`.
3. Group branches need no protection — a group breaking its own branch is recoverable.
4. To review a group's work:

```bash
git fetch origin
git checkout group-07
python scripts/assess.py contributions
```

`contributions` reads the history of whatever is checked out, so run it after fetching all
branches:

```bash
git fetch --all
python scripts/assess.py contributions
```

---

[Session 02 overview](../README.md) · [Session 01 setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md)
