# Name: Qudrat Ullah | Roll No (Trainee ID): TRN-2026-000363 | Date: 2026-11-20
"""Part B: Leakage-free tabular ML pipeline, model comparison, error analysis, and CLI inference."""

import argparse
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEANED_CSV = PROJECT_ROOT / "data" / "cleaned" / "elections_cleaned.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "pipeline.joblib"
REPORTS_DIR = PROJECT_ROOT / "output" / "reports"
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"

# Strictly pre-election features (excludes Votes, vote_share_pct, Turnout N, Rejected Votes)
NUMERIC_FEATURES = ["Registered Voters", "num_candidates_in_seat"]
CATEGORICAL_FEATURES = ["Province", "Regions 5", "Zones 20", "Party", "Six Parties"]
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET_COLUMN = "is_winner"


def add_pre_election_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer leak-free pre-election features known before ballots are cast.

    Args:
        df: Cleaned elections DataFrame.

    Returns:
        Copy of df with `num_candidates_in_seat` added.
    """
    out = df.copy()
    if "num_candidates_in_seat" not in out.columns:
        out["num_candidates_in_seat"] = out.groupby(["Year", "Constituency"])[
            "Party"
        ].transform("count")
    return out


def build_preprocessor() -> ColumnTransformer:
    """Create leakage-free preprocessing ColumnTransformer for numeric and categorical features."""
    num_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    cat_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        [
            ("num", num_pipe, NUMERIC_FEATURES),
            ("cat", cat_pipe, CATEGORICAL_FEATURES),
        ]
    )


def train_and_evaluate(cleaned_path: Path = CLEANED_CSV) -> pd.DataFrame:
    """Train baseline and candidate models, compare via CV, evaluate on future test set, and save pipeline.

    Args:
        cleaned_path: Path to Part A cleaned CSV file.

    Returns:
        DataFrame comparing cross-validated metrics across models.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(cleaned_path)
    df = add_pre_election_features(df)

    # Time-based split BEFORE fitting any transformer (Train: 1970-2013 | Test: 2018-2024)
    train_df = df[df["Year"] < 2018].copy()
    test_df = df[df["Year"] >= 2018].copy()

    X_train, y_train = train_df[FEATURE_COLUMNS], train_df[TARGET_COLUMN]
    X_test, y_test = test_df[FEATURE_COLUMNS], test_df[TARGET_COLUMN]

    candidates = {
        "Baseline (Dummy Most-Frequent)": DummyClassifier(strategy="most_frequent"),
        "Logistic Regression (Balanced)": LogisticRegression(
            max_iter=1000, class_weight="balanced", random_state=42
        ),
        "Random Forest (Balanced)": RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=150, learning_rate=0.08, max_depth=4, random_state=42
        ),
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {
        "f1": "f1",
        "precision": "precision",
        "recall": "recall",
        "roc_auc": "roc_auc",
        "pr_auc": "average_precision",
    }

    comparison_rows = []
    fitted_pipelines = {}

    for name, clf in candidates.items():
        pipe = Pipeline(
            [
                ("preprocessor", build_preprocessor()),
                ("classifier", clf),
            ]
        )
        cv_scores = cross_validate(
            pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1
        )
        pipe.fit(X_train, y_train)
        fitted_pipelines[name] = pipe

        comparison_rows.append(
            {
                "Model": name,
                "CV_F1": round(float(cv_scores["test_f1"].mean()), 4),
                "CV_Precision": round(float(cv_scores["test_precision"].mean()), 4),
                "CV_Recall": round(float(cv_scores["test_recall"].mean()), 4),
                "CV_ROC_AUC": round(float(cv_scores["test_roc_auc"].mean()), 4),
                "CV_PR_AUC": round(float(cv_scores["test_pr_auc"].mean()), 4),
            }
        )

    results_df = (
        pd.DataFrame(comparison_rows)
        .sort_values("CV_PR_AUC", ascending=False)
        .reset_index(drop=True)
    )
    best_model_name = results_df.loc[0, "Model"]
    best_pipeline = fitted_pipelines[best_model_name]

    # Single final evaluation on held-out 2018-2024 test set
    y_pred = best_pipeline.predict(X_test)
    y_prob = best_pipeline.predict_proba(X_test)[:, 1]

    test_metrics = {
        "Best_Model": best_model_name,
        "Train_Rows (1970-2013)": int(len(X_train)),
        "Test_Rows (2018-2024)": int(len(X_test)),
        "Test_F1": round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
        "Test_Precision": round(
            float(precision_score(y_test, y_pred, zero_division=0)), 4
        ),
        "Test_Recall": round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
        "Test_ROC_AUC": round(float(roc_auc_score(y_test, y_prob)), 4),
        "Test_PR_AUC": round(float(average_precision_score(y_test, y_prob)), 4),
    }
    results_df.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)
    pd.Series(test_metrics).to_csv(
        REPORTS_DIR / "best_model_test_metrics.csv", header=["value"]
    )

    # Save Confusion Matrix Figure
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["Runner-Up (0)", "Winner (1)"]
    )
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(f"Confusion Matrix on 2018–2024 Test Set\n({best_model_name})")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "04_confusion_matrix.png", dpi=150)
    plt.close(fig)

    # Error Analysis: Subgroup performance by Province & sample misclassifications
    test_eval = test_df[
        [
            "Year",
            "Constituency",
            "Province",
            "Party",
            "Registered Voters",
            "num_candidates_in_seat",
            TARGET_COLUMN,
        ]
    ].copy()
    test_eval["predicted_winner"] = y_pred
    test_eval["win_probability"] = np.round(y_prob, 4)
    test_eval["is_error"] = test_eval[TARGET_COLUMN] != test_eval["predicted_winner"]

    province_errors = (
        test_eval.groupby("Province", as_index=False)
        .agg(
            total_candidates=("is_error", "count"),
            actual_winners=(TARGET_COLUMN, "sum"),
            predicted_winners=("predicted_winner", "sum"),
            error_rate_pct=("is_error", lambda s: round(float(s.mean() * 100), 2)),
        )
        .sort_values("error_rate_pct", ascending=False)
    )
    province_errors.to_csv(REPORTS_DIR / "error_analysis_by_province.csv", index=False)

    misclassified_samples = (
        test_eval[test_eval["is_error"]]
        .sort_values("win_probability", ascending=False)
        .head(25)
    )
    misclassified_samples.to_csv(
        REPORTS_DIR / "misclassified_examples.csv", index=False
    )

    # Bonus (+2): Permutation Feature Importance on Test Set
    perm = permutation_importance(
        best_pipeline,
        X_test,
        y_test,
        n_repeats=5,
        scoring="average_precision",
        random_state=42,
        n_jobs=-1,
    )
    importance_df = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance_mean": np.round(perm.importances_mean, 4),
            "importance_std": np.round(perm.importances_std, 4),
        }
    ).sort_values("importance_mean", ascending=False)
    importance_df.to_csv(REPORTS_DIR / "feature_importance.csv", index=False)

    # Save trained pipeline artifact
    joblib.dump(best_pipeline, MODEL_PATH)

    print("Part B Training & Evaluation Complete!")
    print(f"Selected Best Model: {best_model_name}")
    print("\nCross-Validation Model Comparison:")
    print(results_df.to_string(index=False))
    print(
        f"\nHeld-Out Test Set (2018-2024) -> PR-AUC: {test_metrics['Test_PR_AUC']} | ROC-AUC: {test_metrics['Test_ROC_AUC']} | F1: {test_metrics['Test_F1']}"
    )
    print("\nTop Features by Permutation Importance:")
    print(importance_df.to_string(index=False))
    return results_df


def predict_new_rows(
    input_csv: Path, output_csv: Path, model_path: Path = MODEL_PATH
) -> pd.DataFrame:
    """Load saved pipeline, validate required feature columns, and write predictions to CSV.

    Args:
        input_csv: Path to unseen candidate rows CSV.
        output_csv: Destination path for predictions CSV.
        model_path: Path to saved joblib pipeline.

    Returns:
        DataFrame with `predicted_winner` and `win_probability` appended.

    Raises:
        FileNotFoundError: If model or input CSV is missing.
        ValueError: If required feature columns are missing from input CSV.
    """
    if not model_path.exists():
        raise FileNotFoundError(
            f"Saved model not found at {model_path}. Run training first."
        )
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found at {input_csv}.")

    df_new = pd.read_csv(input_csv)
    df_new = add_pre_election_features(df_new)
    missing_cols = [c for c in FEATURE_COLUMNS if c not in df_new.columns]
    if missing_cols:
        raise ValueError(
            f"Input CSV is missing required feature columns: {missing_cols}"
        )

    pipeline = joblib.load(model_path)
    df_new["predicted_winner"] = pipeline.predict(df_new[FEATURE_COLUMNS])
    df_new["win_probability"] = np.round(
        pipeline.predict_proba(df_new[FEATURE_COLUMNS])[:, 1], 4
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_new.to_csv(output_csv, index=False)
    print(f"Wrote {len(df_new)} predictions to {output_csv}")
    return df_new


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Part B ML Pipeline & CLI Inference")
    parser.add_argument(
        "--predict", type=Path, help="Path to unseen CSV rows for inference"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPORTS_DIR / "predictions.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    if args.predict:
        predict_new_rows(input_csv=args.predict, output_csv=args.out)
    else:
        train_and_evaluate()
