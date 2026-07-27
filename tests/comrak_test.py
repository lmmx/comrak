"""Test suite for the comrak Python bindings.

Organised by option struct. Within each struct, options are grouped by what
they need in order to be observable in HTML output:

* toggles with a self-contained markdown/HTML signature live in a table,
  driven by ``assert_toggle`` (off -> absent, on -> present);
* options with prerequisites or non-boolean values get their own test;
* options that only affect the CommonMark formatter are tested against
  ``render_commonmark`` rather than ``render_markdown``.

``TestOptionCoverage`` asserts every public attribute is accounted for.
"""

import comrak
import pytest

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


def assert_toggle(options_kwarg, attr, markdown, expected, **prerequisites):
    """Assert an option is inert when off and takes effect when on.

    Guards against the failure mode where an option is exposed to Python but
    never copied through to the underlying comrak options struct: a one-sided
    assertion would pass, this will not.
    """
    opts = getattr(comrak, options_kwarg)()
    for name, value in prerequisites.items():
        setattr(opts, name, value)

    before = comrak.render_markdown(markdown, **{_KWARG[options_kwarg]: opts})
    assert expected not in before, f"{attr} appears to be on by default"

    setattr(opts, attr, True)
    after = comrak.render_markdown(markdown, **{_KWARG[options_kwarg]: opts})
    assert expected in after, f"{attr} is settable but has no effect"


_KWARG = {
    "ExtensionOptions": "extension_options",
    "ParseOptions": "parse_options",
    "RenderOptions": "render_options",
}


def assert_round_trip(options_kwarg, attr, value):
    """Assert an option stores and returns a value.

    Used for options whose effect is not visible in HTML output.
    """
    opts = getattr(comrak, options_kwarg)()
    setattr(opts, attr, value)
    assert getattr(opts, attr) == value


# --------------------------------------------------------------------------
# Core rendering
# --------------------------------------------------------------------------


class TestRendering:
    """Rendering with no options set."""

    def test_heading(self):
        assert comrak.render_markdown("# Hello") == "<h1>Hello</h1>\n"

    def test_emphasis(self):
        result = comrak.render_markdown("**bold** and *italic*")
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result

    def test_nested_emphasis(self):
        result = comrak.render_markdown("**bold with *italic* inside**")
        assert "<strong>" in result
        assert "<em>" in result

    def test_link(self):
        result = comrak.render_markdown("[link](https://example.com)")
        assert '<a href="https://example.com">link</a>' in result

    def test_list(self):
        result = comrak.render_markdown("- item1\n- item2")
        assert "<ul>" in result
        assert "<li>item1</li>" in result
        assert "<li>item2</li>" in result

    def test_code_block(self):
        result = comrak.render_markdown("```python\nprint('hello')\n```")
        assert "<pre>" in result
        assert "<code" in result

    def test_empty_string(self):
        assert comrak.render_markdown("") == ""

    def test_document_structure(self):
        markdown = "# Title\n\nA paragraph.\n\n## Subtitle\n\nAnother paragraph."
        result = comrak.render_markdown(markdown)
        assert "<h1>Title</h1>" in result
        assert "<h2>Subtitle</h2>" in result
        assert "<p>A paragraph.</p>" in result

    def test_html_is_scrubbed_by_default(self):
        result = comrak.render_markdown('<script>alert("xss")</script>')
        assert "<script>" not in result

    def test_unicode_is_preserved(self):
        result = comrak.render_markdown("# 你好 World 🌍")
        assert "你好" in result
        assert "🌍" in result

    def test_special_characters_are_escaped(self):
        result = comrak.render_markdown("Test & test < test > test")
        assert "&amp;" in result

    def test_large_document(self):
        markdown = "\n".join(f"# Heading {i}" for i in range(1000))
        assert comrak.render_markdown(markdown).count("<h1>") == 1000


# --------------------------------------------------------------------------
# ExtensionOptions
# --------------------------------------------------------------------------

#: Extensions whose effect is a self-contained markdown -> HTML signature.
EXTENSION_TOGGLES = [
    pytest.param(
        "strikethrough", "~~struck~~", "<del>struck</del>", id="strikethrough"
    ),
    pytest.param("table", "| a | b |\n|---|---|\n| c | d |", "<table>", id="table"),
    pytest.param(
        "autolink",
        "https://example.com",
        '<a href="https://example.com">',
        id="autolink",
    ),
    pytest.param("superscript", "e = mc^2^", "<sup>2</sup>", id="superscript"),
    pytest.param("subscript", "H~2~O", "<sub>2</sub>", id="subscript"),
    pytest.param("underline", "__underlined__", "<u>underlined</u>", id="underline"),
    pytest.param("spoiler", "it is ||him||", '<span class="spoiler">', id="spoiler"),
    pytest.param("subtext", "-# subtext", "<sub>subtext</sub>", id="subtext"),
    pytest.param(
        "highlight", "==important==", "<mark>important</mark>", id="highlight"
    ),
    pytest.param("insert", "++added++", "<ins>added</ins>", id="insert"),
    pytest.param(
        "block_directive",
        ":::warning\npara\n:::",
        '<div class="warning">',
        id="block_directive",
    ),
    pytest.param(
        "description_lists", "Term\n\n: Definition", "<dl>", id="description_lists"
    ),
    pytest.param("shortcodes", "foo :smile:", "😄", id="shortcodes"),
    pytest.param(
        "math_dollars", "$1 + 2$", 'data-math-style="inline"', id="math_dollars"
    ),
    pytest.param("math_code", "$`1 + 2`$", "<code data-math-style=", id="math_code"),
    pytest.param("alerts", "> [!note]\n> Note this!", "markdown-alert", id="alerts"),
    pytest.param("greentext", ">implying", "<p>&gt;implying", id="greentext"),
    pytest.param(
        "cjk_friendly_emphasis",
        "**この文は重要です。**但这句话并不重要。",
        "<strong>この文は重要です。</strong>",
        id="cjk_friendly_emphasis",
    ),
    pytest.param(
        "wikilinks_title_after_pipe",
        "[[url|label]]",
        'data-wikilink="true"',
        id="wikilinks_title_after_pipe",
    ),
    pytest.param(
        "wikilinks_title_before_pipe",
        "[[label|url]]",
        'data-wikilink="true"',
        id="wikilinks_title_before_pipe",
    ),
]


class TestExtensionOptions:
    """Extensions with a self-contained signature."""

    @pytest.mark.parametrize(("attr", "markdown", "expected"), EXTENSION_TOGGLES)
    def test_toggle(self, attr, markdown, expected):
        assert_toggle("ExtensionOptions", attr, markdown, expected)

    def test_tagfilter(self):
        """Filtering only applies to raw HTML, so it needs unsafe rendering."""
        e_opts = comrak.ExtensionOptions()
        r_opts = comrak.RenderOptions()
        r_opts.unsafe_ = True

        markdown = "Hello <xmp>."
        before = comrak.render_markdown(
            markdown, extension_options=e_opts, render_options=r_opts
        )
        assert "<xmp>" in before

        e_opts.tagfilter = True
        after = comrak.render_markdown(
            markdown, extension_options=e_opts, render_options=r_opts
        )
        assert "&lt;xmp>" in after

    def test_tasklist(self):
        assert_toggle(
            "ExtensionOptions",
            "tasklist",
            "- [ ] Unchecked\n- [x] Checked",
            'type="checkbox"',
        )

    def test_multiline_block_quotes(self):
        """Checked by exact output: ``>>>`` nests blockquotes when disabled."""
        opts = comrak.ExtensionOptions()
        opts.multiline_block_quotes = True
        result = comrak.render_markdown(">>>\nparagraph\n>>>", extension_options=opts)
        assert result == "<blockquote>\n<p>paragraph</p>\n</blockquote>\n"

    def test_front_matter_delimiter(self):
        opts = comrak.ExtensionOptions()
        markdown = "---\nlayout: post\n---\nText\n"

        assert "layout: post" in comrak.render_markdown(
            markdown, extension_options=opts
        )

        opts.front_matter_delimiter = "---"
        result = comrak.render_markdown(markdown, extension_options=opts)
        assert "layout: post" not in result
        assert "Text" in result

    def test_wikilinks_after_pipe_takes_precedence(self):
        """Documented precedence: after-pipe wins when both are enabled."""
        opts = comrak.ExtensionOptions()
        opts.wikilinks_title_after_pipe = True
        opts.wikilinks_title_before_pipe = True
        result = comrak.render_markdown("[[url|label]]", extension_options=opts)
        assert 'href="url"' in result
        assert ">label<" in result

    def test_math_latex(self):
        """LaTeX-style delimiters as an alternative to ``math_dollars``."""
        opts = comrak.ExtensionOptions()
        opts.math_latex = True
        result = comrak.render_markdown(r"\(1 + 2\)", extension_options=opts)
        assert '<span data-math-style="inline">1 + 2</span>' in result

    def test_heading_anchor_markup(self):
        """Exact markup, since this is what downstream sanitisers see."""
        opts = comrak.ExtensionOptions()
        opts.header_id_prefix = "user-content-"
        opts.header_id_prefix_in_href = True
        assert comrak.render_markdown("# README", extension_options=opts) == (
            '<h1 id="user-content-readme">README'
            '<a href="#user-content-readme" aria-label="Link to heading \'README\'"'
            ' data-heading-content="README" class="anchor"></a></h1>\n'
        )


class TestFootnotes:
    """``inline_footnotes`` requires ``footnotes``, so they are tested together."""

    def test_footnotes(self):
        assert_toggle(
            "ExtensionOptions",
            "footnotes",
            "Text[^1]\n\n[^1]: A note.",
            "footnote-ref",
        )

    def test_inline_footnotes(self):
        assert_toggle(
            "ExtensionOptions",
            "inline_footnotes",
            "Hi^[An inline note].",
            "footnote-ref",
            footnotes=True,
        )

    def test_inline_footnotes_require_footnotes(self):
        opts = comrak.ExtensionOptions()
        opts.inline_footnotes = True
        result = comrak.render_markdown("Hi^[An inline note].", extension_options=opts)
        assert "footnote-ref" not in result


class TestHeaderIds:
    """Anchor generation, and prefixing of the generated ``id`` and ``href``."""

    PREFIX = "user-content-"

    def test_prefix_applies_to_id_only(self):
        opts = comrak.ExtensionOptions()
        opts.header_id_prefix = self.PREFIX
        result = comrak.render_markdown("# README", extension_options=opts)
        assert 'id="user-content-readme"' in result
        assert 'href="#readme"' in result

    def test_prefix_in_href_applies_to_both(self):
        opts = comrak.ExtensionOptions()
        opts.header_id_prefix = self.PREFIX
        opts.header_id_prefix_in_href = True
        result = comrak.render_markdown("# README", extension_options=opts)
        assert 'id="user-content-readme"' in result
        assert 'href="#user-content-readme"' in result

    def test_prefix_in_href_is_inert_without_a_prefix(self):
        opts = comrak.ExtensionOptions()
        opts.header_id_prefix_in_href = True
        result = comrak.render_markdown("# README", extension_options=opts)
        assert "user-content-" not in result

    def test_footnote_ids_are_not_prefixed(self):
        """Downstream link rewriting relies on footnotes being left alone."""
        opts = comrak.ExtensionOptions()
        opts.header_id_prefix = self.PREFIX
        opts.header_id_prefix_in_href = True
        opts.footnotes = True
        result = comrak.render_markdown(
            "# Title\n\nText[^1]\n\n[^1]: A note.", extension_options=opts
        )
        assert 'href="#user-content-title"' in result
        assert 'href="#fn-1"' in result
        assert "user-content-fn-1" not in result


class TestUrlRewriters:
    """Link and image URL rewriting via Python callables."""

    def test_link_rewriter(self):
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: f"https://proxy.example.com?url={url}"
        result = comrak.render_markdown(
            "[my link](http://example.com)", extension_options=opts
        )
        assert "https://proxy.example.com?url=http://example.com" in result

    def test_image_rewriter(self):
        opts = comrak.ExtensionOptions()
        opts.image_url_rewriter = lambda url: f"https://cdn.example.com?u={url}"
        result = comrak.render_markdown(
            "![alt](http://example.com/i.png)", extension_options=opts
        )
        assert "https://cdn.example.com?u=http://example.com/i.png" in result

    def test_rewriters_are_independent(self):
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: "LINK"
        result = comrak.render_markdown(
            "![alt](http://example.com/i.png)", extension_options=opts
        )
        assert "http://example.com/i.png" in result

        opts = comrak.ExtensionOptions()
        opts.image_url_rewriter = lambda url: "IMAGE"
        result = comrak.render_markdown(
            "[link](http://example.com)", extension_options=opts
        )
        assert "http://example.com" in result

    def test_rewriter_can_be_cleared(self):
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: "REWRITTEN"
        opts.link_url_rewriter = None
        result = comrak.render_markdown(
            "[link](http://example.com)", extension_options=opts
        )
        assert "http://example.com" in result

    def test_rewriter_applies_to_every_link(self):
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: url.replace("http://", "https://")
        markdown = "[1](http://a.com)\n[2](http://b.com)\n[3](https://c.com)"
        result = comrak.render_markdown(markdown, extension_options=opts)
        assert "http://" not in result
        assert result.count("https://") == 3

    @pytest.mark.parametrize(
        "rewriter",
        [
            pytest.param(lambda url: 42, id="returns-int"),
            pytest.param(lambda url: None, id="returns-none"),
            pytest.param(lambda url: [url], id="returns-list"),
        ],
    )
    def test_non_string_return_falls_back(self, rewriter):
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = rewriter
        result = comrak.render_markdown(
            "[link](http://example.com)", extension_options=opts
        )
        assert "http://example.com" in result

    def test_raising_rewriter_falls_back(self):
        def bad(url):
            raise ValueError("Something went wrong")

        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = bad
        result = comrak.render_markdown(
            "[link](http://example.com)", extension_options=opts
        )
        assert "http://example.com" in result


# --------------------------------------------------------------------------
# ParseOptions
# --------------------------------------------------------------------------


class TestParseOptions:
    def test_smart_punctuation(self):
        opts = comrak.ParseOptions()
        opts.smart = True
        result = comrak.render_markdown("'Hello,' \"world\" ...", parse_options=opts)
        assert "‘Hello,’" in result
        assert "“world”" in result
        assert "…" in result

    def test_default_info_string(self):
        opts = comrak.ParseOptions()
        markdown = "```\nx = 1\n```"

        assert "language-python" not in comrak.render_markdown(
            markdown, parse_options=opts
        )

        opts.default_info_string = "python"
        assert "language-python" in comrak.render_markdown(markdown, parse_options=opts)

    def test_ignore_setext(self):
        opts = comrak.ParseOptions()
        markdown = "Title\n====="

        assert "<h1>" in comrak.render_markdown(markdown, parse_options=opts)

        opts.ignore_setext = True
        assert "<h1>" not in comrak.render_markdown(markdown, parse_options=opts)

    def test_relaxed_autolinks(self):
        e_opts = comrak.ExtensionOptions()
        e_opts.autolink = True
        p_opts = comrak.ParseOptions()
        markdown = "http://localhost"

        before = comrak.render_markdown(
            markdown, extension_options=e_opts, parse_options=p_opts
        )
        assert "<a href=" not in before

        p_opts.relaxed_autolinks = True
        after = comrak.render_markdown(
            markdown, extension_options=e_opts, parse_options=p_opts
        )
        assert "<a href=" in after

    def test_relaxed_tasklist_matching(self):
        e_opts = comrak.ExtensionOptions()
        e_opts.tasklist = True
        p_opts = comrak.ParseOptions()
        markdown = "- [~] Partially done"

        before = comrak.render_markdown(
            markdown, extension_options=e_opts, parse_options=p_opts
        )
        assert 'type="checkbox"' not in before

        p_opts.relaxed_tasklist_matching = True
        after = comrak.render_markdown(
            markdown, extension_options=e_opts, parse_options=p_opts
        )
        assert 'type="checkbox"' in after

    def test_tasklist_in_table(self):
        e_opts = comrak.ExtensionOptions()
        e_opts.tasklist = True
        e_opts.table = True
        p_opts = comrak.ParseOptions()
        markdown = "| val |\n| - |\n| [ ] |\n"

        before = comrak.render_markdown(
            markdown, extension_options=e_opts, parse_options=p_opts
        )
        assert "<td>[ ]</td>" in before

        p_opts.tasklist_in_table = True
        after = comrak.render_markdown(
            markdown, extension_options=e_opts, parse_options=p_opts
        )
        assert '<td>\n<input type="checkbox" disabled="" /> </td>' in after

    def test_escaped_char_spans(self):
        """Auto-enabled by the render option; not independently observable."""
        assert_round_trip("ParseOptions", "escaped_char_spans", True)

    def test_sourcepos_chars(self):
        r_opts = comrak.RenderOptions()
        r_opts.sourcepos = True
        p_opts = comrak.ParseOptions()
        markdown = "# 你好"

        assert 'data-sourcepos="1:1-1:8"' in comrak.render_markdown(
            markdown, parse_options=p_opts, render_options=r_opts
        )

        p_opts.sourcepos_chars = True
        assert 'data-sourcepos="1:1-1:4"' in comrak.render_markdown(
            markdown, parse_options=p_opts, render_options=r_opts
        )

    def test_leave_footnote_definitions(self):
        """Only observable through a custom formatter; round-tripped here."""
        assert_round_trip("ParseOptions", "leave_footnote_definitions", True)


# --------------------------------------------------------------------------
# RenderOptions
# --------------------------------------------------------------------------

#: Render options observable in HTML output.
RENDER_TOGGLES = [
    pytest.param("hardbreaks", "line1\nline2", "<br", id="hardbreaks"),
    pytest.param(
        "github_pre_lang",
        "```python\nx\n```",
        '<pre lang="python">',
        id="github_pre_lang",
    ),
    pytest.param("sourcepos", "# Hello", "data-sourcepos", id="sourcepos"),
    pytest.param(
        "figure_with_caption", "![alt](x.png)", "<figure>", id="figure_with_caption"
    ),
    pytest.param("ignore_empty_links", "[](foo)", "[](foo)", id="ignore_empty_links"),
]

#: Render options that only affect the CommonMark formatter, exercised
#: against ``render_commonmark`` in ``TestCommonmarkOutput`` below.
COMMONMARK_ONLY_RENDER_OPTIONS = {
    "width": 80,
    "prefer_fenced": True,
    "list_style": comrak.ListStyle.Star,
    "ol_width": 3,
    "experimental_minimize_commonmark": True,
}


class TestRenderOptions:
    @pytest.mark.parametrize(("attr", "markdown", "expected"), RENDER_TOGGLES)
    def test_toggle(self, attr, markdown, expected):
        assert_toggle("RenderOptions", attr, markdown, expected)

    def test_unsafe(self):
        opts = comrak.RenderOptions()
        markdown = '<script>alert("xss")</script>'

        assert "<script>" not in comrak.render_markdown(markdown, render_options=opts)

        opts.unsafe_ = True
        assert "<script>" in comrak.render_markdown(markdown, render_options=opts)

    def test_escape(self):
        opts = comrak.RenderOptions()
        opts.escape = True
        result = comrak.render_markdown("<b>bold</b>", render_options=opts)
        assert "&lt;b&gt;" in result

    def test_escape_takes_precedence_over_unsafe(self):
        opts = comrak.RenderOptions()
        opts.unsafe_ = True
        opts.escape = True
        result = comrak.render_markdown("<b>bold</b>", render_options=opts)
        assert "&lt;b&gt;" in result
        assert "<b>" not in result

    def test_escaped_char_spans(self):
        opts = comrak.RenderOptions()
        markdown = r"\*not emphasis\*"

        assert "data-escaped-char" not in comrak.render_markdown(
            markdown, render_options=opts
        )

        opts.escaped_char_spans = True
        assert "data-escaped-char" in comrak.render_markdown(
            markdown, render_options=opts
        )

    def test_tasklist_classes(self):
        e_opts = comrak.ExtensionOptions()
        e_opts.tasklist = True
        r_opts = comrak.RenderOptions()
        markdown = "- [x] Done"

        before = comrak.render_markdown(
            markdown, extension_options=e_opts, render_options=r_opts
        )
        assert "task-list-item" not in before

        r_opts.tasklist_classes = True
        after = comrak.render_markdown(
            markdown, extension_options=e_opts, render_options=r_opts
        )
        assert "task-list-item" in after

    def test_full_info_string(self):
        opts = comrak.RenderOptions()
        markdown = "```python extra info\nx\n```"

        assert "extra info" not in comrak.render_markdown(markdown, render_options=opts)

        opts.full_info_string = True
        result = comrak.render_markdown(
            "``` rust extra info\nfn hello();\n```\n", render_options=opts
        )
        assert 'data-meta="extra info"' in result

    def test_gfm_quirks(self):
        opts = comrak.RenderOptions()
        markdown = "****abcd**** *_foo_*"

        assert comrak.render_markdown(markdown, render_options=opts) == (
            "<p><strong><strong>abcd</strong></strong> <em><em>foo</em></em></p>\n"
        )

        opts.gfm_quirks = True
        assert comrak.render_markdown(markdown, render_options=opts) == (
            "<p><strong>abcd</strong> <em><em>foo</em></em></p>\n"
        )

    def test_compact_html(self):
        opts = comrak.RenderOptions()
        markdown = "# Hello\n\nWorld.\n"

        assert comrak.render_markdown(markdown, render_options=opts) == (
            "<h1>Hello</h1>\n<p>World.</p>\n"
        )

        opts.compact_html = True
        assert comrak.render_markdown(markdown, render_options=opts) == (
            "<h1>Hello</h1><p>World.</p>"
        )


# --------------------------------------------------------------------------
# CommonMark output
# --------------------------------------------------------------------------


class TestCommonmarkOutput:
    """``render_commonmark`` renders Markdown back to normalized CommonMark."""

    def test_basic(self):
        assert comrak.render_commonmark("hello world") == "hello world\n"

    def test_width(self):
        opts = comrak.RenderOptions()
        markdown = "hello hello hello hello hello hello"

        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "hello hello hello hello hello hello\n"
        )

        opts.width = 20
        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "hello hello hello\nhello hello hello\n"
        )

    def test_list_style(self):
        opts = comrak.RenderOptions()
        markdown = "- one\n- two\n- three"

        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "- one\n- two\n- three\n"
        )

        opts.list_style = comrak.ListStyle.Plus
        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "+ one\n+ two\n+ three\n"
        )

        opts.list_style = comrak.ListStyle.Star
        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "* one\n* two\n* three\n"
        )

    def test_ol_width(self):
        opts = comrak.RenderOptions()
        markdown = "1. Something"

        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "1. Something\n"
        )

        opts.ol_width = 5
        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "1.   Something\n"
        )

    def test_prefer_fenced(self):
        opts = comrak.RenderOptions()
        markdown = "```\nhello\n```\n"

        assert comrak.render_commonmark(markdown, render_options=opts) == "    hello\n"

        opts.prefer_fenced = True
        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "```\nhello\n```\n"
        )

    def test_experimental_minimize_commonmark(self):
        opts = comrak.RenderOptions()
        markdown = "__hi"

        assert comrak.render_commonmark(markdown, render_options=opts) == "\\_\\_hi\n"

        opts.experimental_minimize_commonmark = True
        assert comrak.render_commonmark(markdown, render_options=opts) == "__hi\n"

    def test_options_are_independent_of_render_markdown(self):
        """The same ``RenderOptions`` object drives both formatters independently."""
        opts = comrak.RenderOptions()
        opts.list_style = comrak.ListStyle.Plus
        markdown = "- one\n- two"

        assert "<li>one</li>" in comrak.render_markdown(markdown, render_options=opts)
        assert comrak.render_commonmark(markdown, render_options=opts) == (
            "+ one\n+ two\n"
        )


class TestAlertStyle:
    """The ``AlertStyle`` enum and the render option that consumes it."""

    @pytest.mark.parametrize(
        ("style", "expected"),
        [
            pytest.param(
                comrak.AlertStyle.Specific,
                '<div class="markdown-alert markdown-alert-note">\n'
                '<p class="markdown-alert-title">Note</p>\n'
                "<p>Note this!</p>\n"
                "</div>",
                id="specific",
            ),
            pytest.param(
                comrak.AlertStyle.Semantic,
                '<aside class="admonition note">\n'
                '<p class="admonition-title">Note</p>\n'
                "<p>Note this!</p>\n"
                "</aside>",
                id="semantic",
            ),
        ],
    )
    def test_alert_style(self, style, expected):
        e_opts = comrak.ExtensionOptions()
        e_opts.alerts = True
        r_opts = comrak.RenderOptions()
        r_opts.alert_style = style
        result = comrak.render_markdown(
            "> [!note]\n> Note this!",
            extension_options=e_opts,
            render_options=r_opts,
        )
        assert expected in result

    def test_value_equality(self):
        assert comrak.AlertStyle.Specific == comrak.AlertStyle.Specific
        assert comrak.AlertStyle.Specific != comrak.AlertStyle.Semantic

    @pytest.mark.parametrize(
        ("style", "discriminant"),
        [
            pytest.param(comrak.AlertStyle.Specific, 0, id="specific"),
            pytest.param(comrak.AlertStyle.Semantic, 1, id="semantic"),
        ],
    )
    def test_int_conversion(self, style, discriminant):
        assert int(style) == discriminant
        assert style == discriminant

    def test_hashable(self):
        mapping = {
            comrak.AlertStyle.Specific: "specific",
            comrak.AlertStyle.Semantic: "semantic",
        }
        assert mapping[comrak.AlertStyle.Specific] == "specific"
        assert len({comrak.AlertStyle.Specific, comrak.AlertStyle.Specific}) == 1

    def test_module(self):
        """``module="comrak"`` fixes repr and qualified name for pickling."""
        assert comrak.AlertStyle.__module__ == "comrak"


class TestListStyle:
    """The ``ListStyle`` enum. Discriminants are the ASCII bullet codepoints."""

    @pytest.mark.parametrize(
        ("style", "codepoint"),
        [
            pytest.param(comrak.ListStyle.Dash, 45, id="dash"),
            pytest.param(comrak.ListStyle.Plus, 43, id="plus"),
            pytest.param(comrak.ListStyle.Star, 42, id="star"),
        ],
    )
    def test_discriminant_is_the_bullet_character(self, style, codepoint):
        assert int(style) == codepoint
        assert style == codepoint
        assert chr(codepoint) in "-+*"

    def test_default_is_dash(self):
        assert comrak.RenderOptions().list_style == comrak.ListStyle.Dash

    def test_rejects_raw_int(self):
        opts = comrak.RenderOptions()
        with pytest.raises(TypeError):
            opts.list_style = 42

    def test_module(self):
        assert comrak.ListStyle.__module__ == "comrak"


# --------------------------------------------------------------------------
# Cross-cutting
# --------------------------------------------------------------------------


class TestCombinedOptions:
    def test_options_compose(self):
        e_opts = comrak.ExtensionOptions()
        e_opts.shortcodes = True
        p_opts = comrak.ParseOptions()
        p_opts.smart = True
        r_opts = comrak.RenderOptions()
        r_opts.hardbreaks = True

        result = comrak.render_markdown(
            ':smile: "quoted"\nline2',
            extension_options=e_opts,
            parse_options=p_opts,
            render_options=r_opts,
        )
        assert "😄" in result
        assert "“quoted”" in result
        assert "<br" in result

    def test_options_are_independent_between_calls(self):
        opts = comrak.ExtensionOptions()
        opts.strikethrough = True
        assert "<del>" in comrak.render_markdown("~~x~~", extension_options=opts)
        assert "<del>" not in comrak.render_markdown("~~x~~")


class TestDeprecations:
    """Aliases retained for compatibility with earlier releases."""

    def test_header_ids_warns_on_set(self):
        opts = comrak.ExtensionOptions()
        with pytest.warns(FutureWarning, match="header_id_prefix"):
            opts.header_ids = "user-content-"
        assert opts.header_id_prefix == "user-content-"

    def test_header_ids_warns_on_get(self):
        opts = comrak.ExtensionOptions()
        opts.header_id_prefix = "user-content-"
        with pytest.warns(FutureWarning, match="header_id_prefix"):
            assert opts.header_ids == "user-content-"

    def test_header_ids_still_functions(self):
        opts = comrak.ExtensionOptions()
        with pytest.warns(FutureWarning):
            opts.header_ids = "user-content-"
        result = comrak.render_markdown("# README", extension_options=opts)
        assert 'id="user-content-readme"' in result


class TestOptionCoverage:
    """Every public option must be exercised by a test in this module.

    The Rust-side exhaustiveness guard catches options appearing upstream.
    This catches options exposed to Python that nothing exercises, which is
    how an option ends up settable but inert.

    When this fails, either add a test and list the option here, or add it to
    the relevant table above.
    """

    #: Options covered by a dedicated test rather than a parametrised table.
    COVERED_INDIVIDUALLY = {
        "ExtensionOptions": {
            "tagfilter",
            "tasklist",
            "multiline_block_quotes",
            "front_matter_delimiter",
            "math_latex",
            "footnotes",
            "inline_footnotes",
            "header_id_prefix",
            "header_id_prefix_in_href",
            "header_ids",
            "link_url_rewriter",
            "image_url_rewriter",
        },
        "ParseOptions": {
            "smart",
            "default_info_string",
            "ignore_setext",
            "relaxed_autolinks",
            "relaxed_tasklist_matching",
            "tasklist_in_table",
            "escaped_char_spans",
            "sourcepos_chars",
            "leave_footnote_definitions",
        },
        "RenderOptions": {
            "unsafe_",
            "escape",
            "escaped_char_spans",
            "tasklist_classes",
            "full_info_string",
            "gfm_quirks",
            "compact_html",
            "alert_style",
            *COMMONMARK_ONLY_RENDER_OPTIONS,
        },
    }

    TABLE_DRIVEN = {
        "ExtensionOptions": {param.values[0] for param in EXTENSION_TOGGLES},
        "ParseOptions": set(),
        "RenderOptions": {param.values[0] for param in RENDER_TOGGLES},
    }

    @pytest.mark.parametrize(
        "class_name", ["ExtensionOptions", "ParseOptions", "RenderOptions"]
    )
    def test_every_option_is_covered(self, class_name):
        cls = getattr(comrak, class_name)
        public = {name for name in dir(cls) if not name.startswith("_")}
        covered = self.TABLE_DRIVEN[class_name] | self.COVERED_INDIVIDUALLY[class_name]

        assert public - covered == set(), (
            f"{class_name} options with no test: {sorted(public - covered)}"
        )
        assert covered - public == set(), (
            f"{class_name} tests reference options that no longer exist: "
            f"{sorted(covered - public)}"
        )
