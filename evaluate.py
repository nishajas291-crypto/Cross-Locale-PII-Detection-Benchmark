"""Score the detectors against gold labels. Run: python evaluate.py [--model en_core_web_lg]
Matching rule: a prediction is a true positive if the type is equal and span IoU >= 0.5 with an unmatched gold span.
Precision/recall come with Wilson 95% confidence intervals.
"""
import argparse, json, math, collections
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from detectors import RegexDetector, PresidioDetector, TARGETS

def wilson(k, n, z=1.96):
    if n == 0: return float("nan"), float("nan"), float("nan")
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)

def iou(a, b):
    inter = max(0, min(a[1], b[1]) - max(a[0], b[0])); union = (a[1]-a[0]) + (b[1]-b[0]) - inter
    return inter / union if union else 0

def score_text(pred, gold):
    """returns list of (type, outcome, locale-agnostic) outcomes: TP / FP / FN"""
    out, used = [], set()
    for t, s, e in sorted(pred, key=lambda x: x[1]):
        best, bi = 0, None
        for i, g in enumerate(gold):
            if i in used or g["type"] != t: continue
            v = iou((s, e), (g["start"], g["end"]))
            if v > best: best, bi = v, i
        if bi is not None and best >= 0.5: used.add(bi); out.append((t, "TP"))
        else: out.append((t, "FP"))
    for i, g in enumerate(gold):
        if i not in used: out.append((g["type"], "FN"))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data", default="data/synthetic_pii.jsonl")
    ap.add_argument("--model", default="en_core_web_sm"); a = ap.parse_args()
    data = [json.loads(l) for l in open(a.data)]
    dets = [RegexDetector(), PresidioDetector(a.model, india=False), PresidioDetector(a.model, india=True)]
    rows = []  # one row per (detector, locale, type, outcome)
    for d in dets:
        print("running", d.name)
        for r in data:
            pred = [p for p in d.detect(r["text"]) if p[0] in TARGETS]
            for t, o in score_text(pred, r["entities"]): rows.append((d.name, r["locale"], t, o))
    df = pd.DataFrame(rows, columns=["detector", "locale", "type", "outcome"])
    cnt = df.groupby(["detector", "type", "outcome"]).size().unstack(fill_value=0).reindex(columns=["TP", "FP", "FN"], fill_value=0)
    res = []
    for (det, typ), r in cnt.iterrows():
        tp, fp, fn = int(r.TP), int(r.FP), int(r.FN)
        p, pl, ph = wilson(tp, tp + fp); rc, rl, rh = wilson(tp, tp + fn)
        f1 = 2 * p * rc / (p + rc) if (p + rc) else 0
        res.append(dict(detector=det, entity=typ, TP=tp, FP=fp, FN=fn, precision=round(p, 3), precision_ci=f"[{pl:.2f}, {ph:.2f}]",
                        recall=round(rc, 3), recall_ci=f"[{rl:.2f}, {rh:.2f}]", f1=round(f1, 3)))
    res = pd.DataFrame(res); res.to_csv("results/results_by_entity.csv", index=False)
    # locale breakdown: recall of shared entity types on US vs IN text
    loc = []
    for (det, l, typ), g in df[df.locale.isin(["US", "IN"])].groupby(["detector", "locale", "type"]):
        tp = (g.outcome == "TP").sum(); fn = (g.outcome == "FN").sum()
        if tp + fn >= 20:
            rc, lo, hi = wilson(tp, tp + fn); loc.append(dict(detector=det, locale=l, entity=typ, n=tp+fn, recall=round(rc, 3), recall_ci=f"[{lo:.2f}, {hi:.2f}]"))
    loc = pd.DataFrame(loc); loc.to_csv("results/results_by_locale.csv", index=False)
    # false alarms on PII-free sentences
    neg = df[df.locale == "NONE"]; neg_sent = sum(1 for r in data if r["locale"] == "NONE")
    fa = []
    for det in [d.name for d in dets]:
        bad = neg[(neg.detector == det) & (neg.outcome == "FP")]
        fa.append(dict(detector=det, false_alarms=len(bad), pii_free_sentences=neg_sent, most_common=", ".join(f"{k}:{v}" for k, v in collections.Counter(bad.type).most_common(3))))
    fa = pd.DataFrame(fa); fa.to_csv("results/false_alarms.csv", index=False)
    with open("results/results.md", "w") as f:
        f.write(f"# PII detection results (model: {a.model}, {len(data)} sentences)\n\n## By entity type\n\n{res.to_markdown(index=False)}\n\n")
        f.write(f"## Recall by locale (US vs Indian formats)\n\n{loc.to_markdown(index=False)}\n\n## False alarms on PII-free sentences\n\n{fa.to_markdown(index=False)}\n")
    piv = res.pivot(index="entity", columns="detector", values="recall").fillna(0)
    piv.plot(kind="bar", figsize=(9, 5)); plt.ylabel("Recall"); plt.title("PII recall by entity type"); plt.ylim(0, 1.05)
    plt.xticks(rotation=30, ha="right"); plt.tight_layout(); plt.savefig("results/recall_by_entity.png", dpi=150)
    print(res.to_string(index=False)); print(); print(loc.to_string(index=False)); print(); print(fa.to_string(index=False))

if __name__ == "__main__":
    main()
