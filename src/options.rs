use pyo3::exceptions::PyFutureWarning;
use pyo3::prelude::*;
use std::panic::RefUnwindSafe;
use std::sync::Arc;

// Import the Comrak (Rust) types under `comrak_lib::`
use comrak_lib::options::{
    AlertStyleType, Extension as ComrakExtensionOptions, ListStyleType,
    Parse as ComrakParseOptions, Render as ComrakRenderOptions, URLRewriter,
};

/// A wrapper around a Python callable that implements URLRewriter.
/// This allows Python functions to be used as URL rewriters in Comrak.
pub struct PyURLRewriter {
    callback: Arc<Py<PyAny>>,
}

// Py<PyAny> is Send + Sync; we handle Python exceptions by returning the original URL
impl RefUnwindSafe for PyURLRewriter {}

impl PyURLRewriter {
    pub fn new(callback: Arc<Py<PyAny>>) -> Self {
        Self { callback }
    }
}

impl URLRewriter for PyURLRewriter {
    fn to_html(&self, url: &str) -> String {
        Python::attach(|py| {
            self.callback
                .call1(py, (url,))
                .and_then(|result| result.extract::<String>(py))
                .unwrap_or_else(|_| url.to_string())
        })
    }
}

/// Python class that mirrors Comrak's `ExtensionOptions`
#[pyclass(name = "ExtensionOptions", module = "comrak", from_py_object)]
#[derive(Clone)]
pub struct PyExtensionOptions {
    #[pyo3(get, set)]
    pub strikethrough: bool,
    #[pyo3(get, set)]
    pub tagfilter: bool,
    #[pyo3(get, set)]
    pub table: bool,
    #[pyo3(get, set)]
    pub autolink: bool,
    #[pyo3(get, set)]
    pub tasklist: bool,
    #[pyo3(get, set)]
    pub superscript: bool,
    #[pyo3(get, set)]
    pub header_id_prefix: Option<String>,
    #[pyo3(get, set)]
    pub header_id_prefix_in_href: bool,
    #[pyo3(get, set)]
    pub footnotes: bool,
    #[pyo3(get, set)]
    pub inline_footnotes: bool,
    #[pyo3(get, set)]
    pub cjk_friendly_emphasis: bool,
    #[pyo3(get, set)]
    pub subtext: bool,
    #[pyo3(get, set)]
    pub highlight: bool,
    #[pyo3(get, set)]
    pub math_latex: bool,
    #[pyo3(get, set)]
    pub insert: bool,
    #[pyo3(get, set)]
    pub block_directive: bool,
    #[pyo3(get, set)]
    pub description_lists: bool,
    #[pyo3(get, set)]
    pub front_matter_delimiter: Option<String>,
    #[pyo3(get, set)]
    pub multiline_block_quotes: bool,
    #[pyo3(get, set)]
    pub alerts: bool,
    #[pyo3(get, set)]
    pub math_dollars: bool,
    #[pyo3(get, set)]
    pub math_code: bool,
    #[pyo3(get, set)]
    pub shortcodes: bool,
    #[pyo3(get, set)]
    pub wikilinks_title_after_pipe: bool,
    #[pyo3(get, set)]
    pub wikilinks_title_before_pipe: bool,
    #[pyo3(get, set)]
    pub underline: bool,
    #[pyo3(get, set)]
    pub subscript: bool,
    #[pyo3(get, set)]
    pub spoiler: bool,
    #[pyo3(get, set)]
    pub greentext: bool,
    pub link_url_rewriter: Option<Arc<Py<PyAny>>>,
    pub image_url_rewriter: Option<Arc<Py<PyAny>>>,
}

impl PyExtensionOptions {
    /// **Rust-only** helper to copy from `PyExtensionOptions` into a real `ComrakExtensionOptions`.
    pub fn update_extension_options(&self, opts: &mut ComrakExtensionOptions<'_>) {
        opts.strikethrough = self.strikethrough;
        opts.tagfilter = self.tagfilter;
        opts.table = self.table;
        opts.autolink = self.autolink;
        opts.tasklist = self.tasklist;
        opts.superscript = self.superscript;
        opts.header_id_prefix = self.header_id_prefix.clone();
        opts.header_id_prefix_in_href = self.header_id_prefix_in_href;
        opts.inline_footnotes = self.inline_footnotes;
        opts.cjk_friendly_emphasis = self.cjk_friendly_emphasis;
        opts.subtext = self.subtext;
        opts.highlight = self.highlight;
        opts.math_latex = self.math_latex;
        opts.insert = self.insert;
        opts.block_directive = self.block_directive;
        opts.footnotes = self.footnotes;
        opts.description_lists = self.description_lists;
        opts.front_matter_delimiter = self.front_matter_delimiter.clone();
        opts.multiline_block_quotes = self.multiline_block_quotes;
        opts.alerts = self.alerts;
        opts.math_dollars = self.math_dollars;
        opts.math_code = self.math_code;
        opts.shortcodes = self.shortcodes;
        opts.wikilinks_title_after_pipe = self.wikilinks_title_after_pipe;
        opts.wikilinks_title_before_pipe = self.wikilinks_title_before_pipe;
        opts.underline = self.underline;
        opts.subscript = self.subscript;
        opts.spoiler = self.spoiler;
        opts.greentext = self.greentext;
        opts.image_url_rewriter = self
            .image_url_rewriter
            .clone()
            .map(|cb| Arc::new(PyURLRewriter::new(cb)) as Arc<dyn URLRewriter>);
        opts.link_url_rewriter = self
            .link_url_rewriter
            .clone()
            .map(|cb| Arc::new(PyURLRewriter::new(cb)) as Arc<dyn URLRewriter>);
    }
}

#[pymethods]
impl PyExtensionOptions {
    #[new]
    pub fn new() -> Self {
        let defaults = ComrakExtensionOptions::default();
        Self {
            strikethrough: defaults.strikethrough,
            tagfilter: defaults.tagfilter,
            table: defaults.table,
            autolink: defaults.autolink,
            tasklist: defaults.tasklist,
            superscript: defaults.superscript,
            header_id_prefix: defaults.header_id_prefix.clone(),
            block_directive: defaults.block_directive,
            cjk_friendly_emphasis: defaults.cjk_friendly_emphasis,
            header_id_prefix_in_href: defaults.header_id_prefix_in_href,
            highlight: defaults.highlight,
            math_latex: defaults.math_latex,
            inline_footnotes: defaults.inline_footnotes,
            insert: defaults.insert,
            subtext: defaults.subtext,
            footnotes: defaults.footnotes,
            description_lists: defaults.description_lists,
            front_matter_delimiter: defaults.front_matter_delimiter.clone(),
            multiline_block_quotes: defaults.multiline_block_quotes,
            alerts: defaults.alerts,
            math_dollars: defaults.math_dollars,
            math_code: defaults.math_code,
            shortcodes: defaults.shortcodes,
            wikilinks_title_after_pipe: defaults.wikilinks_title_after_pipe,
            wikilinks_title_before_pipe: defaults.wikilinks_title_before_pipe,
            underline: defaults.underline,
            subscript: defaults.subscript,
            spoiler: defaults.spoiler,
            greentext: defaults.greentext,
            link_url_rewriter: None,
            image_url_rewriter: None,
        }
    }

    /// Optional callable that rewrites link URLs.
    /// The callable should accept a URL string and return a modified URL string.
    #[getter]
    pub fn link_url_rewriter(&self, py: Python<'_>) -> Option<Py<PyAny>> {
        self.link_url_rewriter.as_ref().map(|cb| cb.clone_ref(py))
    }

    #[setter]
    pub fn set_link_url_rewriter(&mut self, callback: Option<Py<PyAny>>) {
        self.link_url_rewriter = callback.map(Arc::new);
    }

    /// Optional callable that rewrites image URLs.
    /// the callable should accept a URL string and return a modified URL string.
    #[getter]
    pub fn image_url_rewriter(&self, py: Python<'_>) -> Option<Py<PyAny>> {
        self.image_url_rewriter.as_ref().map(|cb| cb.clone_ref(py))
    }

    #[setter]
    pub fn set_image_url_rewriter(&mut self, callback: Option<Py<PyAny>>) {
        self.image_url_rewriter = callback.map(Arc::new);
    }

    #[getter]
    #[pyo3(warn(message = "Use `header_id_prefix` instead", category = PyFutureWarning))]
    pub fn header_ids(&self) -> Option<String> {
        self.header_id_prefix.clone()
    }

    #[setter]
    #[pyo3(warn(message = "Use `header_id_prefix` instead", category = PyFutureWarning))]
    pub fn set_header_ids(&mut self, prefix: Option<String>) {
        self.header_id_prefix = prefix;
    }
}

/// Python class that mirrors Comrak’s `ParseOptions`
#[pyclass(name = "ParseOptions", module = "comrak", from_py_object)]
#[derive(Clone)]
pub struct PyParseOptions {
    #[pyo3(get, set)]
    pub smart: bool,
    #[pyo3(get, set)]
    pub default_info_string: Option<String>,
    #[pyo3(get, set)]
    pub relaxed_tasklist_matching: bool,
    #[pyo3(get, set)]
    pub relaxed_autolinks: bool,
    #[pyo3(get, set)]
    pub ignore_setext: bool,
    #[pyo3(get, set)]
    pub tasklist_in_table: bool,
    #[pyo3(get, set)]
    pub leave_footnote_definitions: bool,
    #[pyo3(get, set)]
    pub escaped_char_spans: bool,
    #[pyo3(get, set)]
    pub sourcepos_chars: bool,
}

impl PyParseOptions {
    /// Rust-only helper
    pub fn update_parse_options(&self, opts: &mut ComrakParseOptions<'_>) {
        opts.smart = self.smart;
        opts.default_info_string = self.default_info_string.clone();
        opts.relaxed_tasklist_matching = self.relaxed_tasklist_matching;
        opts.relaxed_autolinks = self.relaxed_autolinks;
        opts.ignore_setext = self.ignore_setext;
        opts.tasklist_in_table = self.tasklist_in_table;
        opts.leave_footnote_definitions = self.leave_footnote_definitions;
        opts.escaped_char_spans = self.escaped_char_spans;
        opts.sourcepos_chars = self.sourcepos_chars;
    }
}

#[pymethods]
impl PyParseOptions {
    #[new]
    pub fn new() -> Self {
        let defaults = ComrakParseOptions::default();
        Self {
            smart: defaults.smart,
            default_info_string: defaults.default_info_string.clone(),
            relaxed_tasklist_matching: defaults.relaxed_tasklist_matching,
            relaxed_autolinks: defaults.relaxed_autolinks,
            ignore_setext: defaults.ignore_setext,
            leave_footnote_definitions: defaults.leave_footnote_definitions,
            escaped_char_spans: defaults.escaped_char_spans,
            sourcepos_chars: defaults.sourcepos_chars,
            tasklist_in_table: defaults.tasklist_in_table,
        }
    }
}

/// Python class that mirrors Comrak’s `RenderOptions`
#[pyclass(name = "RenderOptions", module = "comrak", from_py_object)]
#[derive(Clone)]
pub struct PyRenderOptions {
    #[pyo3(get, set)]
    pub hardbreaks: bool,
    #[pyo3(get, set)]
    pub github_pre_lang: bool,
    #[pyo3(get, set)]
    pub full_info_string: bool,
    #[pyo3(get, set)]
    pub width: usize,
    #[pyo3(get, set)]
    pub unsafe_: bool, // named 'unsafe_' because 'unsafe' is reserved
    #[pyo3(get, set)]
    pub escape: bool,
    #[pyo3(get, set)]
    pub list_style: PyListStyle,
    #[pyo3(get, set)]
    pub alert_style: PyAlertStyle,
    #[pyo3(get, set)]
    pub sourcepos: bool,
    #[pyo3(get, set)]
    pub escaped_char_spans: bool,
    #[pyo3(get, set)]
    pub ignore_empty_links: bool,
    #[pyo3(get, set)]
    pub gfm_quirks: bool,
    #[pyo3(get, set)]
    pub prefer_fenced: bool,
    #[pyo3(get, set)]
    pub figure_with_caption: bool,
    #[pyo3(get, set)]
    pub tasklist_classes: bool,
    #[pyo3(get, set)]
    pub ol_width: usize,
    #[pyo3(get, set)]
    pub experimental_minimize_commonmark: bool,
    #[pyo3(get, set)]
    pub compact_html: bool,
}

#[derive(Clone, Copy, Debug, Hash, PartialEq)]
#[pyclass(
    name = "AlertStyle",
    module = "comrak",
    from_py_object,
    eq,
    eq_int,
    frozen,
    hash
)]
pub enum PyAlertStyle {
    Specific,
    Semantic,
}

impl From<PyAlertStyle> for AlertStyleType {
    fn from(val: PyAlertStyle) -> Self {
        match val {
            PyAlertStyle::Specific => AlertStyleType::Specific,
            PyAlertStyle::Semantic => AlertStyleType::Semantic,
        }
    }
}

impl From<AlertStyleType> for PyAlertStyle {
    fn from(val: AlertStyleType) -> Self {
        match val {
            AlertStyleType::Specific => PyAlertStyle::Specific,
            AlertStyleType::Semantic => PyAlertStyle::Semantic,
        }
    }
}

#[derive(Clone, Copy, Debug, Hash, PartialEq)]
#[pyclass(
    name = "ListStyle",
    module = "comrak",
    from_py_object,
    eq,
    eq_int,
    frozen,
    hash
)]
pub enum PyListStyle {
    Dash = 45,
    Plus = 43,
    Star = 42,
}

impl From<PyListStyle> for ListStyleType {
    fn from(val: PyListStyle) -> Self {
        match val {
            PyListStyle::Dash => ListStyleType::Dash,
            PyListStyle::Plus => ListStyleType::Plus,
            PyListStyle::Star => ListStyleType::Star,
        }
    }
}

impl From<ListStyleType> for PyListStyle {
    fn from(val: ListStyleType) -> Self {
        match val {
            ListStyleType::Dash => PyListStyle::Dash,
            ListStyleType::Plus => PyListStyle::Plus,
            ListStyleType::Star => PyListStyle::Star,
        }
    }
}

impl PyRenderOptions {
    /// Rust-only helper
    pub fn update_render_options(&self, opts: &mut ComrakRenderOptions) {
        opts.hardbreaks = self.hardbreaks;
        opts.github_pre_lang = self.github_pre_lang;
        opts.full_info_string = self.full_info_string;
        opts.width = self.width;
        opts.r#unsafe = self.unsafe_;
        opts.escape = self.escape;
        opts.list_style = self.list_style.into();
        opts.alert_style = self.alert_style.into();
        opts.sourcepos = self.sourcepos;
        opts.escaped_char_spans = self.escaped_char_spans;
        opts.ignore_empty_links = self.ignore_empty_links;
        opts.gfm_quirks = self.gfm_quirks;
        opts.prefer_fenced = self.prefer_fenced;
        opts.figure_with_caption = self.figure_with_caption;
        opts.tasklist_classes = self.tasklist_classes;
        opts.ol_width = self.ol_width;
        opts.experimental_minimize_commonmark = self.experimental_minimize_commonmark;
        opts.compact_html = self.compact_html;
    }
}

#[pymethods]
impl PyRenderOptions {
    #[new]
    pub fn new() -> Self {
        let defaults = ComrakRenderOptions::default();
        Self {
            hardbreaks: defaults.hardbreaks,
            github_pre_lang: defaults.github_pre_lang,
            full_info_string: defaults.full_info_string,
            width: defaults.width,
            unsafe_: defaults.r#unsafe,
            escape: defaults.escape,
            list_style: defaults.list_style.into(),
            alert_style: defaults.alert_style.into(),
            sourcepos: defaults.sourcepos,
            escaped_char_spans: defaults.escaped_char_spans,
            ignore_empty_links: defaults.ignore_empty_links,
            gfm_quirks: defaults.gfm_quirks,
            prefer_fenced: defaults.prefer_fenced,
            figure_with_caption: defaults.figure_with_caption,
            tasklist_classes: defaults.tasklist_classes,
            ol_width: defaults.ol_width,
            experimental_minimize_commonmark: defaults.experimental_minimize_commonmark,
            compact_html: defaults.compact_html,
        }
    }
}

/// Compile-time guards: these fail to build when comrak adds an option.
/// When one breaks, add the field to the pyclass above, then name it here.
#[allow(dead_code)]
fn _exhaustiveness(
    e: ComrakExtensionOptions<'_>,
    p: ComrakParseOptions<'_>,
    r: ComrakRenderOptions,
) {
    let ComrakExtensionOptions {
        strikethrough: _,
        tagfilter: _,
        table: _,
        autolink: _,
        tasklist: _,
        superscript: _,
        header_id_prefix: _,
        header_id_prefix_in_href: _,
        footnotes: _,
        inline_footnotes: _,
        description_lists: _,
        front_matter_delimiter: _,
        multiline_block_quotes: _,
        alerts: _,
        math_dollars: _,
        math_code: _,
        shortcodes: _,
        wikilinks_title_after_pipe: _,
        wikilinks_title_before_pipe: _,
        underline: _,
        subscript: _,
        spoiler: _,
        greentext: _,
        image_url_rewriter: _,
        link_url_rewriter: _,
        cjk_friendly_emphasis: _,
        subtext: _,
        highlight: _,
        insert: _,
        block_directive: _,
        math_latex: _,
    } = e;
    let ComrakParseOptions {
        smart: _,
        default_info_string: _,
        relaxed_tasklist_matching: _,
        tasklist_in_table: _,
        relaxed_autolinks: _,
        ignore_setext: _,
        broken_link_callback: _,
        leave_footnote_definitions: _,
        escaped_char_spans: _,
        sourcepos_chars: _,
    } = p;
    let ComrakRenderOptions {
        hardbreaks: _,
        github_pre_lang: _,
        full_info_string: _,
        width: _,
        r#unsafe: _,
        escape: _,
        list_style: _,
        sourcepos: _,
        escaped_char_spans: _,
        ignore_empty_links: _,
        gfm_quirks: _,
        prefer_fenced: _,
        figure_with_caption: _,
        tasklist_classes: _,
        alert_style: _,
        ol_width: _,
        experimental_minimize_commonmark: _,
        compact_html: _,
    } = r;
}
