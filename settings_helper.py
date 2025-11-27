import json, shutil, subprocess, time
from pathlib import Path

DEFAULT_RAWACCEL_PATH = r"C:\Program Files\RawAccel"

def find_settings_path():
    p = Path(DEFAULT_RAWACCEL_PATH) / "settings.json"
    if p.exists():
        return p
    raise FileNotFoundError("RawAccel settings.json not found. Edit DEFAULT_RAWACCEL_PATH.")

def backup(path):
    bak = path.with_suffix(".bak")
    shutil.copy2(path, bak)
    print(f"[OK] Backup created → {bak}")
    return bak

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def merge_patch(base, patch):
    for k, v in patch.items():
        if isinstance(v, dict) and k in base:
            base[k] = merge_patch(base[k], v)
        else:
            base[k] = v
    return base

def restart_rawaccel():
    exe = "RawAccel.exe"
    subprocess.run(["taskkill","/f","/im",exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    exe_path = Path(DEFAULT_RAWACCEL_PATH) / exe
    if exe_path.exists():
        subprocess.Popen([str(exe_path)])
        time.sleep(0.5)
        print("[OK] RawAccel restarted")
        return True
    else:
        print("[ERROR] RawAccel.exe not found")
        return False

def safe_apply_patch(patch):
    path = find_settings_path()
    backup(path)
    data = load_json(path)
    new_data = merge_patch(data, patch)
    preview = path.with_suffix(".preview.json")
    save_json(preview, new_data)
    print(f"[OK] Preview saved → {preview}")
    save_json(path, new_data)
    print("[OK] Settings updated")
    restart_rawaccel()
