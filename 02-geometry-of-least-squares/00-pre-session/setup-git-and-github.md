# Setup guide — Git, GitHub, and working as a group

**MATH60033A · complete this before Session 02 · budget 45 minutes**

> This follows on from the [Session 01 setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md).
> You should already have VS Codium, a working Python environment, and Ollama serving a local
> model. If any of those is missing, fix it first — everything below assumes a working workstation.

Slides for this material: [`slides-github-and-teamwork.qmd`](slides-github-and-teamwork.qmd).

---

## Why this is a separate step

Session 01 got you a machine that works. This gets you a machine that works **with two other
people**, which is a different problem.

From Session 02 onward you are assessed as a group. The course checks that a group mark reflects
what each member did, and one of the four records it uses is your commit history. That record is
only as good as the identity attached to it, which is why the very first thing below is telling git
who you are.

See [`GROUP-ASSESSMENT.md`](../../GROUP-ASSESSMENT.md) for the full policy.

---

## Step 1 — Install Git

Download it from <https://git-scm.com/downloads> and accept every default. macOS may already have
it; the next step tells you.

All commands below go in the **VS Codium integrated terminal** (``View → Terminal``, or
``Ctrl+` ``), not the macOS Terminal app. The integrated terminal opens in your project folder and
sees the virtual environment you activated.

---

## Step 2 — Your identity

```bash
git --version
git config --global user.name  "Your Full Name"
git config --global user.email "your.name@hec.ca"
```

> **⚠️ Use your real name and your university email.** Your commit history is one of the four
> records this course uses to check that all three members of a group did the work. Commits under
> `unknown@localhost` cannot be attributed to you, and unattributed work counts as work you did not
> do.

Check what you set, and **report both values to the instructor in Session 02**:

```bash
git config --global user.name
git config --global user.email
```

If your git email differs from the one on the roster, the contribution report will show you as
having done nothing. Ten seconds to prevent, tedious to repair afterwards.

---

## Step 3 — A GitHub account

1. Go to <https://github.com> and choose **Sign up**.
2. Use an email you will still have after you graduate.
3. Choose a username you would put on a CV — this is a professional record.
4. Verify the email GitHub sends you.
5. Enable **two-factor authentication** when prompted. GitHub requires it.

Free accounts include unlimited private repositories.

---

## Step 4 — Your group repository

**One person per group** creates it. On github.com: **+** → **New repository**.

| Field | Value |
|---|---|
| Repository name | `qmib-gXX` — XX is your group number |
| Description | `Group work` |
| Visibility | **Private** |
| Initialize with README | ✅ |

Then **Settings → Collaborators → Add people**, and add:

- your two teammates
- the instructor

> **⚠️ A private repository the instructor cannot see is one that cannot be marked.** Do this in
> the same sitting. It is the step groups most often forget.

---

## Step 5 — Clone it

Copy the **HTTPS** URL from the green **Code** button, then:

```bash
git clone https://github.com/OWNER/qmib-gXX.git
cd qmib-gXX
```

`File → Open Folder…` and choose that folder. The Explorer should show `README.md`, and the
bottom-left of the window should show the branch `main`.

### Authenticating

On your first push GitHub asks for credentials and **rejects your account password**. It wants a
personal access token:

1. github.com → your avatar → **Settings**
2. **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token**, tick the **`repo`** scope, set an expiry
4. Copy it — **it is shown once**
5. Paste it when git asks for your *password*

```bash
git config --global credential.helper store
```

stores it so you are asked only once.

---

## Step 6 — The round trip

```bash
echo "## Group XX" >> README.md
git add README.md
git commit -m "Add group heading"
git push
```

Refresh the repository page in your browser. Your line is there.

Edit locally → commit → push → visible to your group. Everything this term is a variation on that
loop.

**Each of the three of you does this at least once, from your own machine.** Not one per group.

---

## Working together

### Pull before you start

```bash
git pull
```

Most merge conflicts are caused by somebody editing a stale copy of a file for two hours.

### Work on a branch

```bash
git checkout -b s02-fwl-analysis
# ... work, commit ...
git push -u origin s02-fwl-analysis
```

Then open a **pull request** so a teammate reads the change before it joins `main`. That review is
the group work, not an obstacle to it.

### Reading a conflict

Git marks the disagreement in the file rather than guessing:

```
<<<<<<< HEAD
alpha = 0.05
=======
alpha = 0.01
>>>>>>> their-branch
```

Delete the markers, keep the version you agree on, then `git add` and `git commit`.

### Commit messages

`git commit -m "update"` tells nobody anything. Write for the person reading it in six weeks —
usually you:

```
Fix leakage: move scaler inside the CV pipeline
```

### Credit your pair

```bash
git commit -m "Add stability bootstrap

Co-authored-by: Partner Name <partner.name@hec.ca>"
```

The contribution report counts co-authors. Use it — one person typing does not mean one person
working, and the record should say so.

### aider and your history

aider commits automatically after each change it applies, and this course counts commits as
evidence of who did the work.

```bash
git log --oneline
aider --model ollama_chat/qwen2.5-coder:7b --no-auto-commits
```

Commits made by the agent are attributed to **you**. That is correct — you directed it. But read
the diff before accepting: you are answerable for every line in your repository.

---

## Roles

Your group logs a Driver, an Analyst and a Reporter each session:

- **Driver** writes the code
- **Analyst** decides the specification, checks results, owns the interpretation
- **Reporter** writes the three sentences and presents *if drawn*

Over ten sessions each member should hold each role three or four times. Logged in
`assessment/role-logs/gXX.md`, checked with `python scripts/assess.py roles`.

The presenter is **drawn at random** at the start of the slot. A group where one person understands
the model has not learned the material; the draw makes shared understanding the only viable
strategy.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `git: command not found` | Not on PATH | Reopen the terminal; on Windows restart VS Codium |
| Password rejected on push | GitHub wants a token | Use a personal access token, not your password |
| `rejected — non-fast-forward` | Someone pushed first | `git pull`, resolve, then push |
| Committed under the wrong email | `user.email` unset or wrong | Fix `git config`, tell the instructor; past commits stay wrong |
| Conflict markers in a file | Two people edited the same lines | Delete them, keep the agreed version, add and commit |

---

## Before Session 02

- [ ] Git installed; `user.name` and `user.email` set to your real details
- [ ] GitHub account with two-factor authentication
- [ ] One **private** group repository, with both teammates **and the instructor** added
- [ ] Cloned to your machine and opened in VS Codium
- [ ] One commit pushed **by you personally**, visible on github.com
- [ ] Your exact `user.name` and `user.email` written down to report in class

---

[Session 02 overview](../README.md) · [Session 01 setup guide](../../01-foundations-scenarios-and-tools/00-pre-session/setup-vscodium-local-llm.md)
