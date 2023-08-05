"""Datafeed for pseudorandom number from hashing multiple blockhashes together."""
from typing import Optional

import chained_accounts
from telliot_core.model.endpoints import RPCEndpoint

from telliot_feeds.datafeed import DataFeed
from telliot_feeds.queries.tellor_rng import TellorRNG
from telliot_feeds.sources.blockhash_aggregator import TellorRNGManualSource

local_source = TellorRNGManualSource()

tellor_rng_feed = DataFeed(source=local_source, query=TellorRNG(timestamp=local_source.timestamp))


async def assemble_rng_datafeed(
    timestamp: int, node: RPCEndpoint, account: chained_accounts
) -> Optional[DataFeed[float]]:
    """Assembles a TellorRNG datafeed for the given timestamp."""
    local_source.set_timestamp(timestamp)
    feed = DataFeed(source=local_source, query=TellorRNG(timestamp=timestamp))

    return feed
