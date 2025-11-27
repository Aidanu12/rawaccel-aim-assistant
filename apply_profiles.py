import os
from analyzer import load_session, compute_metrics, recommend_settings
from settings_helper import safe_apply_patch

def find_latest_session():
    files = sorted(os.listdir("data/sessions"))
    return os.path.join("data/sessions", files[-1])

def main(apply=False):
    session = find_latest_session()
    print("[INFO] Using session:", session)
    rows = load_session(session)
    metrics = compute_metrics(rows)
    patch = recommend_settings(metrics)
    print("Metrics:", metrics)
    print("Recommended patch:", patch)
    if apply:
        safe_apply_patch(patch)
    else:
        print("[INFO] Run with --apply to modify RawAccel settings")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    main(args.apply)
