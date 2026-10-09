"""Plot growth rates: n!, C(n, n/2), and Bell numbers on a log scale."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from combinatorics import combinations, bell_number, factorial_iterative

ns = list(range(1, 31))
facts = [factorial_iterative(n) for n in ns]
central = [combinations(n, n // 2) for n in ns]
bells = [bell_number(n) for n in ns]

plt.figure(figsize=(9, 6))
plt.semilogy(ns, facts, "o-", label="n! (factorial)")
plt.semilogy(ns, central, "s-", label="C(n, floor(n/2)) central binomial")
plt.semilogy(ns, bells, "^-", label="B(n) Bell numbers")
plt.xlabel("n")
plt.ylabel("value (log scale)")
plt.title("Combinatorial growth rates")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("growth_rates.png", dpi=120)
print("saved growth_rates.png")
