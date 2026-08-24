"""Session 06: accuracy, ROC AUC, and a cost-based threshold."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 60033
OUT = Path(__file__).resolve().parent / "outputs"


def main() -> None:
    X, y = make_classification(n_samples=1200, n_features=10, n_informative=5, weights=[0.95, 0.05],
                               class_sep=1.1, random_state=SEED)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.35, random_state=SEED)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    model.fit(X_train, y_train)
    probability = model.predict_proba(X_test)[:, 1]
    threshold = 1 / (1 + 8)  # false negative costs eight times a false positive
    prediction = (probability >= threshold).astype(int)

    print(f"Null accuracy: {np.mean(y_test == 0):.3f}")
    print(f"Model accuracy at cost threshold: {accuracy_score(y_test, prediction):.3f}")
    print(f"ROC AUC: {roc_auc_score(y_test, probability):.3f}")
    print(f"Cost-based threshold: {threshold:.3f}")

    OUT.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(y_test, prediction, ax=ax, colorbar=False, cmap="Blues")
    ax.set_title("The threshold converts probabilities into actions")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=180)


if __name__ == "__main__":
    main()
