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
- [ ] **Python 3.11 or 3.12** from <https://www.python.org/downloads/> — on Windows, *"Add python.exe to PATH"* ticked
- [ ] `python3 --version` prints 3.11.x or 3.12.x
- [ ] `.venv` created and activated — your prompt shows `(.venv)`
- [ ] `pip install -r requirements.txt` completed without red text
- [ ] `python -c "import numpy, pandas, sklearn; print('ok')"` prints `ok`
- [ ] **Ollama** installed from <https://ollama.com/download>; `ollama --version` works
- [ ] A model pulled: `qwen2.5-coder:3b` (8 GB RAM), `:7b` (16 GB), or `:14b` (32 GB+)
- [ ] `ollama pull nomic-embed-text` — needed in Session 09
- [ ] **The wifi test:** turn wifi off, run `ollama run qwen2.5-coder:7b "hello"`. It still answers.
- [ ] **aider** installed and talking to Ollama — `OLLAMA_CONTEXT_LENGTH=8192 ollama serve` in one terminal, `aider --model ollama_chat/qwen2.5-coder:7b` in another
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
| `python3: command not found` (Windows) | PATH box not ticked | Try `python`; if still missing, re-run the installer |
| Continue answers nothing | Server not running | `ollama serve` in a separate terminal |
| Model extremely slow | Too large for your RAM | Pull a smaller variant (`:3b`) |
| aider "forgets" the file you gave it | Ollama's 2k default context | Start it as `OLLAMA_CONTEXT_LENGTH=8192 ollama serve` |
| `connection refused` from aider | `ollama serve` not running | Start it, leave that terminal open |
| `ModuleNotFoundError` inside VS Codium | Wrong interpreter | `Ctrl/Cmd+Shift+P` → *Python: Select Interpreter* → `.venv` |
| `pip` fails | Environment not active | Check `(.venv)` is in your prompt |
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
