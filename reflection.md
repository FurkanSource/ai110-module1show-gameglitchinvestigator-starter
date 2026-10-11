# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

I remembered fixing some bugs earlier, but could not locate those changes, so I asked Codex to restart from the official starter. Codex ran two controlled games using Streamlit's AppTest, with the secret set to 50 so the results were reproducible. The first game exposed incorrect comparisons and a New Game button that left the game won; the second exposed invalid guesses consuming attempts and a difficulty change keeping an impossible secret. The records below are observations from Codex's runs, not a claim that I personally played those sessions.

### Bug Reproduction Logs

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
|---|---|---|---|
| `check_guess(60, 50)` | Too High; tell player to go lower | Outcome says Too High but hint says HIGHER | `('Too High', '📈 Go HIGHER!')` |
| First Normal guess `9`, secret `50` | Too Low; numeric comparison | App casts secret to text on even attempts; `'9' > '50'` becomes true | `check_guess(9, '50') = ('Too High', '📈 Go HIGHER!')`; score becomes 5 |
| Enter `3.9` | Reject a non-integer | Truncates to 3 and accepts it | `(True, 3, None)` |
| Wrong high guess on attempt 2, score 0 | No reward for a wrong guess | Adds 5 points | `update_score(0, 'Too High', 2) = 5` |
| Start a Normal game | Eight attempts available | Counter starts at 1, so banner shows seven | `Attempts left: 7` |
| Win with `50`, then click New Game | Playing, empty history, fresh score | Status stays won and history remains | `status=won; history=[9, 50]`; `You already won. Start a new game to play again.` |
| Enter `abc` nine times | Validation error without spending attempts | Counter rises to 10; game still playing; remaining attempts negative | `That is not a number.`; `Attempts left: -1` |
| Change Normal to Easy with secret 50 | New secret between 1 and 20; matching instructions | Secret remains 50 and main instructions still say 1–100 | Sidebar `Range: 1 to 20`; main banner `Guess a number between 1 and 100` |

The code-level causes were reversed messages in `check_guess`, string conversion before comparison, decimal truncation in `parse_guess`, an even-attempt reward in `update_score`, and incomplete session-state initialization/reset in `app.py`. Invalid input incremented the counter before validation, while the loss check only ran for valid guesses. The starter README's claim that the secret changes on every click was not supported by this version: it already initialized the secret only when absent from session state.

Actual output: [starter_reproduction.txt](starter_reproduction.txt). Original baseline: CodePath commit `f651d72`; the reproduction script loads that version even after the fixes. The three original tests also failed with `NotImplementedError` before repairs; see [starter_test_results.txt](starter_test_results.txt).
