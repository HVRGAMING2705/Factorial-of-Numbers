"""Real probability examples solved with the Combinatorics Toolkit."""
from combinatorics import combinations, derangements, permutations


def poker_two_aces():
    # P(exactly 2 aces in a 5-card hand)
    good = combinations(4, 2) * combinations(48, 3)
    total = combinations(52, 5)
    return good / total


def lottery_6_of_49():
    # P(jackpot) = 1 / C(49, 6)
    return 1 / combinations(49, 6)


def committee():
    # Ways to choose a 3-person committee from 10 people
    return combinations(10, 3)


def hat_check(n=10):
    # P(no one gets their own hat back) = !n / n!  -> approaches 1/e
    return derangements(n) / __import__("math").factorial(n)


def password_space():
    # 8-char passwords from 62 alphanumerics, order matters, repetition allowed
    return 62 ** 8


if __name__ == "__main__":
    print(f"P(exactly 2 aces in poker hand) = {poker_two_aces():.6f}")
    print(f"P(6/49 lottery jackpot)         = 1 in {1 / lottery_6_of_49():,.0f}")
    print(f"3-person committees from 10     = {committee()}")
    print(f"P(nobody gets own hat, n=10)    = {hat_check():.6f} (1/e = 0.367879)")
    print(f"8-char alphanumeric passwords   = {password_space():,}")
    print(f"Ordered 3-letter codes (26^3)   = {permutations(26, 3):,} without repetition")
