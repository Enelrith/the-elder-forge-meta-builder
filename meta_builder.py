import configparser
from pathlib import Path

PLUGIN_EXTENSIONS = {".esp", ".esl", ".esm"}

def get_mods_folder() -> Path:
    while True:
        raw = input("Enter the path to your /mods folder: ").strip()
        path = Path(raw)
        if not path.exists():
            print(f"Error: Path does not exist: {path}\n")
            continue
        if not path.is_dir():
            print(f"Error: Path is not a folder: {path}\n")
            continue
        return path

def parse_meta_ini(meta_path: Path, link_plugins: bool) -> dict | None:
    parser = configparser.RawConfigParser()
    try:
        parser.read(meta_path, encoding="utf-8")
    except Exception as e:
        print(f"Could not read {meta_path}: {e}")
        return None

    if not parser.has_section("General"):
        return None

    mod_id = parser.get("General", "modid", fallback="").strip()
    nexus_category = parser.get("General", "nexusCategory", fallback="").strip()

    if mod_id == "0":
        return None

    plugins = []
    if link_plugins:
        plugins = [
            f.name
            for f in meta_path.parent.iterdir()
            if f.is_file() and f.suffix.lower() in PLUGIN_EXTENSIONS
        ]

    return {
        "mod_name": meta_path.parent.name,
        "mod_id": mod_id,
        "nexus_category": nexus_category,
        "plugins": plugins,
    }

def scan_mods_folder(mods_folder: Path) -> list[dict]:
    results = []

    user_input = input("Do you want to associate mods with their plugins? (Y/N): ")
    link_plugins = user_input.lower() == "y"

    mod_dirs = sorted(
        [d for d in mods_folder.iterdir() if d.is_dir()],
        key=lambda d: d.name.lower(),
    )
    print(f"\nScanning {len(mod_dirs)} folder(s) in: {mods_folder}\n")

    for mod_dir in mod_dirs:
        meta_path = mod_dir / "meta.ini"
        if not meta_path.exists():
            continue
        parsed = parse_meta_ini(meta_path, link_plugins)
        if parsed is None:
            print(f"  Skipped (no Nexus data): {mod_dir.name}")
            continue
        results.append(parsed)
        print(f"Found: {parsed['mod_name']} (category {parsed['nexus_category']})")

    return results

def write_output(results: list[dict], mods_folder: Path) -> Path:
    output_path = mods_folder / "mod_data.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in results:
            print(f"Writing data for {entry['mod_name']}..")
            line = f"mod_name={entry['mod_name']}|modid={entry['mod_id']}|nexusCategory={entry['nexus_category']}"
            for plugin in entry["plugins"]:
                line += f"|plugin={plugin}"
            f.write(line + "\n")
            print("  Done!")
    return output_path

def main():
    mods_folder = get_mods_folder()
    results = scan_mods_folder(mods_folder)
    if not results:
        print("\nNo Nexus mods found. Nothing to write.")
        input("\nPress enter to exit.")
        return
    output_path = write_output(results, mods_folder)
    print(f"\nDone. {len(results)} mod(s) written to:\n  {output_path}")
    input("\nPress enter to exit.")

if __name__ == "__main__":
    main()