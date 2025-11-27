import csv
import numpy as np
import os

def load_session(path):
    rows = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "t": float(row["t"]),
                "dx": float(row["dx"]),
                "dy": float(row["dy"]),
                "x": float(row["x"]),
                "y": float(row["y"]),
                "click": int(row["click"])
            })
    return rows

def compute_metrics(rows):
    dxy = np.array([[r["dx"], r["dy"]] for r in rows])
    speeds = np.linalg.norm(dxy, axis=1)
    return {
        "mean_speed": float(np.mean(speeds)),
        "std_speed": float(np.std(speeds)),
        "clicks": sum(r["click"] for r in rows),
        "samples": len(rows)
    }

def recommend_settings(metrics):
    gain = max(0.2, min(3.0, 1.0 + (metrics["mean_speed"] - 5)/20))
    smoothness = max(0.0, min(1.0, 0.2 + metrics["std_speed"]/10))
    return {
        "global": {
            "gain": float(gain),
            "smoothness": float(smoothness),
            "angle": 0.0
        }
    }

if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    rows = load_session(path)
    metrics = compute_metrics(rows)
    patch = recommend_settings(metrics)
    print("Metrics:", metrics)
    print("Recommended patch:", patch)
