use pyo3::prelude::*;

extern crate oxide as ox;
use ox::weibull;

/// Weibull model
///
/// Args:
///     shape (float): Weibull model shape
///     scale (float): Weibull model scale
///     num_steps (int): length of time (unitless) for the reliability function
#[pyclass]
pub struct WeibullModel {
    shape: f64,
    scale: f64,
    reliability: Vec<f64>,
}

#[pymethods]
impl WeibullModel {
    #[new]
    pub fn new(shape: f64, scale: f64, num_steps: u32) -> Self {
        let weibull = weibull::WeibullModel::new(shape, scale);
        let reliability = weibull::reliability(weibull.weibull, num_steps);

        Self {
            shape,
            scale,
            reliability,
        }
    }

    #[getter]
    pub fn reliability(&self) -> PyResult<Vec<f64>> {
        Ok(self.reliability.clone())
    }

    #[getter]
    pub fn shape(&self) -> PyResult<f64> {
        Ok(self.shape)
    }

    #[getter]
    pub fn scale(&self) -> PyResult<f64> {
        Ok(self.scale)
    }
} 

#[pymodule]
pub fn weibull_model(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<WeibullModel>()?;
    Ok(())
}
