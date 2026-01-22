from textwrap import dedent

import comrak


class TestLinkUrlRewriter:
    """Test link_url_rewriter extension option."""

    def test__basic(self):
        """Test basic link URL rewriting."""
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: f"https://proxy.example.com?url={url}"

        result = comrak.render_markdown(
            "[my link](http://example.com)", extension_options=opts
        )
        assert "https://proxy.example.com?url=http://example.com" in result
        assert "<a href=" in result

    def test_none_by_default(self):
        """Test that link_url_rewriter is None by default."""
        opts = comrak.ExtensionOptions()
        assert opts.link_url_rewriter is None

    def test_can_be_set_to_none(self):
        """Test that link_url_rewriter can be set back to None."""
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: url
        assert opts.link_url_rewriter is not None
        opts.link_url_rewriter = None
        assert opts.link_url_rewriter is None

    def test_multiple_links(self):
        """Test rewriting multiple links in a document."""
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: url.replace("http://", "https://")

        markdown = dedent("""\
            [Link 1](http://example.com)
            [Link 2](http://another.com)
            [Link 3](https://already-secure.com)
            """)
        result = comrak.render_markdown(markdown, extension_options=opts)
        assert "https://example.com" in result
        assert "https://another.com" in result
        assert "https://already-secure.com" in result
        assert "http://" not in result

    def test_with_complex_urls(self):
        """Test rewriting URLs with query parameters and fragments."""
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = (
            lambda url: f"https://safe.example.com/redirect?to={url}"
        )

        markdown = "[link](http://example.com/path?query=value#fragment)"
        result = comrak.render_markdown(markdown, extension_options=opts)
        assert (
            "https://safe.example.com/redirect?to=http://example.com/path?query=value#fragment"
            in result
        )

    def test_does_not_affect_images(self):
        """Test that link_url_rewriter doesn't affect image URLs."""
        opts = comrak.ExtensionOptions()
        opts.link_url_rewriter = lambda url: "REWRITTEN"

        markdown = "![alt](http://example.com/image.png)"
        result = comrak.render_markdown(markdown, extension_options=opts)
        # Image URL should NOT be rewritten
        assert "http://example.com/image.png" in result

    def test_getter_returns_callable(self):
        """Test that the getter returns a callable that can be invoked."""
        opts = comrak.ExtensionOptions()

        def my_rewriter(url):
            return f"modified:{url}"

        opts.link_url_rewriter = my_rewriter
        retrieved = opts.link_url_rewriter
        # The retrieved function should behave the same
        assert callable(retrieved)

    def test_with_header_ids_prefix(self):
        """Test rewriting anchor links to match header_ids prefix.

        When using header_ids with a prefix like "user-content-", the generated
        header anchors will have that prefix. This example shows how to use
        link_url_rewriter to update anchor links written in markdown to match.

        Note: link_url_rewriter only affects links from markdown syntax [text](url),
        not the auto-generated anchor links inside headers from header_ids.
        """
        opts = comrak.ExtensionOptions()
        prefix = "user-content-"
        opts.header_ids = prefix
        opts.link_url_rewriter = (
            lambda url: f"#{prefix}{url[1:]}" if url.startswith("#") else url
        )

        markdown = dedent("""\
            # Introduction

            See the [summary](#summary) below.

            ## Summary

            Back to [introduction](#introduction).
            """)
        result = comrak.render_markdown(markdown, extension_options=opts)

        # Header IDs should have the prefix
        assert 'id="user-content-introduction"' in result
        assert 'id="user-content-summary"' in result

        # User-written markdown links should be rewritten with the prefix
        assert 'href="#user-content-summary"' in result
        assert 'href="#user-content-introduction"' in result
