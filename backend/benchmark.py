import time

from services.myers_diff import myers_diff


def run_benchmark(size):
    old_lines = [
        f"line {i}"
        for i in range(size)
    ]

    new_lines = old_lines.copy()

    # Simulate several modifications.
    change_points = [
        size // 4,
        size // 2,
        (size * 3) // 4
    ]

    for point in change_points:
        new_lines[point] = f"modified line {point}"

    start = time.perf_counter()

    result = myers_diff(
        old_lines,
        new_lines
    )

    end = time.perf_counter()

    elapsed_ms = (end - start) * 1000

    return elapsed_ms, len(result)

sizes = [
    100,
    1000,
    5000,
    10000
]


print()
print("GitDiff Benchmark")
print("=" * 40)

for size in sizes:

    elapsed, operations = run_benchmark(size)

    print(
        f"{size:>6} lines : "
        f"{elapsed:>10.3f} ms | "
        f"{operations} operations"
    )