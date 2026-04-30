from pathlib import Path
import re


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", text, re.MULTILINE)
    if m:
        return m.group(1)
    h1 = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if h1:
        return h1.group(1)
    return path.stem


def main() -> None:
    root = Path("knowledge")
    lines = ["# Knowledge Index", ""]
    for path in sorted(root.rglob("*.md")):
        if path.name == "README.md":
            continue
        title = extract_title(path)
        rel = path.as_posix()
        lines.append(f"- [{title}]({rel})")
    Path("knowledge/INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Updated knowledge/INDEX.md")


if __name__ == "__main__":
    main()
