use statrs::distribution::{Weibull, ContinuousCDF};

#[derive(Debug, Clone)]
pub struct WeibullModel {
    pub shape: f64,
    pub scale: f64,
    pub weibull: Weibull,
}

impl WeibullModel {
    pub fn new(shape: f64, scale: f64) -> Self {
        let weibull = Weibull::new(shape, scale).unwrap();
        Self { shape, scale, weibull }
    }
}

pub fn reliability(weibull: Weibull, num_steps: u32) -> Vec<f64> {
    let mut reliability: Vec<f64> = Vec::new();
    for x in 0..num_steps {
        let val = weibull.sf(x as f64);
        reliability.push(val);
    }

    reliability
}
