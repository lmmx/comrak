use pyo3::prelude::*;

// We renamed the Rust library to `comrak_lib`
use comrak_lib::{markdown_to_html, Options as ComrakOptions};

// Import the Python option classes we defined
mod options;
use options::{PyExtensionOptions, PyParseOptions, PyRenderOptions};

/// Render a Markdown string to HTML, with optional Extension/Parse/Render overrides.
#[pyfunction(signature=(text, extension_options=None, parse_options=None, render_options=None))]
fn render_markdown(
    text: &str,
    extension_options: Option<PyExtensionOptions>,
    parse_options: Option<PyParseOptions>,
    render_options: Option<PyRenderOptions>,
) -> PyResult<String> {
    let mut opts = ComrakOptions::default();

    // If user provided custom extension options, apply them.
    if let Some(py_ext) = extension_options {
        py_ext.update_extension_options(&mut opts.extension);
    }

    if let Some(py_parse) = parse_options {
        py_parse.update_parse_options(&mut opts.parse);
    }

    if let Some(py_render) = render_options {
        py_render.update_render_options(&mut opts.render);
    }

    let html = markdown_to_html(text, &opts);
    Ok(html)
}

#[pymodule]
fn comrak(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Expose the function
    m.add_function(wrap_pyfunction!(render_markdown, m)?)?;

    // Expose the classes
    m.add_class::<PyExtensionOptions>()?;
    m.add_class::<PyParseOptions>()?;
    m.add_class::<PyRenderOptions>()?;

    Ok(())
}
