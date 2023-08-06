mod weibull;

use pyo3::prelude::*;
use pyo3::wrap_pymodule;

#[pymodule]
fn oxide(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(weibull::weibull))?;
    Ok(())
}
