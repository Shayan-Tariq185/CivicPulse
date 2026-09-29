"""Turn docs/evidence/hpa-watch.txt into a replicas-vs-CPU chart and print measured timings.

Usage:  python scripts/plot_hpa.py [path-to-watch-file]
Needs:  pip install matplotlib
Only uses what was captured - nothing is estimated. Timing precision = capture interval.
"""
import re
import sys
from datetime import datetime

FMT = "%Y-%m-%d %H:%M:%S"
ROW = re.compile(
    r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\s+\S+\s+\S+\s+(?:cpu:\s*)?(\d+|<unknown>)%?/(\d+)%\s+(\d+)\s+(\d+)\s+(\d+)"
)


def read_text(path):
    raw = open(path, "rb").read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16")
    return raw.decode("utf-8-sig", errors="replace")


def parse(path):
    samples, load_start, load_end = [], None, None
    for line in read_text(path).splitlines():
        line = line.strip()
        if line.endswith("LOAD_START"):
            load_start = datetime.strptime(line[:19], FMT)
        elif line.endswith("LOAD_END"):
            load_end = datetime.strptime(line[:19], FMT)
        else:
            m = ROW.match(line)
            if m and m.group(2) != "<unknown>":
                samples.append((datetime.strptime(m.group(1), FMT), int(m.group(2)),
                                int(m.group(3)), int(m.group(6))))
    return samples, load_start, load_end


def secs(a, b):
    return int((b - a).total_seconds())


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/evidence/hpa-watch.txt"
    samples, ls, le = parse(path)
    if not samples:
        sys.exit("No HPA rows found in " + path)
    if not ls:
        print("Note: no LOAD_START marker found - run scripts/load-test.ps1 so lag can be measured.")

    times = [s[0] for s in samples]
    cpu = [s[1] for s in samples]
    target = samples[0][2]
    reps = [s[3] for s in samples]

    print(f"Samples: {len(samples)}   window: {times[0]} -> {times[-1]}")
    print(f"CPU target: {target}%   peak CPU: {max(cpu)}%   peak replicas: {max(reps)}")

    if ls:
        before = [s for s in samples if s[0] <= ls]
        base = before[-1][3] if before else reps[0]
        after = [s for s in samples if s[0] > ls]
        hot = next((s for s in after if s[1] > target), None)
        up = next((s for s in after if s[3] > base), None)
        top = next((s for s in after if s[3] == max(reps)), None)
        print(f"Replicas before load: {base}")
        if hot:
            print(f"CPU first above target: {secs(ls, hot[0])} s after load start")
        if up:
            print(f"SCALE-UP LAG (load start -> first extra replica): {secs(ls, up[0])} s")
        if top:
            print(f"Time to peak replicas ({max(reps)}): {secs(ls, top[0])} s after load start")
    if le:
        down = next((s for s in samples if s[0] > le and s[3] < max(reps)), None)
        if down:
            print(f"Scale-down began {secs(le, down[0])} s after load end")
        else:
            print("Scale-down not seen yet - keep the capture running (window is 300 s).")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        sys.exit("matplotlib missing: pip install matplotlib   (numbers above are still valid)")

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(times, cpu, color="tab:red", label="CPU % of request")
    ax1.axhline(target, color="tab:red", linestyle=":", label=f"target {target}%")
    ax1.set_ylabel("CPU utilization (%)")
    ax2 = ax1.twinx()
    ax2.step(times, reps, where="post", color="tab:blue", label="replicas")
    ax2.set_ylabel("Backend replicas")
    ax2.set_ylim(0, max(reps) + 1)
    if ls and le:
        ax1.axvspan(ls, le, color="grey", alpha=0.15, label="load running")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper right")
    ax1.set_title("CivicPulse backend: HPA replicas vs CPU under load")
    fig.autofmt_xdate()
    out = "docs/evidence/hpa-chart.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print("Saved chart:", out)


if __name__ == "__main__":
    main()
