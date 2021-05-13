from pytest_mock import MockerFixture
from flask import url_for


def test_webhook_auth(client, mocker: MockerFixture):
    class MockAuthReponse:
        status = 200

        @property
        def status_code(self):
            return self.status

        def json(self):
            return {
                "webhook": {
                    "channel_id": "123",
                    "id": "564",
                    "token": "secret"
                }
            }

    mocker.patch('web.controllers.auth.exchange_token', return_value=MockAuthReponse())
    mocker.patch('web.controllers.auth.save_webhook_info', return_value=True)

    r = client.get(
        url_for('auth.webhook'),
        query_string={'code': "davidism", 'guild_id': "123"},
        follow_redirects=True
    )

    assert r.status_code == 200
    assert b'flashes' in r.data

    MockAuthReponse.status = 400
    r = client.get(
        url_for('auth.webhook'),
        query_string={'code': "davidism", 'guild_id': "123"},
        follow_redirects=True
    )

    assert r.status_code == 200
    assert b'flashes' in r.data