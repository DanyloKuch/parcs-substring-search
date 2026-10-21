import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "results.csv"), newline="", encoding="utf-8") as f:
    rows = [r for r in csv.DictReader(f) if r["mode"] == "par"]

seq_time = float(next(r["time_s"] for r in csv.DictReader(open(os.path.join(here, "results.csv"), encoding="utf-8")) if r["mode"] == "seq"))
workers = [int(r["workers"]) for r in rows]
times = [float(r["time_s"]) for r in rows]
speedup = [seq_time / t for t in times]
efficiency = [s / w for s, w in zip(speedup, workers)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

ax1.plot(workers, times, "o-", color="#1f77b4", label="PARCS (Python, KMP)")
ax1.axhline(seq_time, color="gray", linestyle="--", label="Послідовно (master)")
ax1.set_xlabel("Кількість воркерів N")
ax1.set_ylabel("Час виконання, с")
ax1.set_title("Час виконання від кількості воркерів")
ax1.set_xticks(workers)
ax1.grid(alpha=0.3)
ax1.legend()

ax2.plot(workers, speedup, "o-", color="#2ca02c", label="Фактичне прискорення")
ax2.plot(workers, workers, "--", color="gray", label="Ідеальне (N)")
for w, s, e in zip(workers, speedup, efficiency):
    ax2.annotate(f"{e:.0%}", (w, s), textcoords="offset points", xytext=(6, -12))
ax2.set_xlabel("Кількість воркерів N")
ax2.set_ylabel("Прискорення S = T_seq / T_N")
ax2.set_title("Прискорення (підписано ефективність)")
ax2.set_xticks(workers)
ax2.grid(alpha=0.3)
ax2.legend()

fig.tight_layout()
fig.savefig(os.path.join(here, "plot.png"), dpi=150)
print("saved", os.path.join(here, "plot.png"))
