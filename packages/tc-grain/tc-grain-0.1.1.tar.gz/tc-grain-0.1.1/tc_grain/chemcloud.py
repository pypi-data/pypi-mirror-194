from . import chemcloud_trio_patch
from chemcloud import CCClient

from contextlib import asynccontextmanager


GRAIN_SWORKER_CONFIG = dict(
    BACKENDLESS=True,
)


@asynccontextmanager
async def grain_context():
    # Give the tasklets access to the client singleton
    ccclient = CCClient()
    yield ccclient


@asynccontextmanager
async def grain_run_sworker():
    # We don't actually run anything on the ground
    yield dict(
        name="ChemCloud",
    )
