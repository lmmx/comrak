use comrak_lib::{markdown_to_html, ComrakOptions};
use pyo3::prelude::*;

#[pyfunction]
fn render_markdown(text: &str) -> PyResult<String> {
    let options = ComrakOptions::default();
    let html = markdown_to_html(text, &options);
    Ok(html)
}

#[pymodule]
fn comrak(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // In this style, `m` is an ephemeral reference to the module
    // instead of a plain &PyModule.
    m.add_function(wrap_pyfunction!(render_markdown, m)?)?;
    Ok(())
}
