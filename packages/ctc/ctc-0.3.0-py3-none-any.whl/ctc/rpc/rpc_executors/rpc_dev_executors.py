from __future__ import annotations

from ctc import spec

from .. import rpc_constructors
from .. import rpc_request
from .. import rpc_digestors


async def async_eth_get_compilers(
    *,
    provider: spec.ProviderReference = None,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_get_compilers()
    response = await rpc_request.async_send(request, provider=provider)
    return rpc_digestors.digest_eth_get_compilers(response=response)


async def async_eth_compile_lll(
    code: str, *, provider: spec.ProviderReference = None
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_compile_lll(code=code)
    response = await rpc_request.async_send(request, provider=provider)
    return rpc_digestors.digest_eth_compile_lll(response=response)


async def async_eth_compile_solidity(
    code: str, *, provider: spec.ProviderReference = None
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_compile_solidity(code=code)
    response = await rpc_request.async_send(request, provider=provider)
    return rpc_digestors.digest_eth_compile_solidity(response=response)


async def async_eth_compile_serpent(
    code: str, *, provider: spec.ProviderReference = None
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_compile_serpent(code=code)
    response = await rpc_request.async_send(request, provider=provider)
    return rpc_digestors.digest_eth_compile_serpent(response=response)
