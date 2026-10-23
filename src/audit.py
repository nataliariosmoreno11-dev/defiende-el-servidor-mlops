"""Audita un CSV UNSW-NB15 y escribe evidencia estructurada."""
import argparse, hashlib, json
from pathlib import Path
import pandas as pd

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--output", default="evidencias/auditoria.json")
    args=ap.parse_args()
    report={"source":"UNSW-NB15","files":[]}
    for name in args.files:
        p=Path(name); df=pd.read_csv(p)
        report["files"].append({"path":name,"sha256":sha256(p),
          "rows":len(df),"columns":df.columns.tolist(),
          "classes":df["label"].value_counts(dropna=False).to_dict() if "label" in df else {},
          "missing":df.isna().sum().to_dict()})
    Path(args.output).parent.mkdir(exist_ok=True)
    Path(args.output).write_text(json.dumps(report,indent=2,default=str))
if __name__=="__main__":
    main()
