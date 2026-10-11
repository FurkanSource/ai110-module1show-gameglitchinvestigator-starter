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

## 2. How did you use AI as a teammate?

I used OpenAI Codex and asked it to finish the October 11 assignment without submitting it. A correct suggestion from Codex was to validate a guess before incrementing attempts and to reset all round state together; its tests confirmed that invalid input keeps all eight Normal attempts and that New Game restores playing status after a win or loss. One proposal I did not accept as written was to build on my earlier fixes: when Codex asked where they were, I said, "i dont remember if you want just just restart," so it used the official starter instead of relying on work I could not identify. Codex also resolved an inconsistency between the starter's tuple-returning app function and its string-expecting tests by preserving the original tests and separating the outcome from the UI message. These code changes and verification runs were performed by Codex; I am not claiming that I independently wrote, reviewed every diff, or manually verified them.

## 3. Debugging and testing your fixes

The verification compared repeatable inputs against expected outputs, rather than assuming the app was correct because it launched. Codex added pytest cases and ran the complete suite: all 33 tests passed, including the original three tests without modifying them. One Streamlit test submits 40, 70, and 50 against secret 50, checks both hint directions, verifies a win with score 80, and then confirms that New Game clears the previous round. Other tests cover invalid input, the exact attempt limit, a last-attempt win, difficulty changes, and reruns caused by toggling hints. Codex also played a real Chrome session with secret 92; the README records the observed guesses and output, rather than attributing that browser run to me.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script after a widget interaction, so a normal local variable does not by itself represent a continuing game. Session state is like a small notebook for the current browser session: it remembers the secret, score, attempts, history, and status across reruns. In this version, callbacks update that notebook before the page is drawn again, which keeps the displayed counter current. Starting another round must reset all related entries together; resetting only the secret and attempts leaves the previous win or loss active. These explanations come from the repaired code and Codex's tests, rather than an independently completed Streamlit exercise.

## 5. Looking ahead: your developer habits

A useful habit from this project is to record the exact input, expected result, and actual result before changing code. That made it possible to check the same cases after the fixes and avoid relying on a generic claim that the game works. A concrete next step for me is to replay the walkthrough and explain `parse_guess`, `check_guess`, and the reset callback before treating this as code I understand. The starter's confident description and misleading hints illustrate why AI-generated code needs evidence and tests; successful output alone does not establish my own understanding. Codex prepared this reflection from the conversation and recorded results, so I still need to review its wording before submitting it as my reflection.
