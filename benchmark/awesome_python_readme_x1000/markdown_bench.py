from pathlib import Path

import markdown

MARKDOWN_TEXT = (Path(__file__).parent / "README.md").read_text()


def main():
    N = 10
    for _ in range(N):
        _ = markdown.markdown(MARKDOWN_TEXT)


if __name__ == "__main__":
    main()
