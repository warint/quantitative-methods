# Setup checklist — VS Codium, Python, and a local LLM

**complete before Session 01 · budget 60–90 minutes**

> **The walkthrough is the slide deck**, `MATH60033A-S01-Pre-Session.pptx` in this folder. Work
> through that. This page is the checklist you scan afterwards, plus the troubleshooting table.
> If the two ever disagree, the deck is right.

---

## Why this stack

| Choice | Reason |
|---|---|
| **VS Codium** rather than VS Code | Same editor, telemetry removed. Your work involves confidential and licensed data; the tooling should not exfiltrate it. |
| **A local LLM** rather than a hosted one | Your data never leave your machine. You also learn what is achievable *without* a frontier system — the realistic institutional constraint. |
| **Plain Python + git** rather than a notebook platform | Reproducibility is graded. A commit history is auditable; a notebook's execution state is not. |

Tooling is a governance decision, and you should be able to defend yours. That is the first
substantive lesson of the course.

---

## The checklist

Everything typed goes in the **VS Codium integrated terminal** (``View → Terminal``, or
``Ctrl+` ``) — never the macOS Terminal app.

- [ ] **VS Codium** installed from <https://vscodium.com> and it opens
- [ ] **Extensions** installed: Python (`ms-python.python`), Jupyter (`ms-toolsai.jupyter`), Continue (`Continue.continue`)
- [ ] **Course materials** downloaded — *Code → Download ZIP* from <https://github.com/warint/quantitative-methods>, unzipped **directly on your Desktop** as `quantitative-methods`, and opened with `File → Open Folder…`
- [ ] **Python 3.12 specifically** — not "the latest" — from <https://www.python.org/downloads/release/python-31214/>; on Windows tick *"Add python.exe to PATH"*. `aider-chat` requires Python `<3.13`, so 3.13 and 3.14 cannot run this course's toolchain
- [ ] `python3.12 --version` prints 3.12.x — on Windows `py -3.12 --version`, and `py --list` shows every Python you have. Build the environment with the version named (`py -3.12 -m venv .venv`, `python3.12 -m venv .venv`), because a bare `py` or `python3` picks the newest one installed
- [ ] `.venv` created and activated — your prompt shows `(.venv)`
- [ ] `pip install -r requirements.txt` completed without red text
- [ ] `python -c "import numpy, pandas, sklearn; print('ok')"` prints `ok`
- [ ] **Ollama** installed from <https://ollama.com/download>; `ollama --version` works
- [ ] A model pulled: `qwen2.5-coder:3b` (8 GB RAM), `:7b` (16 GB), or `:14b` (32 GB+)
- [ ] `ollama pull nomic-embed-text` — needed in Session 09
- [ ] **The wifi test:** turn wifi off, run `ollama run qwen2.5-coder:7b "hello"`. It still answers.
- [ ] **aider** installed **outside** the course environment, via pipx — `python3 -m pip install --user pipx`, `python3 -m pipx ensurepath`, new terminal, `pipx install aider-chat` (`py` for `python3` on Windows) — never `pip install aider-chat` into `.venv`. `aider --version` answers in a new terminal
- [ ] `verify_environment.py` shows five passing checks, and you have the output to bring

Git and GitHub are **not** part of Session 01. They are set up before Session 02:
[`setup-git-and-github.md`](../../02-exploratory-data-analysis/00-pre-session/setup-git-and-github.md).

---

## Connecting Continue to Ollama

Continue's config lives at `~/.continue/config.yaml`:

```yaml
name: qmib
version: 0.0.1
models:
  - name: Local coder
    provider: ollama
    model: qwen2.5-coder:7b
    roles: [chat, edit, apply]
  - name: Local embedder
    provider: ollama
    model: nomic-embed-text
    roles: [embed]
context:
  - provider: file
  - provider: code
  - provider: diff
  - provider: terminal
```

Replace the model name with whichever you pulled. Test it: open a `.py` file, select a few lines,
press `Ctrl/Cmd+L`.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ollama: command not found` | Not on PATH yet | Open a new terminal; on Windows restart VS Codium |
| Dependency resolver errors while installing aider | It was installed into `.venv`, where it competes with the course's packages | Install it with pipx instead — see the checklist above |
| Dependency conflicts installing aider, or a build error naming a compiler | Your Python is 3.13 or newer; aider requires `<3.13` | Give aider a 3.12 of its own: `pipx install --python python3.12 aider-chat` |
| `pipx` or `aider` *n'est pas reconnu* / *not recognized* | `pip install --user` writes scripts to a folder Windows does not have on PATH | `py -m pipx …` works regardless; `py -m pipx ensurepath` plus a new terminal fixes PATH itself |
| A newly installed extension or command does nothing | The window or terminal predates the install | *Developer: Reload Window*; for PATH changes, quit VS Codium and reopen |
| `Python introuvable` / `Python was not found` (Windows) | The Microsoft Store alias is shadowing Python | Start → **Manage app execution aliases** → turn **off** `python.exe` and `python3.exe`, then open a new terminal. Do not install from the Store. |
| `python3: command not found` (Windows) | There is no `python3` on Windows | Use `py`. If that is missing too, re-run the python.org installer with **Add python.exe to PATH** ticked |
| Continue answers nothing | Server not running | `ollama serve` in a separate terminal |
| Model extremely slow | Too large for your RAM | Pull a smaller variant (`:3b`) |
| aider "forgets" the file you gave it | Ollama's 2k default context | Set `OLLAMA_CONTEXT_LENGTH=8192` for the **system** and restart Ollama — `launchctl setenv` on macOS, `setx` on Windows, `systemctl edit ollama.service` on Linux |
| `address already in use`, or *une seule utilisation de chaque adresse de socket* | Ollama is already running; the installer starts it on every platform | Do not run `ollama serve`. Set the variable, then restart Ollama itself |
| `connection refused` from aider | Nothing listening on 11434 | Start Ollama — the app on macOS and Windows, `sudo systemctl start ollama` on Linux |
| `ModuleNotFoundError` inside VS Codium | Wrong interpreter | `Ctrl/Cmd+Shift+P` → *Python: Select Interpreter* → `.venv` |
| `pip` fails | Environment not active | Check `(.venv)` is in your prompt |
| Windows: *l'exécution de scripts est désactivée sur ce système* | PowerShell's execution policy blocks `Activate.ps1` | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` — user-scoped, no admin rights, asked once |
| Windows: *le répertoire n'est pas vide* when deleting `.venv` | VS Codium holds the interpreter it has selected | Quit VS Codium; delete from a plain PowerShell; `cmd /c "rmdir /s /q .venv"` as a last resort |
| `deactivate` is not recognised | Activation defines it, so it exists only inside an active environment | You are not in one. Skip it — the prompt shows `(.venv)` when you are |
| LaTeX shows as raw `$...$` | Preview extension missing | Install *Markdown Preview Enhanced*; open with `Ctrl/Cmd+K V` |
| Apple Silicon: slow inference | Rosetta Python | Install the arm64 build |

---

## Rendering the mathematics

The lecture notes use LaTeX. GitHub renders `$...$` and `$$...$$` natively. In VS Codium, install
**Markdown+Math** or **Markdown Preview Enhanced** and open the preview with `Ctrl/Cmd+K V`.

---

## Using the LLM well

The local model is a **sparring partner**, not an oracle.

1. **Ask it to argue against you.** Its most useful output is an objection you had not considered.
2. **Verify every factual claim.** It states plausible falsehoods with complete confidence,
   especially about library APIs, statistical results and citations.
3. **Record what you checked.** Every practice deliverable requires at least one documented instance
   where you caught the model being wrong or unverifiable. This is graded.

You are never penalised for using the model. You are penalised for using it uncritically.

---

[Back to pre-session](README.md) · [Session 01 overview](../README.md)
