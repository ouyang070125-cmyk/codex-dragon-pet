---
name: install-gpt-dragon-pet
description: Install the bundled GPT Dragon Girl dragon companion into the local Codex desktop pet picker when the user requests this pet or its installation.
---

# Install GPT Dragon Girl

This skill includes the desktop v2 pet under `assets/gpt-dragon`.

Run `python <this-skill-directory>/scripts/install_pet.py`. It uses `CODEX_HOME/pets` when set, otherwise `~/.codex/pets`. Installation uses Python's standard library and works offline.

An identical installation succeeds without changes. If the same pet ID has different files, report the conflict; do not overwrite or remove it. Report any other installation error as a failure.

After success, ask the user to open Settings > Pets, refresh, and select GPT龙娘. The script does not change the active pet. Do not claim selection or animation was verified from file installation alone.

The image is the desktop 1536×2288 v2 layout. Keep row 0 column 6 as its reserved neutral look frame; it is not an idle-loop frame. Do not convert it using a web-upload validator or upload it to a cloud pet library as part of installation.
