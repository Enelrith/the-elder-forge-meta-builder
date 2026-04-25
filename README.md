# Elder Forge — Meta Builder

A lightweight CLI tool that scans your **Mod Organizer 2** mods folder, reads each mod's `meta.ini` file, and produces a `mod_data.txt` file containing the Nexus mod ID, category, and optionally the associated plugin files for each mod.

This file is consumed by the [Elder Forge](https://github.com/enelrith/theelderforge) web application to enrich your modlist with category data and mod/plugin associations.

---

## Requirements

- Windows 10 or later
- No installation required — just download and run the `.exe`

---

## Download

Download the latest release from the [Releases](https://github.com/enelrith/theelderforge/releases) page.

> **Note:** Windows SmartScreen may show a warning on first launch. This is a known false positive with PyInstaller-packaged executables. Click **More info → Run anyway** to proceed.

You can verify the file integrity using the SHA-256 checksum provided on the release page:

```
# Run this in PowerShell to verify
certutil -hashfile ElderForge-MetaBuilder.exe SHA256
```

---

## Usage

1. **Run** `ElderForge-MetaBuilder.exe`
2. **Enter the path** to your MO2 `/mods` folder when prompted, for example:
   ```
   C:\Modding\MO2\mods
   ```
3. **Choose** whether to include mod/plugin associations (`Y/N`)
4. The tool writes `mod_data.txt` directly into your `/mods` folder

---

## Output Format

Each line in `mod_data.txt` represents one mod:

**Without plugin associations:**

```
mod_name=Apothecary - An Alchemy Overhaul modid=52130 nexusCategory=94
```

**With plugin associations:**

```
mod_name=Apothecary - An Alchemy Overhaul modid=52130 nexusCategory=94 plugin=Apothecary.esp plugin=Apothecary - Food.esp
```

### Fields

| Field           | Description                                                                         |
| --------------- | ----------------------------------------------------------------------------------- |
| `mod_name`      | The name of the mod folder in MO2                                                   |
| `modid`         | The Nexus Mods mod ID                                                               |
| `nexusCategory` | The Nexus category ID (e.g. `94` = Alchemy)                                         |
| `plugin`        | Plugin file(s) belonging to the mod (`.esp`, `.esm`, `.esl`) — one field per plugin |

### Skipped mods

Mods are skipped if they:

- Have no `meta.ini` file (separators, local mods)
- Have `modid=0` (mods not sourced from Nexus)

---

## Where is my MO2 mods folder?

Open Mod Organizer 2, go to **Tools → Settings → Paths**. The **Mods** field shows the full path. It is typically something like:

```
C:\Modding\MO2\mods
```

or inside your game folder:

```
C:\Games\Steam\steamapps\common\Skyrim Special Edition\MO2\mods
```

---

## Building from Source

Requires Python 3.10+.

```bash
# Clone the repo
git clone https://github.com/enelrith/theelderforge.git
cd theelderforge/tools/meta-builder

# Run directly
python meta_builder.py

# Build the exe
pip install pyinstaller
pyinstaller --onefile --name "ElderForge-MetaBuilder" meta_builder.py
# Output: dist/ElderForge-MetaBuilder.exe
```

---
