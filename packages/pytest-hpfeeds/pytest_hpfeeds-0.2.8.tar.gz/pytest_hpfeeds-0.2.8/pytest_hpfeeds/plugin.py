import asyncio
import os

from hpfeeds.asyncio import ClientSession
import pytest
from pytest_docker_tools import container, fetch
from pytest_docker_tools.wrappers import Container


@pytest.fixture(scope="session")
def hpfeeds_broker_channels():
    return ["test"]


@pytest.fixture(scope="session")
def hpfeeds_broker_environment(hpfeeds_broker_channels):
    channels = ",".join(hpfeeds_broker_channels)
    return {
        "HPFEEDS_TEST_SECRET": "test",
        "HPFEEDS_TEST_SUBCHANS": channels,
        "HPFEEDS_TEST_PUBCHANS": channels,
    }


hpfeeds_broker_image = fetch(repository="hpfeeds/hpfeeds-broker:latest")

hpfeeds_broker = container(
    image="{hpfeeds_broker_image.id}",
    environment=hpfeeds_broker_environment,
    command=[
        "/app/bin/hpfeeds-broker",
        "--bind=0.0.0.0:20000",
        # Read user creds from environment variables
        "--auth=env",
    ],
    ports={
        "20000/tcp": None,
    },
)

hpfeeds_broker_session = container(
    image="{hpfeeds_broker_image.id}",
    environment=hpfeeds_broker_environment,
    command=[
        "/app/bin/hpfeeds-broker",
        "--bind=0.0.0.0:20000",
        # Read user creds from environment variables
        "--auth=env",
    ],
    ports={
        "20000/tcp": None,
    },
    scope="session",
)


@pytest.fixture(scope="function")
async def hpfeeds_client(
    hpfeeds_broker: Container, loop: asyncio.AbstractEventLoop
) -> ClientSession:
    if os.environ.get("CI", ""):
        host = hpfeeds_broker.ips.primary
        port = 20000
    else:
        host = "127.0.0.1"
        port = int(hpfeeds_broker.ports["20000/tcp"][0])

    async with ClientSession(host, port, "test", "test") as session:
        yield session


@pytest.fixture(scope="function")
async def hpfeeds_client_session(
    hpfeeds_broker_session: Container, loop: asyncio.AbstractEventLoop
) -> ClientSession:
    if os.environ.get("CI", ""):
        host = hpfeeds_broker_session.ips.primary
        port = 20000
    else:
        host = "127.0.0.1"
        port = int(hpfeeds_broker_session.ports["20000/tcp"][0])

    async with ClientSession(host, port, "test", "test") as session:
        yield session
