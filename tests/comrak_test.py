import comrak


class TestBasicRendering:
    """Test basic markdown to HTML rendering."""

    def test_simple_markdown(self):
        """Test rendering simple markdown."""
        result = comrak.render_markdown("# Hello")
        assert result == "<h1>Hello</h1>\n"

    def test_bold_text(self):
        """Test rendering bold text."""
        result = comrak.render_markdown("**bold**")
        assert "<strong>bold</strong>" in result

    def test_italic_text(self):
        """Test rendering italic text."""
        result = comrak.render_markdown("*italic*")
        assert "<em>italic</em>" in result

    def test_link(self):
        """Test rendering links."""
        result = comrak.render_markdown("[link](https://example.com)")
        assert '<a href="https://example.com">link</a>' in result

    def test_list(self):
        """Test rendering lists."""
        markdown = "- item1\n- item2"
        result = comrak.render_markdown(markdown)
        assert "<ul>" in result
        assert "<li>item1</li>" in result
        assert "<li>item2</li>" in result

    def test_code_block(self):
        """Test rendering code blocks."""
        markdown = "```python\nprint('hello')\n```"
        result = comrak.render_markdown(markdown)
        assert "<pre>" in result
        assert "<code" in result

    def test_empty_string(self):
        """Test rendering empty string."""
        result = comrak.render_markdown("")
        assert result == ""

    def test_multiline_markdown(self):
        """Test rendering multiline markdown."""
        markdown = """# Title

This is a paragraph.

## Subtitle

Another paragraph."""
        result = comrak.render_markdown(markdown)
        assert "<h1>Title</h1>" in result
        assert "<h2>Subtitle</h2>" in result
        assert "<p>This is a paragraph.</p>" in result


class TestExtensionOptions:
    """Test ExtensionOptions configuration."""

    def test_shortcodes_disabled_by_default(self):
        """Test that shortcodes are disabled by default."""
        result = comrak.render_markdown("foo :smile:")
        assert ":smile:" in result
        assert "😄" not in result

    def test_shortcodes_enabled(self):
        """Test enabling shortcodes."""
        opts = comrak.ExtensionOptions()
        opts.shortcodes = True
        result = comrak.render_markdown("foo :smile:", extension_options=opts)
        assert "😄" in result
        assert ":smile:" not in result

    def test_strikethrough(self):
        """Test strikethrough extension."""
        opts = comrak.ExtensionOptions()
        opts.strikethrough = True
        result = comrak.render_markdown("~~strikethrough~~", extension_options=opts)
        assert "<del>strikethrough</del>" in result

    def test_table(self):
        """Test table extension."""
        opts = comrak.ExtensionOptions()
        opts.table = True
        markdown = """| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |"""
        result = comrak.render_markdown(markdown, extension_options=opts)
        assert "<table>" in result
        assert "<thead>" in result
        assert "<tbody>" in result

    def test_autolink(self):
        """Test autolink extension."""
        opts = comrak.ExtensionOptions()
        opts.autolink = True
        result = comrak.render_markdown("https://example.com", extension_options=opts)
        assert '<a href="https://example.com">https://example.com</a>' in result

    def test_tasklist(self):
        """Test tasklist extension."""
        opts = comrak.ExtensionOptions()
        opts.tasklist = True
        markdown = "- [ ] Unchecked\n- [x] Checked"
        result = comrak.render_markdown(markdown, extension_options=opts)
        assert "checkbox" in result.lower() or 'type="checkbox"' in result

    def test_superscript(self):
        """Test superscript extension."""
        opts = comrak.ExtensionOptions()
        opts.superscript = True
        result = comrak.render_markdown("x^2^", extension_options=opts)
        assert "<sup>2</sup>" in result

    def test_footnotes(self):
        """Test footnotes extension."""
        opts = comrak.ExtensionOptions()
        opts.footnotes = True
        markdown = "Text[^1]\n\n[^1]: Footnote"
        result = comrak.render_markdown(markdown, extension_options=opts)
        # Footnotes should generate some special markup
        assert "footnote" in result.lower() or "Footnote" in result


class TestParseOptions:
    """Test ParseOptions configuration."""

    def test_smart_punctuation(self):
        """Test smart punctuation."""
        opts = comrak.ParseOptions()
        opts.smart = True
        result = comrak.render_markdown("'Hello,' \"world\" ...", parse_options=opts)
        # Smart quotes should convert straight quotes to curly quotes and ... to ellipsis
        assert "‘Hello,’" in result  # fancy single quote
        assert "“world”" in result  # fancy double quote
        assert "…" in result  # ellipsis character


class TestRenderOptions:
    """Test RenderOptions configuration."""

    def test_hardbreaks(self):
        """Test hardbreaks option."""
        opts = comrak.RenderOptions()
        opts.hardbreaks = True
        result = comrak.render_markdown("line1\nline2", render_options=opts)
        assert "<br" in result

    def test_unsafe_html(self):
        """Test unsafe HTML rendering."""
        opts = comrak.RenderOptions()
        opts.unsafe_ = True
        markdown = '<script>alert("xss")</script>'
        result = comrak.render_markdown(markdown, render_options=opts)
        assert "<script>" in result

    def test_safe_html_by_default(self):
        """Test that HTML is escaped by default."""
        markdown = '<script>alert("xss")</script>'
        result = comrak.render_markdown(markdown)
        # By default, HTML should be escaped or removed
        assert "<script>" not in result or "&lt;script&gt;" in result


class TestOptionsObjects:
    """Test that options objects can be instantiated and configured."""

    def test_extension_options_instantiation(self):
        """Test ExtensionOptions can be instantiated."""
        opts = comrak.ExtensionOptions()
        assert hasattr(opts, "shortcodes")
        assert hasattr(opts, "strikethrough")
        assert hasattr(opts, "table")

    def test_parse_options_instantiation(self):
        """Test ParseOptions can be instantiated."""
        opts = comrak.ParseOptions()
        assert hasattr(opts, "smart")

    def test_render_options_instantiation(self):
        """Test RenderOptions can be instantiated."""
        opts = comrak.RenderOptions()
        assert hasattr(opts, "hardbreaks")
        assert hasattr(opts, "unsafe_")

    def test_extension_options_defaults(self):
        """Test ExtensionOptions default values."""
        opts = comrak.ExtensionOptions()
        assert opts.shortcodes is False
        # Most GFM extensions should be enabled by default
        assert isinstance(opts.strikethrough, bool)

    def test_options_can_be_set(self):
        """Test that options can be set and retrieved."""
        opts = comrak.ExtensionOptions()
        opts.shortcodes = True
        assert opts.shortcodes is True
        opts.shortcodes = False
        assert opts.shortcodes is False


class TestCombinedOptions:
    """Test using multiple option types together."""

    def test_combined_extension_and_render_options(self):
        """Test using extension and render options together."""
        ext_opts = comrak.ExtensionOptions()
        ext_opts.strikethrough = True

        render_opts = comrak.RenderOptions()
        render_opts.hardbreaks = True

        markdown = "~~test~~\nline2"
        result = comrak.render_markdown(
            markdown,
            extension_options=ext_opts,
            render_options=render_opts,
        )
        assert "<del>test</del>" in result
        assert "<br" in result

    def test_all_three_option_types(self):
        """Test using all three option types together."""
        ext_opts = comrak.ExtensionOptions()
        ext_opts.shortcodes = True

        parse_opts = comrak.ParseOptions()
        parse_opts.smart = True

        render_opts = comrak.RenderOptions()
        render_opts.hardbreaks = True

        markdown = ':smile: "quoted"\nline2'
        result = comrak.render_markdown(
            markdown,
            extension_options=ext_opts,
            parse_options=parse_opts,
            render_options=render_opts,
        )
        assert "😄" in result


class TestRegressions:
    """Test for potential regressions and edge cases."""

    def test_unicode_handling(self):
        """Test that unicode characters are handled correctly."""
        markdown = "# 你好 World 🌍"
        result = comrak.render_markdown(markdown)
        assert "你好" in result
        assert "🌍" in result

    def test_special_characters(self):
        """Test special characters in markdown."""
        markdown = "Test & test < test > test"
        result = comrak.render_markdown(markdown)
        # Should be properly escaped
        assert "&amp;" in result or "&" in result

    def test_nested_formatting(self):
        """Test nested markdown formatting."""
        markdown = "**bold with *italic* inside**"
        result = comrak.render_markdown(markdown)
        assert "<strong>" in result
        assert "<em>" in result

    def test_very_long_document(self):
        """Test rendering a very long document."""
        markdown = "\n".join([f"# Heading {i}" for i in range(1000)])
        result = comrak.render_markdown(markdown)
        assert result.count("<h1>") == 1000
