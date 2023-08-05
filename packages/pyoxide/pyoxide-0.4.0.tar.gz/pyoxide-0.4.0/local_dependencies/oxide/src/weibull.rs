use statrs::distribution::{Weibull, ContinuousCDF};

/// Weibull Model
#[derive(Debug, Clone)]
pub struct WeibullModel {
    /// The Weibull distribution shape
    pub shape: f64,
    /// The Weibull distribution scale
    pub scale: f64,
    /// The `statrs::distribution::Weibull` distribution
    pub weibull: Weibull,
}

impl WeibullModel {
    pub fn new(shape: f64, scale: f64) -> Self {
        let weibull = Weibull::new(shape, scale).unwrap();
        Self { shape, scale, weibull }
    }
}

/// Draw the reliability over time for a Weibull distribution
///
/// Given a Weibull distribution, draw the survival function over
/// time for a given number to unitless time steps.
///
/// # Arguments:
///
/// * `weibull`: an instance of `statrs::distribution::Weibull`
/// * `num_steps`: number of (unitless) time steps to draw the function over
///
/// ## Example:
///
/// ```
/// use statrs::distribution::{Weibull, ContinuousCDF};
/// use oxide::weibull::reliability;
///
/// let weibull = Weibull::new(0.5, 200.0).unwrap();
/// let reliability = reliability(weibull, 720);
/// ```
pub fn reliability(weibull: Weibull, num_steps: u32) -> Vec<f64> {
    (0..num_steps)
        .map(|x| weibull.sf(x as f64))
        .collect()
}
