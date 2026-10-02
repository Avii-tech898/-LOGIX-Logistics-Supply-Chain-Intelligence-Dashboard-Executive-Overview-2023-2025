from pathlib import Path
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"
MODEL_DIR = OUTPUT_DIR / "models_temporal"

RESULT_FILE = (
    OUTPUT_DIR /
    "temporal_delivery_delay_model_results.csv"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD
# ============================================================

X_train = joblib.load(
    MODEL_DIR / "X_train_processed.pkl"
)

X_test = joblib.load(
    MODEL_DIR / "X_test_processed.pkl"
)

y_train = joblib.load(
    MODEL_DIR / "y_train.pkl"
)

y_test = joblib.load(
    MODEL_DIR / "y_test.pkl"
)


# ============================================================
# MODELS
# ============================================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000,
            random_state=42
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42,
            max_depth=8,
            min_samples_leaf=20
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
            max_depth=12,
            min_samples_leaf=10,
        ),
}


results = []


print("=" * 70)
print("LOGIX - TEMPORAL DELIVERY DELAY MODELS")
print("=" * 70)


for name, model in models.items():

    print()
    print(f"Training: {name}")

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities
    )

    print(
        f"Accuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1        : {f1:.4f}"
    )

    print(
        f"ROC-AUC   : {roc_auc:.4f}"
    )

    results.append(
        {
            "model": name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "roc_auc": roc_auc,
        }
    )

    filename = (
        name.lower()
        .replace(" ", "_")
        + "_temporal.pkl"
    )

    joblib.dump(
        model,
        MODEL_DIR / filename
    )


# ============================================================
# RESULTS
# ============================================================

results_df = pd.DataFrame(
    results
)

results_df = results_df.sort_values(
    "roc_auc",
    ascending=False
)

results_df.to_csv(
    RESULT_FILE,
    index=False
)

print()
print("=" * 70)
print("TEMPORAL MODEL RESULTS")
print("=" * 70)

print(
    results_df.to_string(
        index=False
    )
)

print()
print(f"✓ Results saved:")
print(RESULT_FILE)

print("=" * 70)