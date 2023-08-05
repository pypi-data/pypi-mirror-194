"""Asyncify ChemCloud
Asyncified components:
    - Result request
    - Result polling sleep
    - Compute request
TODO:
    - Refresh token?
"""
from chemcloud.models import (
    FutureResultBase,
    FutureResult,
    FutureResultGroup,
    AtomicInputOrList,
    PossibleResultsOrList,
    GROUP_ID_PREFIX,
)
from chemcloud.http_client import _RequestsClient
from chemcloud.client import CCClient
from chemcloud.utils import _b64_to_bytes, _bytes_to_b64

import trio
import httpx
from qcelemental.util.serialization import json_dumps
from time import time
from typing import Any


async def aget(
    self: FutureResult | FutureResultGroup,
    timeout: float | None = None,
    interval: float = 1.0,
) -> PossibleResultsOrList:
    if self.result:
        return self.result

    start_time = time()
    fid = self.id
    if type(self) is FutureResultGroup:
        fid = fid.replace(GROUP_ID_PREFIX, "")

    while True:
        _, self.result = await self.client.aresult(fid)
        if self.result:
            break
        if timeout:
            if (time() - start_time) > timeout:
                raise TimeoutError(
                    f"Your timeout limit of {timeout} seconds was exceeded"
                )
        await trio.sleep(interval)

    return self.result


FutureResultBase.aget = aget


async def _arequest(
    self,
    method: str,
    route: str,
    *,
    headers: dict[str, str] | None = None,
    data: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    api_call: bool = True,
):
    """Make HTTP request"""
    url = (
        f"{self._chemcloud_domain}"
        f"{self._settings.chemcloud_api_version_prefix if api_call else ''}{route}"
    )
    request = httpx.Request(
        method,
        url,
        headers=headers,
        data=data,
        params=params,
    )
    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0, read=20.0)) as client:
        response = await client.send(request)
    response.raise_for_status()
    return response.json()


async def _authenticated_arequest(self, method: str, route: str, **kwargs):
    """Make authenticated HTTP request"""
    kwargs["headers"] = kwargs.get("headers", {})
    access_token = self._get_access_token()
    kwargs["headers"]["Authorization"] = f"Bearer {access_token}"
    return await self._arequest(
        method,
        route,
        **kwargs,
    )


async def acompute(
    self, input_data: AtomicInputOrList, engine: str, queue: str | None = None
) -> FutureResult | FutureResultGroup:
    """Submit a computation to ChemCloud"""
    # Convery any bytes data to b64 encoding
    _bytes_to_b64(input_data)

    result_id = await self._authenticated_arequest(
        "post",
        "/compute",
        data=json_dumps(input_data),
        params={"engine": engine, "queue": queue},
    )
    return self._result_id_to_future_result(input_data, result_id)


async def aresult(
    self,
    result_id: str,
) -> tuple[str, PossibleResultsOrList | None]:
    result = await self._authenticated_arequest("get", f"/compute/result/{result_id}")
    if result["result"]:
        # Convery b64 encoded native_files to bytes
        _b64_to_bytes(result["result"])

    return result["state"], result["result"]


_RequestsClient._arequest = _arequest
_RequestsClient._authenticated_arequest = _authenticated_arequest
_RequestsClient.acompute = acompute
_RequestsClient.aresult = aresult


async def acompute(
    self, input_data: AtomicInputOrList, engine: str, queue: str | None = None
) -> FutureResult | FutureResultGroup:
    if self.supported_engines is not None:
        assert (
            engine in self.supported_engines
        ), f"Please use one of the following engines: {self.supported_engines}"

    return await self._client.acompute(input_data, engine, queue)


CCClient.acompute = acompute
