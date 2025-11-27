import csv
import os
import time
import random
from datetime import datetime
import sys

# Prepare directories
OUTDIR = os.path.join("data", "sessions")
os.makedirs(OUTDIR, exist_ok=True)

# Ask for input mode
print("Choose input mode:")
print("1 — Standard (pynput) → easier, works everywhere")
print("2 — Raw (Win32 raw input) → high precision, best for FPS analysis")
choice = input("Enter 1 or 2 (default 2): ").strip()
if choice != "1":
    choice = "2"

# Recorder class
if choice == "1":
    from pynput import mouse

    class AimTest:
        def __init__(self, targets=12, hold_time=1.0):
            self.targets = targets
            self.hold_time = hold_time
            self.records = []
            self.last_pos = None
            self.listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)

        def on_move(self, x, y):
            t = time.time()
            if self.last_pos is None:
                dx = dy = 0.0
            else:
                dx = x - self.last_pos[0]
                dy = y - self.last_pos[1]
            self.last_pos = (x, y)
            self.records.append((t, dx, dy, x, y, 0))

        def on_click(self, x, y, button, pressed):
            t = time.time()
            self.records.append((t, 0.0, 0.0, x, y, 1 if pressed else 0))

        def run(self):
            import tkinter as tk
            root = tk.Tk()
            root.attributes("-fullscreen", True)
            canvas = tk.Canvas(root, bg="black")
            canvas.pack(fill=tk.BOTH, expand=True)

            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()

            self.listener.start()
            targets = [(random.randint(200, width-200), random.randint(200, height-200))
                       for _ in range(self.targets)]
            idx = 0

            def next_target():
                nonlocal idx
                canvas.delete("all")
                if idx >= len(targets):
                    root.destroy()
                    self.listener.stop()
                    self.save()
                    return
                x, y = targets[idx]
                r = 30
                canvas.create_oval(x-r, y-r, x+r, y+r, fill="white")
                idx += 1
                root.after(int(self.hold_time*1000), next_target)

            root.after(500, next_target)
            root.mainloop()

        def save(self):
            fname = datetime.now().strftime("session_%Y%m%d_%H%M%S.csv")
            path = os.path.join(OUTDIR, fname)
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["t","dx","dy","x","y","click"])
                for r in self.records:
                    writer.writerow(r)
            print(f"[OK] Saved session → {path}")

else:  # Raw Win32 input
    import ctypes
    from ctypes import wintypes
    import pythoncom
    import win32api, win32con, win32gui

    class RawAimTest:
        def __init__(self, duration=10):
            self.records = []
            self.duration = duration

        def run(self):
            print("[INFO] Running raw input test for", self.duration, "seconds")
            print("Move your mouse around now...")
            start = time.time()
            while time.time() - start < self.duration:
                x, y = win32api.GetCursorPos()
                t = time.time()
                self.records.append((t, 0, 0, x, y, 0))
                time.sleep(0.01)
            self.save()

        def save(self):
            fname = datetime.now().strftime("session_%Y%m%d_%H%M%S.csv")
            path = os.path.join(OUTDIR, fname)
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["t","dx","dy","x","y","click"])
                for r in self.records:
                    writer.writerow(r)
            print(f"[OK] Saved session → {path}")

# Run chosen recorder
if choice == "1":
    AimTest().run()
else:
    RawAimTest().run()
