"""Install the bundled pet without changing the active selection or overwriting another pet."""
import argparse
import json
import os
from pathlib import Path
import shutil


def install(pets_dir):
    source = Path(__file__).resolve().parents[1] / 'assets' / 'gpt-dragon'
    manifest = json.loads((source / 'pet.json').read_text(encoding='utf-8'))
    target = pets_dir / manifest['id']
    names = ['pet.json', 'spritesheet.webp']
    if target.exists():
        if not target.is_dir() or target.is_symlink() or any(
            not (target / n).is_file() or (target / n).is_symlink()
            or (target / n).read_bytes() != (source / n).read_bytes() for n in names
        ):
            raise FileExistsError(f'Different content already exists; nothing overwritten: {target}')
        print(f'Already installed: {target}')
        return
    pets_dir.mkdir(parents=True, exist_ok=True)
    # mkdir without exist_ok prevents accidental replacement if another installer wins the race.
    target.mkdir()
    for name in names:
        shutil.copyfile(source / name, target / name)
    print(f'Installed: {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pets-dir', type=Path, default=Path(os.environ.get('CODEX_HOME') or Path.home()/'.codex')/'pets')
    args = parser.parse_args()
    try:
        install(args.pets_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')
