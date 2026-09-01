"""
environment verification.

Run this BEFORE Session 1, **with the environment activated** — the prompt
should show (.venv) first:

    python 01-foundations-scenarios-and-tools/00-pre-session/verify_environment.py

If check 0 fails, nothing below it means anything: the packages are installed
somewhere this interpreter cannot see. Activate and run it again.

All checks must pass. Bring the output to class.
"""

import importlib
import json
import platform
import sys
import urllib.error
import urllib.request

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
results = []


def report(check, status, detail=""):
    results.append((check, status, detail))
    mark = {PASS: "[ok]  ", FAIL: "[FAIL]", WARN: "[warn]"}[status]
    print(f"{mark} {check}")
    if detail:
        for line in detail.strip().splitlines():
            print(f"        {line}")


# ---------------------------------------------------------------- 1. Python
# The course runs on 3.12 and only 3.12. Everything in requirements.txt is happy
# on 3.14 — but aider-chat declares requires-python <3.13, so on anything newer
# it cannot be installed at all. Rather than run two interpreters, the course
# uses the newest one aider accepts. 3.12 is supported until October 2028.
WANT = (3, 12)


def in_venv():
    """True when this interpreter is a virtual environment's own."""
    return sys.prefix != sys.base_prefix


def check_python():
    major, minor = sys.version_info[:2]
    detail = f"{platform.python_implementation()} {platform.python_version()} on {platform.platform()}"

    # The commonest reason every package check fails is that this script is
    # being run by the system interpreter rather than the environment's — the
    # packages are installed, just not where this Python is looking. Say so
    # first, because otherwise the output blames the install.
    if not in_venv():
        report("0. Virtual environment", FAIL,
               f"Running {sys.executable}\n"
               "This is NOT the course environment, so the package checks below\n"
               "will fail even if everything installed correctly.\n"
               "Activate it first, then run this again:\n"
               "    .venv\\Scripts\\activate     (Windows)\n"
               "    source .venv/bin/activate  (macOS and Linux)\n"
               "Your prompt should show (.venv) before you re-run.")
    else:
        report("0. Virtual environment", PASS, sys.executable)
    if (major, minor) == WANT:
        report("1. Python 3.12", PASS, detail)
    elif (major, minor) > WANT:
        report("1. Python 3.12", FAIL, detail +
               f"\nThis is newer than the course uses. aider requires Python < 3.13 and"
               f"\nwill not install here. Install 3.12, then rebuild the environment"
               f"\nnaming it:  py -3.12 -m venv .venv   (Windows)"
               f"\n             python3.12 -m venv .venv  (macOS and Linux)")
    else:
        report("1. Python 3.12", FAIL, detail +
               "\nThis is older than the course uses. Install 3.12 and rebuild .venv.")


# ---------------------------------------------------------------- 2. Packages
REQUIRED = [
    ("numpy", "numerical arrays"),
    ("pandas", "data frames"),
    ("scipy", "scientific computing"),
    ("sklearn", "scikit-learn"),
    ("statsmodels", "econometrics"),
    ("matplotlib", "plotting"),
    ("pyarrow", "parquet caching"),
]
OPTIONAL = [
    ("seaborn", "plotting (S8-S10)"),
    ("shap", "model explanation (S8)"),
    ("doubleml", "causal ML reference (S11)"),
    ("econml", "causal forests (S11)"),
]


def check_packages():
    missing = []
    for mod, _ in REQUIRED:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        report("2. Required packages", FAIL,
               "Missing: " + ", ".join(missing) +
               "\nRun: pip install -r requirements.txt")
    else:
        import numpy
        import pandas
        import sklearn
        report("2. Required packages", PASS,
               f"numpy {numpy.__version__} | pandas {pandas.__version__} | scikit-learn {sklearn.__version__}")

    missing_opt = []
    for mod, why in OPTIONAL:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing_opt.append(f"{mod} ({why})")
    if missing_opt:
        report("2b. Optional packages", WARN,
               "Not installed (fine for now): " + ", ".join(missing_opt))
    else:
        report("2b. Optional packages", PASS, "all present")


# ---------------------------------------------------------------- 3. Numerics
def check_numerics():
    """A real (tiny) OLS problem — the Session 2 estimator, solved three ways."""
    try:
        import numpy as np
        rng = np.random.default_rng(60033)
        n, p = 200, 3
        X = np.column_stack([np.ones(n), rng.normal(size=(n, p))])
        beta = np.array([1.0, 2.0, -0.5, 0.25])
        y = X @ beta + rng.normal(scale=0.3, size=n)

        b_inv = np.linalg.inv(X.T @ X) @ X.T @ y          # normal equations
        b_solve = np.linalg.solve(X.T @ X, X.T @ y)        # better
        b_lstsq = np.linalg.lstsq(X, y, rcond=None)[0]     # best (QR/SVD)

        spread = max(np.abs(b_inv - b_lstsq).max(),
                     np.abs(b_solve - b_lstsq).max())
        err = np.abs(b_lstsq - beta).max()

        if spread < 1e-8 and err < 0.15:
            report("3. Linear algebra", PASS,
                   f"OLS recovered beta (max abs error {err:.4f});\n"
                   f"three solvers agree to {spread:.2e}")
        else:
            report("3. Linear algebra", FAIL,
                   f"solver spread {spread:.2e}, estimation error {err:.4f}")
    except Exception as exc:
        report("3. Linear algebra", FAIL, f"{type(exc).__name__}: {exc}")


# ---------------------------------------------------------------- 4. Plot + parquet
def check_io():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        import os
        import tempfile

        tmp = tempfile.mkdtemp()

        fig, ax = plt.subplots(figsize=(4, 2))
        ax.plot(np.linspace(0, 1, 50), np.sin(np.linspace(0, 6, 50)))
        png = os.path.join(tmp, "check.png")
        fig.savefig(png, dpi=80)
        plt.close(fig)

        df = pd.DataFrame({"a": range(5), "b": list("abcde")})
        pq = os.path.join(tmp, "check.parquet")
        df.to_parquet(pq)
        back = pd.read_parquet(pq)

        ok = os.path.getsize(png) > 0 and back.equals(df)
        report("4. Plotting and parquet I/O", PASS if ok else FAIL,
               f"wrote {os.path.getsize(png)} bytes of PNG; parquet round-trip {'ok' if back.equals(df) else 'FAILED'}")
    except Exception as exc:
        report("4. Plotting and parquet I/O", FAIL,
               f"{type(exc).__name__}: {exc}\nIf this mentions pyarrow, run: pip install pyarrow")


# ---------------------------------------------------------------- 5. Local LLM
def check_ollama():
    url = "http://localhost:11434/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=4) as resp:
            payload = json.loads(resp.read().decode())
        names = [m.get("name", "?") for m in payload.get("models", [])]
        if not names:
            report("5. Local LLM (Ollama)", FAIL,
                   "Ollama is running but no model is installed.\n"
                   "Run: ollama pull qwen2.5-coder:7b")
            return
        has_embed = any("embed" in n for n in names)
        detail = "Models available: " + ", ".join(names)
        if not has_embed:
            detail += "\nNote: no embedding model yet. Before Session 10: ollama pull nomic-embed-text"
        report("5. Local LLM (Ollama)", PASS, detail)
    except (urllib.error.URLError, OSError):
        report("5. Local LLM (Ollama)", FAIL,
               "Could not reach Ollama at localhost:11434.\n"
               "Is it installed?  https://ollama.com/download\n"
               "Is it running?    ollama serve\n"
               "See setup-vscodium-local-llm.md, step 4.")
    except Exception as exc:
        report("5. Local LLM (Ollama)", FAIL, f"{type(exc).__name__}: {exc}")


# ---------------------------------------------------------------- main
def main():
    print("=" * 68)
    print("  environment verification")
    print("=" * 68)
    print()

    check_python()
    check_packages()
    check_numerics()
    check_io()
    check_ollama()

    print()
    print("=" * 68)
    failed = [c for c, s, _ in results if s == FAIL]
    warned = [c for c, s, _ in results if s == WARN]
    if failed:
        print(f"  {len(failed)} CHECK(S) FAILED: {', '.join(failed)}")
        print("  Fix these before Session 1. See setup-vscodium-local-llm.md.")
        print("=" * 68)
        sys.exit(1)
    print("  All required checks passed." + (f"  ({len(warned)} warning)" if warned else ""))
    print("  Bring this output to Session 1.")
    print("=" * 68)


if __name__ == "__main__":
    main()
