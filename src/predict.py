"""Predice con un modelo guardado y conserva una salida auditable."""
import argparse
from pathlib import Path
import joblib, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--threshold", type=float, default=.5)
    args = ap.parse_args()
    df = pd.read_csv(args.data)
    row_id = df["id"] if "id" in df else pd.Series(range(len(df)))
    y_true = df["label"] if "label" in df else pd.Series([None] * len(df))
    X = df.drop(columns=[c for c in ["label", "attack_cat", "id"] if c in df])
    model = joblib.load(args.model)
    score = model.predict_proba(X)[:, 1]
    out = pd.DataFrame({"row_id": row_id, "y_true": y_true,
                        "score_attack": score,
                        "y_pred": (score >= args.threshold).astype(int)})
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
