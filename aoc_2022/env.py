from pathlib import Path
from re import findall

env = dict(
    findall(
        r"([^=]+)\s*=\s*([^=\n]+)", (Path(__file__).parent.parent / ".env").read_text()
    )
)
cookies = {"session": env["AOC_SESSION"]}
year = 2022
