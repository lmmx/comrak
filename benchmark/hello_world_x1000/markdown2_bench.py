import markdown2

MARKDOWN_TEXT = """
# Example

This is **bold** text with [a link](https://example.com).
And some list:
- item1
- item2

The end.
"""


def main():
    N = 1000
    for _ in range(N):
        _ = markdown2.markdown(MARKDOWN_TEXT)


if __name__ == "__main__":
    main()
