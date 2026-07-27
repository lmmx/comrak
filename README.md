# comrak

<!-- [![downloads](https://static.pepy.tech/badge/comrak/month)](https://pepy.tech/project/comrak) -->
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![PyPI](https://img.shields.io/pypi/v/comrak.svg)](https://pypi.org/project/comrak)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/comrak.svg)](https://pypi.org/project/comrak)
[![License](https://img.shields.io/pypi/l/comrak.svg)](https://pypi.python.org/pypi/comrak)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lmmx/comrak/master.svg)](https://results.pre-commit.ci/latest/github/lmmx/comrak/master)

Python bindings for the [Comrak Rust library](https://crates.io/crates/comrak), a fast CommonMark/GFM parser.

Currently tracking **comrak 0.54**.

## Installation

```bash
pip install comrak
```

### Requirements

- Python 3.9+

## Usage

```py
>>> import comrak
>>> comrak.render_markdown("# Hello")
'<h1>Hello</h1>\n'
```

### CommonMark output

`render_commonmark` renders Markdown back to normalized CommonMark instead of
HTML. It takes the same `extension_options`/`parse_options`/`render_options`
as `render_markdown`:

```py
>>> comrak.render_commonmark("- one\n- two\n- three")
'- one\n- two\n- three\n'
>>> opts = comrak.RenderOptions()
>>> opts.list_style = comrak.ListStyle.Plus
>>> comrak.render_commonmark("- one\n- two\n- three", render_options=opts)
'+ one\n+ two\n+ three\n'
```

### Options

Every option in comrak's `Extension`, `Parse` and `Render` structs is exposed,
with the same name and the same default:

```py
>>> opts = comrak.ExtensionOptions()
>>> comrak.render_markdown("foo :smile:", extension_options=opts)
'<p>foo :smile:</p>\n'
>>> opts.shortcodes = True
>>> comrak.render_markdown("foo :smile:", extension_options=opts)
'<p>foo 😄</p>\n'
```

The three option objects are independent and can be combined:

```py
>>> ext = comrak.ExtensionOptions()
>>> ext.alerts = True
>>> render = comrak.RenderOptions()
>>> render.alert_style = comrak.AlertStyle.Semantic
>>> comrak.render_markdown("> [!note]\n> Note this!",
...                        extension_options=ext, render_options=render)
'<aside class="admonition note">\n...'
```

For what each option does, see comrak's own
[documentation](https://docs.rs/comrak/latest/comrak/struct.Options.html).
The field names match one-for-one:

- [`options::Extension`](https://docs.rs/comrak/latest/comrak/options/struct.Extension.html)
- [`options::Parse`](https://docs.rs/comrak/latest/comrak/options/struct.Parse.html)
- [`options::Render`](https://docs.rs/comrak/latest/comrak/options/struct.Render.html)

Two options take enums rather than raw values: `RenderOptions.alert_style`
(`comrak.AlertStyle`) and `RenderOptions.list_style` (`comrak.ListStyle`). Both
compare equal to their integer discriminants.

The one naming difference from the Rust API is:

| Rust | Python |
|---|---|
| `render.unsafe` | `RenderOptions.unsafe_` |

`ExtensionOptions.header_ids` is a deprecated alias for `header_id_prefix` and
raises a `FutureWarning`; it will be removed in a future release.

### Not exposed

- `parse.broken_link_callback` — [see tracking issue](https://github.com/lmmx/comrak/issues/58)
- `extension.phoenix_heex` — gated behind a comrak crate feature that isn't built here
- Plugins (syntax highlighting, heading adapters)
- XML output (`comrak::markdown_to_commonmark_xml`)

`render_markdown` renders to HTML. `render_commonmark` renders to normalized
[CommonMark][commonmark]. The options that solely affect the CommonMark formatter (`width`,
`list_style`, `prefer_fenced`, `ol_width`, `experimental_minimize_commonmark`)
have no effect on `render_markdown`'s HTML output, only on `render_commonmark`.

[commonmark]: https://commonmark.org/

## Benchmarks

Tested with small (8 lines) and medium (1200 lines) markdown strings

- vs. [markdown](https://pypi.org/project/markdown): 15x faster (S/M)
- vs. [markdown2](https://pypi.org/project/markdown2): 20x (S) - 60x (M) faster

## Contributing

Maintained by [lmmx](https://github.com/lmmx). Contributions welcome!

1. **Issues & Discussions**: Please open a GitHub issue or discussion for bugs, feature requests, or questions.
2. **Pull Requests**: PRs are welcome!
   - Set up with [uv](https://docs.astral.sh/uv/): `uv sync`
   - Build and test: `uv run maturin develop && uv run pytest`
   - If reporting a bug, please include the version and the error message/traceback if available.

New comrak options are caught at compile time by an exhaustiveness check in
`src/options.rs`, and untested options are caught by `TestOptionCoverage` in
`tests/comrak_test.py`. This was introduced to help keep track of new comrak features
and their test coverage in this library.

## License

Licensed under the 2-Clause BSD License. See [LICENSE](https://github.com/lmmx/comrak/blob/master/LICENSE) for all the details.
