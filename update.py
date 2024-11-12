#!/usr/bin/python3
#
# A script to import the original icons and patch them by removing the
# recolouring logic for a static version of the Breeze Dark icon theme.
#

import glob
import os
import re
import shutil

COLOUR_MAPPING = {
    # <class>: <colour>

    "ColorScheme-Text": "#fcfcfc",
    "ColorScheme-Accent": "#3daee9",

    "ColorScheme-Highlight": "#3daee9",
    "ColorScheme-Background": "#2a2e32",
    "ColorScheme-ButtonText": "#7B7C7E",

    "ColorScheme-NegativeText": "#da4453",
    "ColorScheme-NeutralText": "#f67400",
    "ColorScheme-PositiveText": "#27ae60",
}

# Fix for BUG 448169
COLOUR_FOLDER_FIX = "#31363b"

SYSTEM_ICONS = "/usr/share/icons/breeze-dark"

FOLDERS = [
    "actions",
    "animations",
    "applets",
    "apps",
    "categories",
    "devices",
    "emblems",
    "emotes",
    "mimetypes",
    "places",
    "preferences",
    "status"
]

for folder in FOLDERS:
    print("Processing:", folder.ljust(70))

    # Update with system icons
    os.system(f"cp -r '{SYSTEM_ICONS}/{folder}' ./")

    # Gather file list
    files = glob.glob(folder + "/**/*.svg", recursive=True)
    for path in files:
        print("->", path[:70].ljust(70), end="\r")
        # Skip symlinks
        if os.path.islink(path):
            continue

        # Skip empty file (upstream bug?)
        if os.path.getsize(path) == 0:
            os.remove(path)
            continue

        with open(path, "r", encoding="utf-8") as f:
            svg = f.read()

        # Use regex to remove <style> and <defs> tags
        svg = re.sub(r'<style[^>]*>.*?</style>', '', svg, flags=re.DOTALL)
        # svg = re.sub(r'<defs[^>]*>.*?</defs>', '', svg, flags=re.DOTALL)

        # Make sure everything between "<path>" and the end tag "/>" are on the same line
        while re.search(r'<path[^>]*\n[^>]*>', svg):
            svg = re.sub(r'(<path[^>]*?)\s*\n\s*([^>]*>)', r'\1 \2', svg, flags=re.DOTALL)

        # Patch "currentColor" fill with the appropriate colour
        new_lines = []
        for line in svg.splitlines():
            if "currentColor" in line:
                for class_name, colour in COLOUR_MAPPING.items():
                    if class_name in line:
                        # Remove class attribute
                        line = line.replace(f"class=\"{class_name}\"", "")
                        line = line.replace("currentColor", colour)

                        # Fix inner icon for folders (BUG 448169)
                        if class_name == "ColorScheme-Text" and "fill-opacity:0.6" in line:
                            line = line.replace(colour, COLOUR_FOLDER_FIX)

                # Not an inline class? Likely defined in the <g> tag
                if "fill:currentColor" in line and not "class=" in line:
                    line = line.replace("currentColor", COLOUR_MAPPING["ColorScheme-Text"])

                # Some files have a class attribute, but no fill style. Add it in, I guess?
                # FIXME: Not working?
                if "class=" in line:
                    class_name = line.split("class=\"")[1].split("\"")[0].strip()
                    if "style=" in line:
                        line = line.replace("style=\"", f"style=\"fill:{COLOUR_MAPPING[class_name]};")
                        line = line.replace(f"class=\"{class_name}\"", "")
                    else:
                        line = line.replace(f"class=\"{class_name}\"", f"fill=\"{COLOUR_MAPPING[class_name]}\"")

            new_lines.append(line)

        # Write patched file
        with open(path, "w", encoding="utf-8") as f:
            for line in new_lines:
                f.write(line.strip() + "\n")

    print(" " * 70, end="\r")

# ====== Restore personal preferences ======
# Prefer 64px version instead of 96px places icons
if os.path.exists("places/96/"):
    shutil.rmtree("places/96/")

# Git folder too thin at 64px; prefer 32px version
os.remove("places/64/folder-git.svg")

# Prefer classic dialog icons
os.system("git checkout status/64/dialog-*.svg")

# Prefer older, lighter black folder icon
os.system("git checkout places/{16,22,24,32,48,64}/folder-black.svg")

# Prefer older list remove icon
os.system("git checkout actions/{16,22}/list-remove.svg actions/{16,22}/list-remove-symbolic.svg")
