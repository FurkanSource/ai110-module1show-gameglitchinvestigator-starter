# AI Interactions Log

## Actual Requests and Decisions

Tool: OpenAI Codex desktop app. The student's initial request was:

> look through the tab open on google then finish the assignment due at oct 11 dont submit after u finish

When asked about prior work, Furkan said he had "fixed some bugs." Codex
proposed building on those fixes and asked for their location. Furkan replied:

> i dont remember if you want just just restart

The project was therefore restarted from CodePath's official starter, leaving
the playlist lab untouched. No individual test-generation prompts, separate
bug-chat sessions, manual corrections, or second-model responses are invented
here: the testing and implementation were performed under the broad request.

## Agent Workflow

Codex read the assignment and rubric, cloned the starter, and ran the original
tests and two controlled AppTest games. It created the reproduction script,
saved the observed output, marked the faulty areas, and committed evidence and
regression tests before repairing the app. It then moved pure game rules to
`logic_utils.py`, repaired callbacks and state in `app.py`, and ran the tests.
Finally it checked a real Chrome game and wrote the walkthrough and reflection.

Files modified or created: `app.py`, `logic_utils.py`, `reflection.md`,
`README.md`, `ai_interactions.md`, `requirements.txt`,
`tests/test_regressions.py`, `tests/test_app.py`,
`tools/reproduce_starter.py`, and the evidence files.
The original `tests/test_game_logic.py` was preserved unchanged.

Feature expansion: the previously debug-only history is now a player-visible
table with attempt, guess, outcome, and score. Validation feedback, current
metrics, and finished-game controls also improve the UI.

Manual student corrections to code: none reported in this restarted version.
Student decision: use a fresh starter rather than try to recover prior work.
Codex ran the automated and browser checks; these are not attributed to Furkan.

## Edge-Case Test Generation

Prompt context: the actual completion request quoted above, together with the
assignment's request for pytest verification. Codex chose the following cases
from the observed failures; there was no separate student-authored prompt for
each case.

| Edge case | Generated check | Why it matters | Result |
|---|---|---|---|
| `None`, empty string, whitespace | Reject with an error | Blank submissions must not consume a turn | Pass |
| `abc` | Reject and keep attempts/history/score unchanged | Starter incremented attempts before validation | Pass |
| `3.9`, `50.0` | Reject non-integer strings | Starter silently truncated decimal guesses | Pass |
| `-1`, `0`, `101` on Normal | Reject numbers outside 1–100 | A valid integer can still be an invalid game guess | Pass |
| `1`, `100`, padded ` 50 ` | Accept boundaries and surrounding whitespace | Guard against rejecting valid input during validation repair | Pass |
| Last allowed guess equals secret | Win, not loss | End-of-round checks must prioritize a correct answer | Pass |
| Win/loss followed by New Game | Clear the full round | Starter left terminal status and history behind | Pass |

Actual test output is in `test_results.txt` and the README: 33 passed.

## Suggestions Reconsidered

- The starter's docstring describes a `(outcome, message)` tuple, but its three
  tests expect a plain outcome string. Codex preserved the existing tests and
  kept display messages in the UI rather than changing the tests to fit the
  old implementation. The three starter tests now pass unchanged.
- The starter README says the secret resets on each click. The source already
  initializes it conditionally in session state. Codex documented the actual
  reset/difficulty bugs instead of repeating that unsupported claim.
- The first automated reproduction hit the test runner's short startup timeout;
  Codex increased the AppTest timeout to 30 seconds and reran successfully.

These technical revisions were made by Codex. The student's actual revision
to the proposed workflow is documented in `reflection.md` section 2.

## Style and Model Comparison

Codex added docstrings to the pure functions and kept UI/state handling apart
from the rules. No linting-output bonus or second-model comparison is claimed.
