"""Streamlit interface for the repaired number guessing game."""

import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}
HINTS = {"Too High": "📉 Too High — go lower!",
         "Too Low": "📈 Too Low — go higher!"}


def start_new_game():
    """Reset every round-specific value using the selected difficulty."""
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    # FIX: Codex centralized resets for both New Game and difficulty changes.
    st.session_state.update(
        secret=random.randint(low, high),
        attempts=0,
        score=0,
        status="playing",
        history=[],
        guess_input="",
        input_error=None,
        last_outcome=None,
    )


def submit_guess():
    """Validate first, then apply exactly one attempt and its result."""
    if st.session_state.get("_guess_submitted_this_run", False):
        return
    st.session_state._guess_submitted_this_run = True

    if st.session_state.status != "playing":
        return
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    ok, guess, error = parse_guess(st.session_state.guess_input, low, high)
    st.session_state.input_error = error
    if not ok:
        return

    # FIX: Codex counts valid guesses only and never casts the secret to text.
    st.session_state.attempts += 1
    outcome = check_guess(guess, st.session_state.secret)
    st.session_state.score = update_score(
        st.session_state.score, outcome, st.session_state.attempts
    )
    st.session_state.last_outcome = outcome
    st.session_state.history.append({
        "Attempt": st.session_state.attempts,
        "Guess": guess,
        "Outcome": outcome,
        "Score": st.session_state.score,
    })
    if outcome == "Win":
        st.session_state.status = "won"
    elif st.session_state.attempts >= ATTEMPT_LIMITS[st.session_state.difficulty]:
        st.session_state.status = "lost"


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("A repaired guessing game with clear hints and tested rules.")
st.sidebar.header("Settings")
st.sidebar.selectbox(
    "Difficulty", list(ATTEMPT_LIMITS), index=1, key="difficulty",
    on_change=start_new_game,
)
if "secret" not in st.session_state:
    start_new_game()
st.session_state._guess_submitted_this_run = False

difficulty = st.session_state.difficulty
low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.sidebar.caption("Changing difficulty starts a fresh round.")
st.sidebar.markdown(
    "**Scoring:** First-guess win: 100 points; each additional valid guess "
    "reduces the win bonus by 10 (minimum 10). Misses cost 5 points, "
    "with a score floor of zero. New Game resets the score."
)

st.info(f"Guess a whole number between {low} and {high}.")
left, right = st.columns(2)
left.metric("Attempts left", max(0, attempt_limit - st.session_state.attempts))
right.metric("Round score", st.session_state.score)
finished = st.session_state.status != "playing"
st.text_input(
    "Enter your guess:",
    key="guess_input",
    disabled=finished,
    on_change=submit_guess,
)
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Submit Guess 🚀", on_click=submit_guess, disabled=finished)
with col2:
    st.button("New Game 🔁", on_click=start_new_game)
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.session_state.input_error:
    st.error(st.session_state.input_error)
elif st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}. Start a new game to try again."
    )
elif show_hint and st.session_state.last_outcome in HINTS:
    # FIX: Codex made the direction agree with the numeric outcome.
    st.warning(HINTS[st.session_state.last_outcome])

if st.session_state.history:
    st.subheader("Guess history")
    st.table(st.session_state.history)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)

st.divider()
st.caption("AI-assisted repairs verified with logic and Streamlit tests.")
