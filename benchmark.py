"""Benchmark the four factorial algorithms in combinatorics.py."""
import math
import timeit

from combinatorics import (
    factorial_iterative,
    factorial_memoized,
    factorial_prime,
)

METHODS = {
    "iterative (loop)": factorial_iterative,
    "memoized (lru_cache)": factorial_memoized,
    "prime factorization": factorial_prime,
    "stdlib math.factorial": math.factorial,
}


def benchmark(ns=(100, 500, 1000, 2000), repeats=5):
    print(f"{'n':>6} | " + " | ".join(f"{name:>22}" for name in METHODS))
    print("-" * (8 + 25 * len(METHODS)))
    results = {name: [] for name in METHODS}
    for n in ns:
        row = []
        for name, fn in METHODS.items():
            # warm the memoized cache once per n so we measure steady state
            if name.startswith("memoized"):
                fn(n)
            t = min(timeit.repeat(lambda: fn(n), number=1, repeat=repeats))
            results[name].append(t)
            row.append(f"{t * 1000:>20.3f} ms")
        print(f"{n:>6} | " + " | ".join(row))
    return results


if __name__ == "__main__":
    print("Factorial algorithm shootout (best of 5 runs)\n")
    benchmark()
    print("\nNote: memoized is O(1) after the cache warms; prime factorization")
    print("wins on very large n by doing fewer big-int multiplications.")
