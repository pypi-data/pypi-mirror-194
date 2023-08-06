# pytest-hpfeeds

pytest-hpfeeds is a collection of boilerplate to help with smoke/integration testing of honeypots against a hpfeeds broker. It leverages pytest-docker-tools to manage running a test broker inside docker. It provides a `hpfeeds_client` fixture to provide your pytest with a client connected to that broker.


## hpfeeds_broker

This package provides a `hpfeeds_broker` fixture. By referencing this fixture from a test pytest-hpfeeds will automatically start a broker (in a container) before your test and destroy it after the test is completed.

```python
def test_my_broker(hpfeeds_broker):
    assert hpfeeds_broker.ips.primary is not None
```

By default the broker is configured with a single user (`test` with a secret of `test`) and a single channel called `test`.


## hpfeeds_client

The package also provides a `hpfeeds_client` fixture. This is an instance of `hpfeeds.asyncio.ClientSession` that is already connected to your broker. Because the client depends on the `hpfeeds_broker` you don't need to reference it, pytest will still automatically start and stop the broker as needed.

```python
async def test_my_client(hpfeeds_client):
    hpfeeds_client.subscribe('test')
    hpfeeds_client.publish('test', 'hello')
    assert await hpfeeds_client.read() == ('test', 'test', b'hello')
```


## hpfeeds_broker_channels

You can implement this fixture in your `conftest.py` to change which channels your broker knows about.

```python
import pytest

@pytest.fixture()
def hpfeeds_broker_channels():
    return ["cowrie.sessions"]

async def test_my_client(hpfeeds_client):
    hpfeeds_client.subscribe('cowrie.sessions"')
    hpfeeds_client.publish('cowrie.sessions"', 'hello')
    assert await hpfeeds_client.read() == ('test', 'cowrie.sessions"', b'hello')
```


## Testing a honeypot in practice

You have packaged a honeypot and you want to write an end to end test to make sure that it functions as expected.

If you have a honeypot in the current directory with a `Dockerfile` you can write a `conftest.py` like this:

```python
import pathlib

from pytest_docker_tools import image_or_build

CURRENT_DIR = pathlib.Path(__file__).parent

image = image_or_build(
    environ_key='IMAGE_ID',
    path=str(CURRENT_DIR),
)

honeypot = container(
    image=image,
    environment={
        "OUTPUT_HPFEEDS_HOST": "{hpfeeds_broker.ips.primary}",
        "OUTPUT_HPFEEDS_PORT": "20000",
        "OUTPUT_HPFEEDS_IDENT": "test",
        "OUTPUT_HPFEEDS_SECRET": "test",
        "OUTPUT_HPFEEDS_CHANNEL": "test",
    },
    ports={"8443/tcp": None},
    user="nobody",
    read_only=True,
)
```

To learn more about what this is doing, you should read the pytest-docker-tools [README](https://github.com/Jc2k/pytest-docker-tools/blob/main/README.md). But some key points are:

* Variables are automatically interpolated against pytest fixtures. So `"{hpfeeds_broker.ips.primary}"` resolves the `hpfeeds_broker` fixture (causing an ephemeral broker container to be started) and gets its main IP to pass to your honeypot image.
* The `image` fixture lets you test an existing image (one that exists locally). The `build` fixture lets you do iterative development - it effectively does `docker build` every time you run your tests. Sometimes you want both. You want your development environment to use the `buld` fixture, but your release pipeline should use the `image` fixture so that it is testing the exact image (bit for bit) that will be deployed. That's what the `image_or_build` fixture is for. If your CI pipeline sets the `IMAGE_ID` environment variable then the existing image is tested. Otherwise pytest will `docker build` a new image.

Now to test this honeypot you can write a test:

```python
import json

import httpx


async def test_honeypot_logs_data(honeypot, hpfeeds_client):
    hpfeeds_client.subscribe("test")

    ip, port = honeypot.get_addr("8443/tcp")

    # Simulate simulating an attack on the honeypot
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{ip}:{port}/some-endpoint")
        assert r.status_code == 200

    ident, channel, event = await hpfeeds_client.read()

    # Verify the event is correct and that the structure hasn't changed
    assert json.loads(event) == {
        "event": "http.get",
        # ....
    }

```

By using `pytest-hpfeeds` and `pytest-docker-tools` most of the heavy lifting of build and starting your containerised honeypot and connecting it to a hpfeeds broker is hidden away. You can concentrating on simulating attacks against the honeypot and verifying the hpfeeds output, making it safe to rapidly deploy to your production environment without regressing your event processing backend.
