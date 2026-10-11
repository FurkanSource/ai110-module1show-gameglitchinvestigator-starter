"""Pure game rules, separated from Streamlit for direct testing."""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the starter's inclusive number range for a difficulty."""
    ranges = {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 50)}
    return ranges.get(difficulty, (1, 100))


def parse_guess(
    raw: str | None, low: int = 1, high: int = 100
) -> tuple[bool, int | None, str | None]:
    """Return validity, integer, and error for a whole number in range.

    Surrounding whitespace is allowed. Empty, non-integer, and out-of-range
    input returns an error without changing any game state.
    """
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."
    # FIX: Codex replaced decimal truncation with strict integer validation.
    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number (for example, 42)."
    if not low <= value <= high:
        return False, None, f"Enter a number between {low} and {high}."
    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare validated integers and return Win, Too High, or Too Low."""
    # FIX: Codex kept the original tests' string contract and numeric inputs.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Apply scoring using a one-based valid-guess attempt number.

    A win adds 100 points on attempt one, decreasing by 10 per additional
    attempt to a minimum bonus of 10. A miss costs 5, with a floor of zero.
    """
    # FIX: Codex removed alternating rewards and corrected the win offset.
    if outcome == "Win":
        return current_score + max(10, 100 - 10 * (attempt_number - 1))
    if outcome in ("Too High", "Too Low"):
        return max(0, current_score - 5)
    return current_score
