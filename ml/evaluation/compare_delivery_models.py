from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "ml" / "outputs"


BASELINE_FILE = (
    OUTPUT_DIR /
    "delivery_delay_model_results.csv"
)

ENGINEERED_FILE = (
    OUTPUT_DIR /
    "engineered_delivery_delay_model_results.csv"
)

TEMPORAL_FILE = (
    OUTPUT_DIR /
    "temporal_delivery_delay_model_results.csv"
)

OUTPUT_FILE = (
    OUTPUT_DIR /
    "delivery_delay_model_comparison.csv"
)


frames = []


# ============================================================
# Baseline
# ============================================================

if BASELINE_FILE.exists():

    baseline = pd.read_csv(
        BASELINE_FILE
    )

    baseline["pipeline"] = (
        "Random Split - Baseline"
    )

    frames.append(baseline)


# ============================================================
# Engineered
# ============================================================

if ENGINEERED_FILE.exists():

    engineered = pd.read_csv(
        ENGINEERED_FILE
    )

    engineered["pipeline"] = (
        "Random Split - Engineered"
    )

    frames.append(engineered)


# ============================================================
# Temporal
# ============================================================

if TEMPORAL_FILE.exists():

    temporal = pd.read_csv(
        TEMPORAL_FILE
    )

    temporal["pipeline"] = (
        "Time-Based - Final"
    )

    frames.append(temporal)


# ============================================================
# Combine
# ============================================================

if not frames:

    raise FileNotFoundError(
        "No model result files found."
    )


comparison = pd.concat(
    frames,
    ignore_index=True
)


comparison = comparison[
    [
        "pipeline",
        "model",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ]
]


comparison.to_csv(
    OUTPUT_FILE,
    index=False
)


print("=" * 70)
print("LOGIX - MODEL PIPELINE COMPARISON")
print("=" * 70)

print(
    comparison.to_string(
        index=False
    )
)

print()
print(f"✓ Saved:")
print(OUTPUT_FILE)

print("=" * 70)