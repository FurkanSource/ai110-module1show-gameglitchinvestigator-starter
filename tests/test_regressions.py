"""Regression tests for validation, numeric comparisons, and scoring."""

import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


@pytest.mark.parametrize("raw", [None, "", "   ", "abc", "3.9", "50.0"])
def test_invalid_input_is_rejected(raw):
    ok, value, error = parse_guess(raw)
    assert not ok
    assert value is None
    assert error


@pytest.mark.parametrize("raw", ["-1", "0", "101"])
def test_out_of_range_input_is_rejected(raw):
    assert parse_guess(raw, 1, 100)[0] is False


@pytest.mark.parametrize("raw, expected", [("1", 1), ("100", 100), (" 50 ", 50)])
def test_integer_boundaries_and_whitespace(raw, expected):
    assert parse_guess(raw, 1, 100) == (True, expected, None)


def test_easy_range_is_enforced():
    assert parse_guess("20", 1, 20) == (True, 20, None)
    assert parse_guess("21", 1, 20)[0] is False


@pytest.mark.parametrize(
    "guess, expected", [(9, "Too Low"), (100, "Too High"), (50, "Win")]
)
def test_comparisons_are_numeric(guess, expected):
    assert check_guess(guess, 50) == expected


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
@pytest.mark.parametrize("attempt", [1, 2])
def test_incorrect_guesses_never_reward_points(outcome, attempt):
    assert update_score(20, outcome, attempt) == 15
    assert update_score(0, outcome, attempt) == 0


def test_win_bonus_has_no_off_by_one():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 3) == 80
    assert update_score(0, "Win", 20) == 10


@pytest.mark.parametrize(
    "difficulty, expected",
    [("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 50))],
)
def test_starter_difficulty_ranges_preserved(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected
