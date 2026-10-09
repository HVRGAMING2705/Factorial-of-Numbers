"""Combinatorics Toolkit — factorials, permutations, combinations,
Stirling numbers, and counting utilities with multiple algorithmic approaches.
"""
import math
from functools import lru_cache


def _check_nonneg_int(n, name="n"):
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"{name} must be an integer, got {type(n).__name__}")
    if n < 0:
        raise ValueError(f"{name} must be non-negative, got {n}")


def factorial_iterative(n):
    """n! computed with a simple loop. O(n) multiplications."""
    _check_nonneg_int(n)
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@lru_cache(maxsize=None)
def _memo_fact(n):
    return 1 if n < 2 else n * _memo_fact(n - 1)


_memo_cache = {0: 1, 1: 1}


def factorial_memoized(n):
    """n! with memoization: repeated calls are O(1) after the first.

    Implemented iteratively over an explicit cache dict so there is no
    recursion-depth limit (a naive recursive lru_cache version dies
    past n ~ 1000 on CPython's default recursion limit).
    """
    _check_nonneg_int(n)
    if n in _memo_cache:
        return _memo_cache[n]
    start = max(k for k in _memo_cache if k <= n)
    acc = _memo_cache[start]
    for i in range(start + 1, n + 1):
        acc *= i
        _memo_cache[i] = acc
    return acc


def _primes_upto(n):
    """Sieve of Eratosthenes."""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i:n + 1:i] = [False] * len(range(i * i, n + 1, i))
    return [i for i, is_p in enumerate(sieve) if is_p]


def factorial_prime(n):
    """n! via prime factorization (Legendre's formula).

    The exponent of prime p in n! is sum(floor(n / p^i)). Multiplying
    p**exp for each prime is often faster than naive multiplication for
    large n because there are far fewer primes than n.
    """
    _check_nonneg_int(n)
    if n < 2:
        return 1
    result = 1
    for p in _primes_upto(n):
        exp, power = 0, p
        while power <= n:
            exp += n // power
            power *= p
        result *= p ** exp
    return result


def factorial(n, method="auto"):
    """Unified factorial with selectable algorithm.

    method: 'iterative' | 'memoized' | 'prime' | 'stdlib' | 'auto'
    """
    methods = {
        "iterative": factorial_iterative,
        "memoized": factorial_memoized,
        "prime": factorial_prime,
        "stdlib": math.factorial,
    }
    if method == "auto":
        return math.factorial(n)
    if method not in methods:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(methods)}")
    return methods[method](n)


def permutations(n, r):
    """nPr — ordered arrangements of r items chosen from n."""
    _check_nonneg_int(n)
    _check_nonneg_int(r, "r")
    if r > n:
        return 0
    result = 1
    for i in range(n, n - r, -1):
        result *= i
    return result


def combinations(n, r):
    """nCr — unordered selections of r items from n.

    Uses the multiplicative formula C(n,r) = prod((n-k)/(k+1)) with exact
    integer division, avoiding gigantic intermediate factorials.
    """
    _check_nonneg_int(n)
    _check_nonneg_int(r, "r")
    if r > n:
        return 0
    r = min(r, n - r)
    result = 1
    for k in range(r):
        result = result * (n - k) // (k + 1)
    return result


def stirling2(n, k):
    """Stirling numbers of the second kind S(n, k): ways to partition
    n labelled objects into k non-empty unlabelled subsets. Dynamic
    programming with S(n,k) = k*S(n-1,k) + S(n-1,k-1)."""
    _check_nonneg_int(n)
    _check_nonneg_int(k, "k")
    if k > n:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    table = [[0] * (k + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            table[i][j] = j * table[i - 1][j] + table[i - 1][j - 1]
    return table[n][k]


def bell_number(n):
    """B(n) — total partitions of n labelled objects: sum_k S(n, k)."""
    _check_nonneg_int(n)
    return sum(stirling2(n, k) for k in range(n + 1))


def gamma_factorial(x):
    """Continuous extension of factorial: Gamma(x + 1).

    Agrees with n! for integers; defined for non-integers too
    (e.g. (1/2)! = sqrt(pi)/2).
    """
    if isinstance(x, int) and x < 0:
        raise ValueError("factorial undefined for negative integers")
    return math.gamma(x + 1)


def trailing_zeros(n):
    """Zeros at the end of n! — count of factor 5s (Legendre)."""
    _check_nonneg_int(n)
    count, power = 0, 5
    while power <= n:
        count += n // power
        power *= 5
    return count


def multinomial(n, groups):
    """Multinomial coefficient: arrangements of n items split into
    groups of the given sizes. sum(groups) must equal n."""
    _check_nonneg_int(n)
    if sum(groups) != n:
        raise ValueError(f"group sizes {groups} must sum to n={n}")
    result = factorial_iterative(n)
    for g in groups:
        result //= factorial_iterative(g)
    return result


def derangements(n):
    """!n — permutations of n with no element in its original position
    (the hat-check problem). Recurrence: !n = (n-1)*(!(n-1) + !(n-2))."""
    _check_nonneg_int(n)
    if n == 0:
        return 1
    if n == 1:
        return 0
    a, b = 1, 0
    for i in range(2, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b
