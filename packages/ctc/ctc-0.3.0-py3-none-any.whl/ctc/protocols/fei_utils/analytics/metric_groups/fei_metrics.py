from __future__ import annotations

import typing

from ctc import evm
from ctc.protocols import chainlink_utils
from ctc.protocols import fei_utils
from ctc.protocols import etherscan_utils

from ...coracle import coracle_spec
from .. import analytics_spec


async def async_compute_prices(
    blocks: typing.Sequence[int], verbose: bool = False
) -> analytics_spec.MetricGroup:
    from ctc.toolbox import pd_utils

    feed_data = await chainlink_utils.async_get_feed_data(
        feed='FEI_USD', start_block=blocks[0] - 10000
    )
    feed_data = feed_data
    # feed_data = evm.interpolate_block_series(
    #     series=feed_data, end_block=blocks[-1]
    # )
    feed_data = pd_utils.interpolate_series(
        series=feed_data,
        end_index=blocks[-1],
    )
    result = [feed_data[block] for block in blocks]

    return {
        'name': 'Prices',
        'metrics': {
            'usd_fei_chainlink': {
                'name': 'USD_FEI Chainlink',
                'values': result,
                'units': 'USD_FEI',
            },
        },
    }


async def async_compute_pfei_by_platform(
    blocks: typing.Sequence[int], verbose: bool = False
) -> analytics_spec.MetricGroup:

    deposit_balances = await fei_utils.async_get_fei_deposit_balances_by_block(
        blocks=blocks,
    )

    platform_balances = fei_utils.fei_deposits_to_deployments_by_block(
        deposit_balances
    )

    # gather links
    links_by_platform: typing.MutableMapping[
        str, typing.MutableSequence[str]
    ] = {}
    for deposit in deposit_balances.keys():
        platform = coracle_spec.deposit_metadata.get(deposit, {}).get(
            'platform'
        )
        if platform is not None:
            url = etherscan_utils.create_address_url(deposit)
            links_by_platform.setdefault(platform, [])
            links_by_platform[platform].append(url)

    metrics: dict[str, analytics_spec.MetricData] = {}
    for name, values in platform_balances.items():
        metrics[name] = {
            'name': name,
            'values': values,
            'links': links_by_platform.get(name, []),
            'units': 'FEI',
        }

    return {
        'name': 'Protocol FEI By Platform',
        'metrics': metrics,
    }


#
# # dex data
#


async def async_compute_dex_tvls(
    blocks: typing.Sequence[int],
    verbose: bool = False,
) -> analytics_spec.MetricGroup:
    import asyncio

    pools = analytics_spec.dex_pools

    names = list(pools.keys())
    addresses = [pool['address'] for pool in pools.values()]

    _chunk_by_blocks = False
    if _chunk_by_blocks:
        tasks: list[asyncio.Task[typing.Union[list[int], list[float]]]] = []
        for block in blocks:
            task = evm.async_get_erc20_balances_of_addresses(
                wallets=addresses,
                token='FEI',
                block=block,
            )
            tasks.append(asyncio.create_task(task))
        results = await asyncio.gather(*tasks)
        results = list(zip(*results))

    else:
        tasks = []
        for address in addresses:
            task = evm.async_get_erc20_balance_by_block(
                wallet=address,
                token='FEI',
                blocks=blocks,
            )
            tasks.append(asyncio.create_task(task))
        results = await asyncio.gather(*tasks)

    tvl_by_pool = dict(zip(names, results))

    tvl_by_pool = {
        pool: {'values': tvl, 'units': 'FEI', 'name': pool}
        for pool, tvl in tvl_by_pool.items()
    }

    # sum by platform
    tvl_by_platform = {}
    for pool_name, pool_info in analytics_spec.dex_pools.items():
        pool_tvl = tvl_by_pool[pool_name]
        platform = pool_info['platform']
        if platform not in tvl_by_platform:
            tvl_by_platform[platform] = pool_tvl
        else:
            assert pool_tvl['units'] == tvl_by_platform[platform]['units']
            tvl_by_platform[platform]['values'] = [
                sum(datapoints)
                for datapoints in zip(
                    pool_tvl['values'],
                    tvl_by_platform[platform]['values'],
                )
            ]

    return {
        'name': 'DEX TVL by Platform',
        'metrics': tvl_by_platform,
    }
