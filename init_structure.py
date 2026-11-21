from pathlib import Path

folders = [
    "docs/decisions", "docs/build-guide",
    "cad/frame", "cad/arm-holder", "cad/arm-prober",
    "cad/printed-parts", "cad/macros",
    "bom",
    "firmware/esp32",
    "software/vision", "software/control",
]
for f in folders:
    p = Path(f)
    p.mkdir(parents=True, exist_ok=True)
    (p / ".gitkeep").touch()   # Git speichert sonst keine leeren Ordner

Path(".gitignore").write_text(
    "__pycache__/\n*.pyc\n.venv/\n.idea/\n.vscode/\n"
    "*.FCStd1\n*.FCBak\n*.stl\n*.step\n.pio/\n"
)
print("Struktur angelegt.")