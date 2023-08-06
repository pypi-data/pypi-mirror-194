import datetime as dt

import pytest

from siti.exc import InvalidCredentials, SitiError
from siti.http import Session


@pytest.mark.vcr
def test_invalid_auth():
    session = Session()
    with pytest.raises(InvalidCredentials) as e:
        session.configure(
            consumer_key='wrong', consumer_secret='creds', demo=True
        )
    assert (
        e.value.desc
        == 'A valid OAuth client could not be found for client_id: wrong'
    )


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_expired_token():
    session = Session()
    session.configure(demo=True)
    session.oauth_token.expires_at = dt.datetime(2020, 10, 22)
    assert session.oauth_token.is_expired
    session.configure(demo=True)
    assert not session.oauth_token.is_expired

    # making a petition so it will refresh the token
    session.oauth_token.expires_at = dt.datetime(2020, 10, 22)
    assert session.oauth_token.is_expired
    await session.get('/suptech-api/ifpe/1.0.0/reporte/pendientes')
    assert not session.oauth_token.is_expired


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_generic_exception():
    session = Session()
    session.configure(demo=True)
    with pytest.raises(SitiError) as ex:
        await session.get('/suptech-api/ifpe/1.0.0/reporte/pendientes')
    assert 'Error genérico' in str(ex.value)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_wrong_credentials():
    # this test tries to emulate that for some reason the token changed
    # midway though the session, so it will return an error
    session = Session()
    session.configure(demo=True)
    session.oauth_token.token = 'WRONG'
    with pytest.raises(SitiError) as ex:
        await session.get('/suptech-api/ifpe/1.0.0/reporte/pendientes')
    assert 'Invalid Credentials' in str(ex.value.desc)
