"""Entrena una configuración y registra el experimento en MLflow.

Uso:
python -m src.train --config configs/v1.yaml --data data/UNSW_NB15_training-set.csv
"""
from __future__ import annotations
import argparse, json, os, subprocess
from pathlib import Path
import mlflow, yaml, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DROP = {"label", "attack_cat", "id"}

def git_value() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"

def make_estimator(cfg, numeric, categorical):
    prep_num = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
    prep_cat = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                         ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    prep = ColumnTransformer([("num", prep_num, numeric), ("cat", prep_cat, categorical)])
    if cfg["family"] == "logistic_regression":
        model = LogisticRegression(max_iter=500, C=cfg["model"]["C"],
                                   class_weight=cfg["model"]["class_weight"])
    else:
        model = RandomForestClassifier(random_state=cfg["seed"], **cfg["model"])
    return Pipeline([("preprocess", prep), ("model", model)])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--experiment", default="defiende-el-servidor")
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text())
    df = pd.read_csv(args.data)
    y = df.pop("label").astype(int)
    X = df.drop(columns=[c for c in ["attack_cat", "id"] if c in df], errors="ignore")
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]
    Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=.2, stratify=y,
                                          random_state=cfg["seed"])
    pipe = make_estimator(cfg, numeric, categorical)
    mlflow.set_experiment(args.experiment)
    with mlflow.start_run(run_name=cfg["version"]) as run:
        pipe.fit(Xtr, ytr)
        score = pipe.predict_proba(Xva)[:, 1]
        pred = (score >= cfg["threshold"]).astype(int)
        tn, fp, fn, tp = confusion_matrix(yva, pred, labels=[0,1]).ravel()
        metrics = {
            "recall_attack": recall_score(yva, pred, zero_division=0),
            "precision_attack": precision_score(yva, pred, zero_division=0),
            "fpr": fp / (fp + tn) if fp + tn else 0.0,
            "macro_f1": f1_score(yva, pred, average="macro", zero_division=0),
        }
        mlflow.log_params({"version": cfg["version"], "family": cfg["family"],
                           "seed": cfg["seed"], "threshold": cfg["threshold"],
                           "git_commit": git_value()})
        mlflow.log_metrics(metrics)
        Path("models").mkdir(exist_ok=True)
        import joblib
        artifact = Path("models") / (cfg["version"] + ".joblib")
        joblib.dump(pipe, artifact)
        mlflow.log_artifact(str(artifact))
        print(json.dumps({"run_id": run.info.run_id, **metrics}, indent=2))

if __name__ == "__main__":
    main()
