import pytest
from discord import RequestsWebhookAdapter, Webhook

from Helpers.db_helper import DiscordHelper, ReleaseHelper


@pytest.mark.usefixtures("session")
class TestDiscorHelper:
    def test_make_webhooks(self):
        adapter = RequestsWebhookAdapter()
        webhooks = DiscordHelper.make_discord_webhooks(adapter)
        for webhook in webhooks:
            assert isinstance(webhook, Webhook)


@pytest.mark.usefixtures("session")
def test_release_helper(session):
    ReleaseHelper.fetch_new_releases(session)
