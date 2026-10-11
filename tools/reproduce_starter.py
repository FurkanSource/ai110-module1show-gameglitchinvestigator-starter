"""Reproduce bugs against the original starter, before applying repairs."""

import ast
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import subprocess
import sys

from streamlit.testing.v1 import AppTest


def main():
    """Run deterministic starter games and print the observed failures."""
    source = subprocess.check_output(
        ["git", "show", "f651d72:app.py"], encoding="utf-8"
    )
    tree = ast.parse(source)
    functions = ast.Module(
        body=[node for node in tree.body if isinstance(node, ast.FunctionDef)],
        type_ignores=[],
    )
    namespace = {}
    exec(compile(functions, "app.py", "exec"), namespace)
    print("Original starter bug reproduction; run by Codex, not the student.")
    for guess, secret in [(60, 50), (9, "50"), (100, "50")]:
        print(f"check_guess({guess!r}, {secret!r}) = "
              f"{namespace['check_guess'](guess, secret)!r}")
    print(f"parse_guess('3.9') = {namespace['parse_guess']('3.9')!r}")
    print("update_score(0, 'Too High', 2) = "
          f"{namespace['update_score'](0, 'Too High', 2)}")

    game = AppTest.from_string(source, default_timeout=30).run()
    assert not game.exception
    game.session_state.secret = 50
    print("Game 1: Normal, controlled secret=50")
    print(f"Initial banner: {game.info[0].value}")
    game.text_input[0].set_value("9")
    game.button[0].click().run()
    print(f"Guess 9 -> {game.warning[0].value}; "
          f"attempts={game.session_state.attempts}, "
          f"score={game.session_state.score}")
    game.text_input[0].set_value("50")
    game.button[0].click().run()
    print(f"Guess 50 -> status={game.session_state.status}; "
          f"success={[item.value for item in game.success]}")
    game.button[1].click().run()
    print(f"New Game -> status={game.session_state.status}; "
          f"history={game.session_state.history}; "
          f"success={[item.value for item in game.success]}")

    game = AppTest.from_string(source, default_timeout=30).run()
    game.session_state.secret = 50
    print("Game 2: Normal, controlled secret=50")
    game.text_input[0].set_value("abc")
    for _ in range(9):
        game.button[0].click().run()
    print(f"Nine invalid guesses -> status={game.session_state.status}; "
          f"attempts={game.session_state.attempts}; "
          f"error={game.error[0].value}; banner={game.info[0].value}")
    game.selectbox[0].select("Easy").run()
    print(f"Switch to Easy -> secret={game.session_state.secret}; "
          f"sidebar={[item.value for item in game.sidebar.caption]}; "
          f"banner={game.info[0].value}")
    assert not game.exception


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    output = StringIO()
    with redirect_stdout(output):
        main()
    Path("starter_reproduction.txt").write_text(
        output.getvalue(), encoding="utf-8"
    )
    print(output.getvalue())
