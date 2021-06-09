import pandas as pd
from itertools import chain, repeat
from collections import namedtuple

from blueshift_calendar import get_calendar
from blueshift_data.readers import Library

from zipline_pipeline.pipeline import Pipeline, SimplePipelineEngine
from zipline_pipeline.pipeline import CustomFilter, CustomFactor
from zipline_pipeline.pipeline.data import EquityPricing
from zipline_pipeline.pipeline.loaders import EquityPricingLoader
import zipline_pipeline.pipeline.domain as domain
from blueshift_data.pipeline.domain import PricingDomain, BLUESHIFT_PIPELINE_SUPPORT
from blueshift_data.pipeline.data import BlueshiftEquityPricing

def filter_universe(universe):
    class FilteredUniverse(CustomFilter):
        inputs = ()
        window_length = 1
        def compute(self,today,assets,out):
            in_universe = [True for asset in assets if asset not in universe]
            out[:] = in_universe
    
    return FilteredUniverse()

def period_returns(lookback):
    class SignalPeriodReturns(CustomFactor):
        inputs = [EquityPricing.close]
        def compute(self,today,assets,out,close_price):
            start_price = close_price[0]
            end_price = close_price[-1]
            returns = end_price/start_price - 1
            out[:] = returns
    
    return SignalPeriodReturns(window_length = lookback)

def make_strategy_pipeline(universe):
    pipe = Pipeline()
    momentum = period_returns(100)
    pipe.add(momentum,'momentum')
    universe_filter = filter_universe(universe)
    pipe.set_screen(universe_filter)

    return pipe

# set up engine
cal = get_calendar('NYSE')
lib = Library("C:/Users/prodi/.blueshift/data/library/us-equities")
daily_store = list(lib['1d'])[0]
minute_store = list(lib['1m'])[0]
adj_handler = minute_store.adjustments_handler
pipeline_loader = EquityPricingLoader.without_fx(daily_store, adj_handler)
#BLUESHIFT_US_EQUITIES = domain.StoreDomain(daily_store)
#BlueshiftUSEquityPricing = EquityPricing.specialize(BLUESHIFT_US_EQUITIES)
PricingDomain.set_store(daily_store)

def get_loader(column):
    if column in BlueshiftEquityPricing.columns:
        return pipeline_loader
    raise ValueError(
        "No PipelineLoader registered for column %s." % column
    )

engine = SimplePipelineEngine(
            get_loader,
            lib,
            #domain.StoreDomain(daily_store),
            #BLUESHIFT_US_EQUITIES,
            PricingDomain,
        )

# setup pipeline
AttachedPipeline = namedtuple('AttachedPipeline', ['pipe','chunks', 'eager'])
pipelines = {}
chunks = chain([5], repeat(126))
eager = True
pipeline = make_strategy_pipeline([])
pipelines['test'] = AttachedPipeline(pipeline, iter(chunks), eager)

# run pipeline
start_session = pd.Timestamp('2010-02-01')
end_session = pd.Timestamp('2010-04-30')
pipe, chunks, _ = pipelines['test']
chunksize = next(chunks)
sessions = cal.all_sessions
start_date_loc = sessions.get_loc(start_session)
end_loc = min(
            start_date_loc + chunksize,
            sessions.get_loc(end_session)
        )
start_session = sessions[start_date_loc]
end_session = sessions[end_loc]

res = engine.run_pipeline(pipe, start_session, end_session)
