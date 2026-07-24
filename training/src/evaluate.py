"""Small, repeatable helpers for selecting and recording model thresholds."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def classification_metrics(y_true, probabilities, threshold: float) -> dict[str, float]:
    """Return metrics for one explicit probability threshold."""
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between 0 and 1")

    predicted = (pd.Series(probabilities) >= threshold).astype(int)
    return {
        "threshold": threshold,
        "auc": float(roc_auc_score(y_true, probabilities)),
        "accuracy": float(accuracy_score(y_true, predicted)),
        "precision": float(precision_score(y_true, predicted, zero_division=0)),
        "recall": float(recall_score(y_true, predicted, zero_division=0)),
        "f1": float(f1_score(y_true, predicted, zero_division=0)),
    }
