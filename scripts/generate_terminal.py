"""
Regenerates assets/terminal.gif -- a self-hosted, self-drawn retro
terminal boot + neofetch animation. No third-party badge services,
no external rendering endpoints: this repo owns the whole asset.

Run locally:
    pip install github-readme-terminal
    python scripts/generate_terminal.py

Wired into .github/workflows/terminal.yml to re-run on a schedule
so the "live" line below stays fresh without you touching it.
"""

import os
import pathlib

import requests

# ---- provision gifos config before importing it (module reads config on import) ----
CONFIG_DIR = pathlib.Path.home() / ".config" / "gifos"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

(CONFIG_DIR / "gifos_settings.toml").write_text("""
[general]
debug = false
cursor = "_"
show_cursor = true
blink_cursor = true
user_name = "sam"
fps = 12
color_scheme = "candlelit_library"

[files]
frame_base_name = "frame_"
frame_folder_name = "frames"
output_gif_name = "terminal"
""")

(CONFIG_DIR / "ansi_escape_colors.toml").write_text("""
[candlelit_library]
    [candlelit_library.default_colors]
    fg = "#f0d9b5"
    bg = "#14100b"

    [candlelit_library.normal_colors]
    black = "#2b2118"
    red = "#c4653c"
    green = "#a8935a"
    yellow = "#e8a33d"
    blue = "#6b5842"
    magenta = "#b3703f"
    cyan = "#8a7454"
    white = "#f0d9b5"

    [candlelit_library.bright_colors]
    black = "#3d2f22"
    red = "#e0824f"
    green = "#c9b273"
    yellow = "#ffb300"
    blue = "#8a765c"
    magenta = "#d1895a"
    cyan = "#a68f6c"
    white = "#fff3da"
""")

import gifos  # noqa: E402  (must come after config files are written)

AMBER, RUST, DIM, OK, R = "\x1b[93m", "\x1b[91m", "\x1b[36m", "\x1b[92m", "\x1b[0m"
USERNAME = "Sam97300"


def fetch_live_line() -> str:
    """Best-effort live GitHub stats line. Falls back to a static one
    if the API is unreachable or rate-limited -- never breaks the build."""
    try:
        headers = {"Accept": "application/vnd.github+json"}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        r = requests.get(
            f"https://api.github.com/users/{USERNAME}", headers=headers, timeout=8
        )
        r.raise_for_status()
        data = r.json()
        return f"public repos: {data['public_repos']}   followers: {data['followers']}"
    except Exception:
        return "(stats offline -- API was napping, try the profile directly)"


def main():
    t = gifos.Terminal(width=760, height=460, xpad=16, ypad=16, line_spacing=6)
    t.set_prompt(f"{RUST}sam{R}@{AMBER}pccoe{R}:~$ ")

    # ---- scene 1: boot ----
    t.gen_text(f"{AMBER}CANDLELIT-BIOS{R} v0.9 -- sam97300/systems", 1)
    t.clone_frame(6)
    t.gen_text(f"Initializing amber phosphor array ......... {OK}OK{R}", 2)
    t.clone_frame(6)
    t.gen_text(f"Mounting /home/sam ......................... {OK}OK{R}", 3)
    t.clone_frame(6)
    t.gen_text(f"Loading rice: candlelit_library ............ {OK}OK{R}", 4)
    t.clone_frame(6)
    t.gen_text(f"Scanning for unfinished side projects ...... {RUST}FOUND 6{R}", 5)
    t.clone_frame(20)
    t.clear_frame()

    # ---- scene 2: login + neofetch ----
    t.gen_text(f"pccoe login: {AMBER}sam{R}", 1)
    t.clone_frame(6)
    t.gen_text("Password: ************", 2)
    t.clone_frame(6)
    t.gen_text(f"{DIM}Last login: just now, from a diploma topper's laptop{R}", 3)
    t.clone_frame(10)
    t.gen_typing_text(f"{RUST}sam{R}@{AMBER}pccoe{R}:~$ neofetch", 5, speed=2)
    t.clone_frame(10)

    fields = [
        ("OS", "Fedora / Bazzite (whichever boots first)"),
        ("Host", "HP OMEN -- i7-14650HX, RTX 4060"),
        ("Shell", "bash (zsh / fish / nu on standby)"),
        ("Terminal", "WezTerm"),
        ("Theme", "Candlelit Library -- amber, obviously"),
        ("Editor", "Neovim + Zed, both hand-configured"),
        ("Role", "Director of LLM & CLI tools"),
        ("Status", "B.Tech via DSE @ PCCOE, IT branch"),
    ]
    row = 7
    for label, value in fields:
        t.gen_text(f"{AMBER}{label}{R}: {value}", row)
        row += 1
    t.clone_frame(30)
    t.clear_frame()

    # ---- scene 3: live stats ----
    t.gen_typing_text(f"{RUST}sam{R}@{AMBER}pccoe{R}:~$ curl api.github.com/users/sam97300", 1, speed=2)
    t.clone_frame(8)
    t.gen_text(f"{DIM}{fetch_live_line()}{R}", 3)
    t.clone_frame(30)
    t.gen_prompt(5, 1, 1)
    t.clone_frame(20)
    t.clear_frame()

    # ---- scene 4: roadmap ----
    t.gen_typing_text(f"{RUST}sam{R}@{AMBER}pccoe{R}:~$ cat roadmap.txt", 1, speed=2)
    t.clone_frame(8)
    roadmap = [
        "[ ] Tails OS & Qubes OS",
        "[ ] Linux internals, properly this time",
        "[ ] Google Cloud (currently in the beginner course)",
        "[ ] AWS + IBM Cloud + IBM Quantum -- all in progress",
        "[ ] HackTheBox / TryHackMe / pwn.college",
        "[ ] quantum cloud infra -- the long-horizon obsession",
    ]
    row = 3
    for line in roadmap:
        t.gen_text(f"{DIM}{line}{R}", row)
        row += 1
    t.clone_frame(10)
    t.gen_prompt(row + 1, 1, 1)
    t.clone_frame(30)

    t.gen_gif()


if __name__ == "__main__":
    main()
