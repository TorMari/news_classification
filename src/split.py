import os
import json
from datetime import datetime
import pandas as pd


def make_splits(df, strategy="time+group", seed=42,
                target_col="category_id",
                group_col=None,
                time_col="datePublished",
                train_size=0.7,
                val_size=0.15,
                test_size=0.15):

    df = df.copy()
    if "row_id" not in df.columns:
        df = df.reset_index().rename(columns={"index": "row_id"})

    splits = {"train": [], "val": [], "test": []}

    if strategy == "time+group":
        df[time_col] = pd.to_datetime(df[time_col])

        df_sorted_list = []
        for _, group in df.groupby(target_col):
            group_sorted = group.sort_values(time_col)
            df_sorted_list.append(group_sorted)
        
        for _, group in df.groupby(target_col):
            group_sorted = group.sort_values(time_col)
            
            n = len(group_sorted)
            train_end = int(n * train_size)
            val_end = train_end + int(n * val_size)

            splits["train"].extend(group_sorted.iloc[:train_end]["row_id"].tolist())
            splits["val"].extend(group_sorted.iloc[train_end:val_end]["row_id"].tolist())
            splits["test"].extend(group_sorted.iloc[val_end:]["row_id"].tolist())

    else:
        raise ValueError("Unknown strategy")

    return splits


def save_splits(splits, out_dir="data/sample", seed=42, strategy="time+group",
                group_col="category_id", time_col="datePublished"):

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    for split_name, ids in splits.items():
        path = os.path.join(out_dir, f"splits_{split_name}_ids.txt")

        with open(path, "w", encoding="utf-8") as f:
            for i in ids:
                f.write(str(i) + "\n")

    manifest = {
        "strategy": strategy,
        "seed": seed,
        "generated_at": datetime.utcnow().isoformat(),
        "sizes": {
            "train": len(splits["train"]),
            "val": len(splits["val"]),
            "test": len(splits["test"])
        },
        "columns_used": {
            "group_column": group_col,
            "time_column": time_col
        }
    }

    with open("docs/splits_manifest_lab5.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)