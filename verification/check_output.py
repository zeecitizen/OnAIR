"""Verification helper for the fork only, not for upstream.

Reads OnAIR's printed CURRENT DATA lines and reports, for each back-to-back
pair published in part 2, whether the first channel's values reached the
pipeline or were lost."""

import ast
import sys

rows = []
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    if line.startswith("CURRENT DATA:"):
        rows.append(ast.literal_eval(line.split(":", 1)[1].strip()))

print("frames printed:", len(rows))
print("part 1 (one channel per frame):")
for r in rows[:3]:
    print("   ", r)

lost = delivered = 0
for n in range(10, 210, 10):
    want = [n + 0.1, n + 0.2]
    # the pair is state_0 = n then state_1 = n + 1; look at every frame from
    # the one where state_1 = n + 1 arrived until the next pair
    seen = [r for r in rows if r[3:5] == [n + 1.1, n + 1.2]]
    if not seen:
        print("    pair %d: state_1 value not found in output" % n)
        continue
    if any(r[1:3] == want for r in seen):
        delivered += 1
    else:
        lost += 1
        print("    pair %d: state_0 LOST, pipeline shows %s" % (n, seen[-1]))
print(
    "part 2 (two channels back to back, 20 pairs): state_0 delivered %d, lost %d"
    % (delivered, lost)
)
