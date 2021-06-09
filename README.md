# Zipline Pipeline

A fork of the pipline module from zipline. This makes pipeline features from 
zipline easy to integrate with an independent module. To integrate your 
backtesting system, do the following:

- Subclass the `zipline_pipeline.pipeline.domain.Domain` class
- Subclass the `zipline_pipeline.pipeline.data.dataset.DataSet` class
- Instantiate a new custom `DataSet` object with an instance of the custom domain
- Subclass the `zipline_pipeline.pipeline.loaders.EquityPricingLoader`, or
    use instantiate the default one with your data reader and adjustment 
    reader objects. The data-reader must be a daily data reader and have the 
    method `load_raw_arrays`. The adjustment reader must have the method 
    `load_pricing_adjustments`.
- Instantiate a `SimplePipelineEngine` with the pipeline loader, and your 
    own `AssetFinder`. The `AssetFinder` object must implement the method 
    `lifetimes`.