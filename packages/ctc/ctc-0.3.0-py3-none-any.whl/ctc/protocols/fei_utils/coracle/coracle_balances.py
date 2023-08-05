from __future__ import annotations

import typing

from ctc import evm
from ctc import rpc
from ctc import spec
from ctc.toolbox import nested_utils

from . import coracle_tokens
from . import coracle_oracles
from . import coracle_deposits
from . import coracle_spec


function_abis: dict[str, spec.FunctionABI] = {
    'balance': {
        'inputs': [],
        'name': 'balance',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function',
    },
    'resistantBalanceAndFei': {
        'inputs': [],
        'name': 'resistantBalanceAndFei',
        'outputs': [
            {
                'internalType': 'uint256',
                'name': '_resistantBalance',
                'type': 'uint256',
            },
            {
                'internalType': 'uint256',
                'name': '_resistantFei',
                'type': 'uint256',
            },
        ],
        'stateMutability': 'view',
        'type': 'function',
    },
}


#
# # deposit balance getters
#


async def async_get_deposit_balance(
    deposit: spec.ContractAddress,
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    provider: spec.ProviderReference = None,
) -> typing.Union[int, typing.Sequence[int]]:
    """get token balance of a particular deposit"""
    result = await rpc.async_eth_call(
        to_address=deposit,
        function_abi=function_abis['balance'],
        block_number=block,
        provider=provider,
    )
    if not (isinstance(result, int) or isinstance(result, list)):
        raise Exception('invalid rpc result')
    return typing.cast(typing.Union[int, typing.Sequence[int]], result)


async def async_get_deposits_balances(
    deposits: typing.Sequence[spec.ContractAddress],
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    provider: spec.ProviderReference = None,
) -> list[int]:
    return await rpc.async_batch_eth_call(
        to_addresses=deposits,
        function_abi=function_abis['balance'],
        block_number=block,
        provider=provider,
    )


async def async_get_deposit_balance_by_block(
    deposit: spec.ContractAddress,
    *,
    blocks: typing.Sequence[spec.BlockReference],
    provider: spec.ProviderReference = None,
) -> list[int]:
    return await rpc.async_batch_eth_call(
        to_address=deposit,
        function_abi=function_abis['balance'],
        block_numbers=blocks,
        provider=provider,
    )


async def async_get_deposit_resistant_balance_and_fei(
    deposit: spec.ContractAddress,
    *,
    block: typing.Optional[spec.BlockReference] = None,
    provider: spec.ProviderReference = None,
) -> typing.Union[int, typing.Sequence[int]]:
    """get token balance of a particular deposit"""
    result = await rpc.async_eth_call(
        to_address=deposit,
        function_abi=function_abis['resistantBalanceAndFei'],
        block_number=block,
        provider=provider,
    )
    if not (isinstance(result, int) or isinstance(result, list)):
        raise Exception('invalid rpc result')
    return typing.cast(typing.Union[int, typing.Sequence[int]], result)


async def async_get_deposits_resistant_balances_and_fei(
    deposits: typing.Sequence[spec.ContractAddress],
    *,
    block: typing.Optional[spec.BlockReference] = None,
    provider: spec.ProviderReference = None,
) -> list[tuple[int, int]]:
    return await rpc.async_batch_eth_call(
        to_addresses=deposits,
        function_abi=function_abis['resistantBalanceAndFei'],
        block_number=block,
        provider=provider,
    )


async def async_get_deposit_resistant_balance_and_fei_by_block(
    deposit: spec.ContractAddress,
    *,
    blocks: typing.Sequence[spec.BlockReference],
    provider: spec.ProviderReference = None,
) -> list[int]:
    return await rpc.async_batch_eth_call(
        to_address=deposit,
        function_abi=function_abis['resistantBalanceAndFei'],
        block_numbers=blocks,
        provider=provider,
    )


#
# # token balance getters
#


async def async_get_token_balance(
    token: spec.Address,
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    provider: spec.ProviderReference = None,
    normalize: bool = True,
    usd: bool = False,
) -> typing.Union[int, float]:

    if block is None:
        block = 'latest'
    if block is not None:
        block = await evm.async_block_number_to_int(
            block=block, provider=provider
        )
    deposits = await coracle_deposits.async_get_token_deposits(
        token=token, block=block, provider=provider
    )
    balances = await async_get_deposits_balances(
        deposits=deposits, block=block, provider=provider
    )
    balance: typing.Union[int, float] = sum(balances)

    if normalize:
        if token == coracle_spec.usd_token:
            balance = balance / 1e18
        elif balance == 0:
            pass
        else:
            balance = await evm.async_normalize_erc20_quantity(
                quantity=balance,
                provider=provider,
                token=token,
            )

    if usd:
        if not normalize:
            raise Exception('must normalize for usd conversion')
        token_price = await coracle_oracles.async_get_token_price(
            token=token,
            block=block,
            provider=provider,
            normalize=True,
        )
        balance = balance * token_price

    return balance


async def async_get_token_balance_by_block(
    token: spec.Address,
    *,
    blocks: typing.Sequence[spec.BlockNumberReference],
    provider: spec.ProviderReference = None,
    normalize: bool = True,
    usd: bool = False,
) -> typing.Union[list[int], list[float]]:
    import asyncio

    coroutines = [
        async_get_token_balance(
            token=token,
            provider=provider,
            normalize=normalize,
            block=block,
            usd=usd,
        )
        for block in blocks
    ]
    return await asyncio.gather(*coroutines)


async def async_get_tokens_balances(
    *,
    tokens: typing.Sequence[spec.Address] | None = None,
    block: spec.BlockNumberReference | None = None,
    provider: spec.ProviderReference = None,
    normalize: bool = True,
    usd: bool = False,
    exclude_fei: bool = True,
) -> typing.Union[dict[spec.Address, int], dict[spec.Address, float]]:

    if block is None:
        block = 'latest'
    block = await evm.async_block_number_to_int(block=block, provider=provider)

    # use all tokens in pcv by default
    if tokens is None:
        tokens = await coracle_tokens.async_get_tokens_in_pcv(
            block=block, provider=provider
        )
    if exclude_fei:
        FEI = '0x956f47f50a910163d8bf957cf5846d573e7f87ca'
        tokens = [token for token in tokens if token != FEI]

    # get deposits for each token
    tokens_deposits = await coracle_deposits.async_get_tokens_deposits(
        tokens=tokens, block=block, provider=provider
    )

    # get deposit balances
    all_deposits = [
        deposit
        for token_deposits in tokens_deposits.values()
        for deposit in token_deposits
    ]
    all_balances = await async_get_deposits_balances(
        deposits=all_deposits,
        provider=provider,
        block=block,
    )
    all_balances_iter = iter(all_balances)
    deposits_balances: dict[str, list[int]] = {}
    for token, token_deposits in tokens_deposits.items():
        deposits_balances[token] = []
        for _ in token_deposits:
            deposits_balances[token].append(next(all_balances_iter))

    # sum deposits balances of each token
    tokens_balances: dict[str, typing.Union[int, float]] = {
        token: sum(token_balances)
        for token, token_balances in deposits_balances.items()
    }

    # normalize
    if normalize:

        # normalize only non-usd tokens with non-zero balance
        normalize_tokens = []
        for token in tokens:
            if token != coracle_spec.usd_token and tokens_balances[token] > 0:
                normalize_tokens.append(token)

        # normalize and replace
        normalized = await evm.async_normalize_erc20s_quantities(
            quantities=[tokens_balances[token] for token in normalize_tokens],
            tokens=normalize_tokens,
            block=block,
            provider=provider,
        )
        for token, normalized_balance in zip(normalize_tokens, normalized):
            tokens_balances[token] = normalized_balance

        # normalize usd balance
        if coracle_spec.usd_token in tokens:
            tokens_balances[coracle_spec.usd_token] /= 1e18

    if usd:
        if not normalize:
            raise Exception('must normalize for usd conversion')
        token_prices = await coracle_oracles.async_get_tokens_prices(
            tokens=tokens,
            block=block,
            provider=provider,
            normalize=True,
        )
        tokens_balances = {
            token: tokens_balances[token] * token_price
            for token, token_price in zip(tokens_balances, token_prices)
        }

    return tokens_balances


async def async_get_tokens_balances_by_block(
    blocks: typing.Sequence[spec.BlockNumberReference],
    *,
    tokens: typing.Optional[typing.Sequence[spec.Address]] = None,
    provider: spec.ProviderReference = None,
    normalize: bool = True,
    usd: bool = False,
    exclude_fei: bool = True,
) -> typing.Union[
    typing.Mapping[spec.Address, list[int]],
    typing.Mapping[spec.Address, list[float]],
]:
    from ctc.toolbox import async_utils

    coroutines = [
        async_get_tokens_balances(
            tokens=tokens,
            provider=provider,
            normalize=normalize,
            block=block,
            usd=usd,
            exclude_fei=exclude_fei,
        )
        for block in blocks
    ]
    block_token_balances = await async_utils.async_gather_coroutines(
        *coroutines
    )

    if normalize:
        if typing.TYPE_CHECKING:
            int_type = typing.List[typing.Dict[spec.Address, int]]
            int_result = typing.cast(int_type, block_token_balances)
            return nested_utils.list_of_dicts_to_dict_of_lists(int_result)
        else:
            return nested_utils.list_of_dicts_to_dict_of_lists(
                block_token_balances
            )
    else:
        if typing.TYPE_CHECKING:
            float_type = typing.List[typing.Dict[spec.Address, float]]
            float_result = typing.cast(float_type, block_token_balances)
            return nested_utils.list_of_dicts_to_dict_of_lists(float_result)
        else:
            return nested_utils.list_of_dicts_to_dict_of_lists(
                block_token_balances
            )
