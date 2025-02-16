# comrak

<!-- [![downloads](https://static.pepy.tech/badge/comrak/month)](https://pepy.tech/project/comrak) -->
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![PyPI](https://img.shields.io/pypi/v/comrak.svg)](https://pypi.org/project/comrak)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/comrak.svg)](https://pypi.org/project/comrak)
[![License](https://img.shields.io/pypi/l/comrak.svg)](https://pypi.python.org/pypi/comrak)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lmmx/comrak/master.svg)](https://results.pre-commit.ci/latest/github/lmmx/comrak/master)

Python bindings for the Comrak Rust library, a fast CommonMark/GFM parser

## Installation

```bash
pip install comrak
```

### Requirements

- Python 3.9+

## Features

Fast Markdown to HTML parser in Rust, shipped for Python via PyO3.

### Options

All options are exposed in a simple manner:

```py
>>> import comrak
>>> opts = comrak.ExtensionOptions()
>>> comrak.render_markdown("foo :smile:", extension_options=opts)
'<p>foo :smile:</p>\n'
>>> opts.shortcodes = True
>>> comrak.render_markdown("foo :smile:", extension_options=opts)
'<p>foo 😄</p>\n'
```

Refer to the [Comrak docs](https://docs.rs/comrak/latest/comrak/struct.Options.html) for all available options.

## Benchmarks

Tested with small (8 lines) and medium (1200 lines) markdown strings

- vs. [markdown](https://pypi.org/project/markdown): 15x faster (S/M)
- vs. [markdown2](https://pypi.org/project/markdown2): 20x (S) - 60x (M) faster

## Contributing

Maintained by [lmmx](https://github.com/lmmx). Contributions welcome!

1. **Issues & Discussions**: Please open a GitHub issue or discussion for bugs, feature requests, or questions.
2. **Pull Requests**: PRs are welcome!
   - Install the dev extra (e.g. with [uv](https://docs.astral.sh/uv/): `uv pip install -e .[dev]`)
   - Run tests (when available) and include updates to docs or examples if relevant.
   - If reporting a bug, please include the version and the error message/traceback if available.

## License

Licensed under the 2-Clause BSD License. See [LICENSE](https://github.com/lmmx/comrak/blob/master/LICENSE) for all the details.
