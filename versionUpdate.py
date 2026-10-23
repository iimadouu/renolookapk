import json
import re
from pathlib import Path

#versionUpdate.py is a script that reads the version from pubspec.yaml and writes it to latest.json in the apkrepo directory.

APK_REPO_DIR = Path(__file__).resolve().parent
PUBSPEC_PATH = APK_REPO_DIR.parent / "pubspec.yaml"
LATEST_JSON_PATH = APK_REPO_DIR / "latest.json"
VERSION_PATTERN = re.compile(
    r"""^version:\s*['"]?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+\d+)?)['"]?\s*(?:#.*)?$"""
)


def main() -> None:
    if not PUBSPEC_PATH.is_file():
        raise FileNotFoundError(f"Could not find Flutter version file: {PUBSPEC_PATH}")

    matches = []
    for line in PUBSPEC_PATH.read_text(encoding="utf-8").splitlines():
        match = VERSION_PATTERN.fullmatch(line.strip())
        if match:
            matches.append(match.group(1))

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one valid 'version:' entry in {PUBSPEC_PATH}, "
            f"found {len(matches)}."
        )

    latest = {"version": matches[0]}
    LATEST_JSON_PATH.write_text(
        json.dumps(latest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {LATEST_JSON_PATH} to version {matches[0]}")


if __name__ == "__main__":
    main()