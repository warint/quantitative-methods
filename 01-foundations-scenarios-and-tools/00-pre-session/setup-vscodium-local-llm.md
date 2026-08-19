# Setup guide — VS Codium + Python + a local LLM

**MATH60033A · complete this before Session 01 · budget 60–90 minutes**

> Session 1 does **not** include installation time. Arrive with all five checks passing.

---

## Why this stack

Three deliberate choices, each with a pedagogical reason.

| Choice | Reason |
|---|---|
| **VS Codium** rather than VS Code | Same editor, telemetry removed, no proprietary licence. Your work in this course involves confidential and licensed data; the tooling should not exfiltrate it. |
| **A local LLM** rather than a hosted one | Your data never leave your machine. You also learn what a model can do *without* a frontier system behind it — which is the realistic constraint in most institutions. |
| **Plain Python + git** rather than a notebook platform | Reproducibility is a graded outcome. A repository with commits is auditable; a notebook state is not. |

This is also the first substantive lesson of the course: **tooling is a governance decision**, and
you should be able to defend yours.

---

## Step 1 — VS Codium

Download for your platform from **<https://vscodium.com/>** and install.

**macOS (Homebrew):**
```bash
brew install --cask vscodium
```

**Windows (winget):**
```powershell
winget install VSCodium.VSCodium
```

**Linux (Debian/Ubuntu):** follow the repository instructions at <https://vscodium.com/#install>.

> **Note.** VS Codium uses the Open VSX marketplace, not Microsoft's. Almost everything we need is
> there. Where it is not, the guide below gives an alternative.

---

## Step 2 — Extensions

Open the Extensions panel (`Ctrl/Cmd+Shift+X`) and install:

| Extension | Publisher | Purpose |
|---|---|---|
| **Python** | ms-python | Language support, environments, debugging |
| **Jupyter** | ms-toolsai | Run cells inside `.py` files with `# %%` |
| **Continue** | Continue | The LLM interface — chat and inline edit |
| **Markdown Preview Enhanced** | shd101wyy | Renders the LaTeX in the lecture notes |
| **Even Better TOML** | tamasfe | Config files |
| **GitLens** *(optional)* | GitKraken | Commit history at a glance |

If the Microsoft Python extension is unavailable in Open VSX on your platform, install **Pylance
alternative: `ms-python.python` from the `.vsix` release**, or use **`charliermarsh.ruff` +
`ms-pyright`**. Either is sufficient.

---

## Step 3 — Python environment

We use Python 3.11 or 3.12.

```bash
# from the repository root
python3 -m venv .venv

# activate
source .venv/bin/activate          # macOS / Linux
.venv\Scripts\activate             # Windows PowerShell

python -m pip install --upgrade pip
pip install -r requirements.txt
```

In VS Codium: `Ctrl/Cmd+Shift+P` → **Python: Select Interpreter** → choose `.venv`.

> **Rule for the whole course:** one virtual environment, committed `requirements.txt`, never
> `pip install` outside the environment. If your results do not reproduce from a clean clone plus
> `pip install -r requirements.txt`, they do not reproduce.

---

## Step 4 — The local LLM

We use **Ollama**, which runs models entirely on your machine.

### Install

**macOS / Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** download the installer from <https://ollama.com/download>.

### Pull a model

Choose according to your hardware. Check first:

```bash
# rough guide: you need model size + ~2 GB of free RAM (or VRAM)
```

| Your machine | Recommended model | Command |
|---|---|---|
| 8 GB RAM | `qwen2.5-coder:3b` | `ollama pull qwen2.5-coder:3b` |
| 16 GB RAM | `qwen2.5-coder:7b` | `ollama pull qwen2.5-coder:7b` |
| 32 GB+ RAM / Apple Silicon M-series | `qwen2.5-coder:14b` | `ollama pull qwen2.5-coder:14b` |

Alternatives that work well: `llama3.1:8b`, `mistral-nemo`, `deepseek-coder-v2:16b`.
Any coding-capable model is fine — the course does not depend on a specific one.

You will also want an **embedding model** for Session 10:

```bash
ollama pull nomic-embed-text
```

### Verify

```bash
ollama list
ollama run qwen2.5-coder:7b "Explain the bias-variance tradeoff in three sentences."
```

Type `/bye` to exit.

---

## Step 5 — Connect Continue to Ollama

Open the Continue panel in VS Codium, then edit its config file
(`~/.continue/config.yaml`, or `~/.continue/config.json` on older versions):

```yaml
name: MATH60033A
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

Replace the model name with whichever you pulled.

**Test it.** Open any `.py` file, select a few lines, press `Ctrl/Cmd+L`, and ask
*"what does this do?"*. Then — the important test — **turn off your wifi and ask again.** If it
still answers, your setup is genuinely local.

---

## Step 6 — Run the verification script

From the repository root, with your environment activated:

```bash
python 01-foundations-scenarios-and-tools/00-pre-session/verify_environment.py
```

You should see five green checks. **Bring the output to class** (a screenshot or a paste into your
notes is fine).

If a check fails, the script prints what to do. If you are still stuck, ask your local LLM —
that is itself a useful test of whether it is working.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ollama: command not found` | Not on PATH | Restart the terminal; on macOS check `/usr/local/bin` |
| Continue answers nothing | Ollama server not running | `ollama serve` in a separate terminal |
| Model is extremely slow | Model too large for RAM | Pull a smaller variant |
| `ModuleNotFoundError` inside VS Codium | Wrong interpreter selected | `Ctrl/Cmd+Shift+P` → Python: Select Interpreter → `.venv` |
| LaTeX shows as raw `$...$` | Preview extension missing | Install Markdown Preview Enhanced; open with `Ctrl/Cmd+K V` |
| Apple Silicon: slow inference | Rosetta Python | Install the arm64 build of Python |

---

## What "using the LLM well" means in this course

The local model is a **sparring partner**, not an oracle. Three habits, applied from Session 1:

1. **Ask it to argue against you.** Its most useful output is an objection you had not considered.
2. **Verify every factual claim.** It will state plausible falsehoods with complete confidence,
   especially about library APIs, statistical results, and citations.
3. **Record what you checked.** Every lab deliverable in this course requires at least one
   documented instance where you caught the model being wrong or unverifiable. This is graded.

You are never penalised for using the model. You are penalised for using it uncritically.

---

[Back to pre-session](README.md) · [Session 01 overview](../README.md)
