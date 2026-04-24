from collections import defaultdict
from ner_pipeline import results_baseline, results_hybrid
import pandas as pd

def is_match(pred, gold):
    pred_text, pred_type = pred
    gold_text, gold_type = gold
    
    if pred_type != gold_type:
        return False
    
    return (
        pred_text in gold_text or
        gold_text in pred_text
    )


def evaluate(results):
    stats = defaultdict(lambda: {"correct": 0, "missed": 0, "fp": 0})
    
    for item in results:
        pred = list(set(item["predicted"]))
        gold = list(set(item["expected"]))
        
        matched_gold = set()
        for p in pred:
            found = False
            
            for g in gold:
                if is_match(p, g):
                    stats[p[1]]["correct"] += 1
                    matched_gold.add(g)
                    found = True
                    break
            
            if not found:
                stats[p[1]]["fp"] += 1
        
        for g in gold:
            if g not in matched_gold:
                stats[g[1]]["missed"] += 1
    
    return stats

def compute_metrics(stats):
    metrics = {}
    
    for t, v in stats.items():
        c, fp, m = v["correct"], v["fp"], v["missed"]
        
        precision = c / (c + fp) if (c + fp) > 0 else 0
        recall = c / (c + m) if (c + m) > 0 else 0
        
        metrics[t] = {
            "correct": c,
            "missed": m,
            "fp": fp,
            "precision": round(precision, 2),
            "recall": round(recall, 2)
        }
    
    return metrics

baseline_stats = evaluate(results_baseline)
hybrid_stats = evaluate(results_hybrid)

baseline_metrics = compute_metrics(baseline_stats)
hybrid_metrics = compute_metrics(hybrid_stats)

df_baseline = pd.DataFrame(baseline_metrics).T
df_hybrid = pd.DataFrame(hybrid_metrics).T

print("=== BASELINE ===")
print(df_baseline)

print("\n=== HYBRID ===")
print(df_hybrid)