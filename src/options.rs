use pyo3::prelude::*;

// Import the Comrak (Rust) types under `comrak_lib::`
use comrak_lib::options::{
    Extension as ComrakExtensionOptions, ListStyleType, Parse as ComrakParseOptions,
    Render as ComrakRenderOptions,
};

/// Python class that mirrors Comrak’s `ExtensionOptions`
#[pyclass(name = "ExtensionOptions")]
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
    pub header_ids: Option<String>,
    #[pyo3(get, set)]
    pub footnotes: bool,
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
    pub shortcodes: bool, // if your comrak_lib has the "shortcodes" feature
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
        opts.header_ids = self.header_ids.clone();
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
            header_ids: defaults.header_ids.clone(),
            footnotes: defaults.footnotes,
            description_lists: defaults.description_lists,
            front_matter_delimiter: defaults.front_matter_delimiter.clone(),
            multiline_block_quotes: defaults.multiline_block_quotes,
            alerts: defaults.alerts,
            math_dollars: defaults.math_dollars,
            math_code: defaults.math_code,
            shortcodes: false, // or `defaults.shortcodes` if your version has that
            wikilinks_title_after_pipe: defaults.wikilinks_title_after_pipe,
            wikilinks_title_before_pipe: defaults.wikilinks_title_before_pipe,
            underline: defaults.underline,
            subscript: defaults.subscript,
            spoiler: defaults.spoiler,
            greentext: defaults.greentext,
        }
    }
}

/// Python class that mirrors Comrak’s `ParseOptions`
#[pyclass(name = "ParseOptions")]
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
}

impl PyParseOptions {
    /// Rust-only helper
    pub fn update_parse_options(&self, opts: &mut ComrakParseOptions<'_>) {
        opts.smart = self.smart;
        opts.default_info_string = self.default_info_string.clone();
        opts.relaxed_tasklist_matching = self.relaxed_tasklist_matching;
        opts.relaxed_autolinks = self.relaxed_autolinks;
        opts.ignore_setext = self.ignore_setext;
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
        }
    }
}

/// Python class that mirrors Comrak’s `RenderOptions`
#[pyclass(name = "RenderOptions")]
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
    pub list_style: u8, // store 42 = '*', 43 = '+', 45 = '-'
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
        // convert integer to ListStyleType
        opts.list_style = match self.list_style {
            43 => ListStyleType::Plus, // '+'
            42 => ListStyleType::Star, // '*'
            _ => ListStyleType::Dash,  // '-'
        };
        opts.sourcepos = self.sourcepos;
        opts.escaped_char_spans = self.escaped_char_spans;
        opts.ignore_empty_links = self.ignore_empty_links;
        opts.gfm_quirks = self.gfm_quirks;
        opts.prefer_fenced = self.prefer_fenced;
        opts.figure_with_caption = self.figure_with_caption;
        opts.tasklist_classes = self.tasklist_classes;
        opts.ol_width = self.ol_width;
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
            list_style: defaults.list_style as u8, // 45 if dash
            sourcepos: defaults.sourcepos,
            escaped_char_spans: defaults.escaped_char_spans,
            ignore_empty_links: defaults.ignore_empty_links,
            gfm_quirks: defaults.gfm_quirks,
            prefer_fenced: defaults.prefer_fenced,
            figure_with_caption: defaults.figure_with_caption,
            tasklist_classes: defaults.tasklist_classes,
            ol_width: defaults.ol_width,
        }
    }
}
