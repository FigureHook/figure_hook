from collections import namedtuple
from typing import Iterable

from discord import RequestsWebhookAdapter

from constants import PeriodicTask
from database import pgsql_session
from Models import Task, Webhook
from Sender.discord_hooker import DiscordHooker
from utils.announcement_checksum import (AlterChecksum, GSCChecksum,
                                         SiteChecksum)
from utils.data_access import (make_discord_webhooks,
                               make_newly_release_embeds_after)
from utils.scrapyd_api import schedule_spider

from .celery import app


@app.task
def news_push():
    this_task: Task
    with pgsql_session():
        this_task = Task.query.get(PeriodicTask.NEWS_PUSH)
        adapter = RequestsWebhookAdapter()
        discord_webhooks = make_discord_webhooks(adapter)
        embeds = make_newly_release_embeds_after(this_task.executed_at)
        this_task.update()
        hooker = DiscordHooker(discord_webhooks, embeds=embeds)
        hooker.send()

        webhooks: Iterable[Webhook] = Webhook.all()
        for webhook in webhooks:
            is_existed = hooker.webhook_status.get(webhook.id)
            if is_existed is not None:
                webhook.update(is_existed=is_existed)

    return hooker.stats


@app.task
def check_new_release():
    scheduled_jobs = []
    with pgsql_session():
        CheckingPair = namedtuple("CheckingPair", ["checksum_cls", "spider_name"])
        sites_to_check = [
            CheckingPair(AlterChecksum, "alter_recent"),
            CheckingPair(GSCChecksum, "gsc_recent")
        ]
        for checking_pair in sites_to_check:
            checksum: SiteChecksum = checking_pair.checksum_cls()
            if checksum.is_changed:
                response = schedule_spider(checking_pair.spider_name)
                scheduled_jobs.append(response)
                checksum.update()
    return scheduled_jobs