"""Exercise actual Streamlit reruns, controls, and session state."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def game():
    app = Path(__file__).resolve().parents[1] / "app.py"
    instance = AppTest.from_file(str(app), default_timeout=30).run()
    assert not instance.exception
    instance.session_state.secret = 50
    return instance


def guess(game, value):
    """Submit through the same input and button used by a player."""
    game.text_input[0].set_value(value)
    game.button[0].click().run()
    assert not game.exception


def test_complete_game_and_restart(game):
    assert game.session_state.attempts == 0
    guess(game, "40")
    assert "higher" in game.warning[0].value.lower()
    guess(game, "70")
    assert "lower" in game.warning[0].value.lower()
    guess(game, "50")
    assert game.session_state.status == "won"
    assert game.session_state.attempts == 3
    assert game.session_state.score == 80
    assert game.button[0].disabled
    assert "80" in game.success[0].value
    game.button[1].click().run()
    assert game.session_state.status == "playing"
    assert game.session_state.attempts == 0
    assert game.session_state.score == 0
    assert game.session_state.history == []
    assert game.text_input[0].value == ""
    assert not game.button[0].disabled


def test_invalid_inputs_do_not_consume_attempts(game):
    for value in ["", "  ", "abc", "3.9", "-1", "0", "101"]:
        guess(game, value)
        assert game.error
        assert game.session_state.attempts == 0
        assert game.session_state.history == []
        assert game.session_state.score == 0
        assert game.session_state.secret == 50


def test_loss_on_exact_attempt_limit_and_restart(game):
    for attempt in range(1, 9):
        guess(game, "1")
        assert game.session_state.attempts == attempt
        expected = "lost" if attempt == 8 else "playing"
        assert game.session_state.status == expected
    assert game.button[0].disabled
    assert "0" in game.metric[0].value
    assert "50" in game.error[0].value
    game.button[1].click().run()
    assert game.session_state.status == "playing"
    assert game.session_state.attempts == 0


def test_last_allowed_guess_can_win(game):
    for _ in range(7):
        guess(game, "1")
    guess(game, "50")
    assert game.session_state.status == "won"
    assert game.session_state.score == 30


def test_difficulty_change_and_new_game_use_correct_range(game):
    guess(game, "40")
    game.selectbox[0].select("Easy").run()
    assert 1 <= game.session_state.secret <= 20
    assert game.session_state.attempts == 0
    assert game.session_state.history == []
    assert "1 and 20" in game.info[0].value
    assert game.metric[0].value == "6"
    game.session_state.secret = 20
    guess(game, "21")
    assert game.session_state.attempts == 0
    guess(game, "20")
    assert game.session_state.status == "won"
    game.button[1].click().run()
    assert 1 <= game.session_state.secret <= 20
    assert game.session_state.status == "playing"


def test_unrelated_rerun_preserves_secret_and_round(game):
    guess(game, "9")
    assert game.session_state.history[-1]["Outcome"] == "Too Low"
    game.checkbox[0].uncheck().run()
    assert game.session_state.secret == 50
    assert game.session_state.attempts == 1
    assert len(game.session_state.history) == 1
    assert not game.warning


def test_pressing_enter_on_text_input_submits_guess(game):
    game.text_input[0].set_value("40").run()
    assert game.session_state.attempts == 1
    assert "higher" in game.warning[0].value.lower()

