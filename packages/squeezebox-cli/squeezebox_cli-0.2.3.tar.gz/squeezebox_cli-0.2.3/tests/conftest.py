import pytest


@pytest.fixture()
def requests_post(mocker):
    return mocker.patch('squeezebox_cli.core.protocol.requests.post')
