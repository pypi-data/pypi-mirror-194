from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def demo():
    with patch(
        'siti.resources.ifpe.base.ResourceIFPE._endpoint',
        '/suptech-api/ifpe/1.0.0',
    ):
        yield


@pytest.fixture(scope='module')
def vcr_config():
    config = dict()
    config['filter_headers'] = [
        ('Authorization', 'DUMMY'),
    ]
    return config
