"""Main module for the Slack Plog package"""
import logging
from urllib.parse import urlparse
from logging.handlers import HTTPHandler
from slack_sdk.webhook import WebhookClient
from datetime import datetime


class SlackPlog(HTTPHandler):
    def __init__(self, slack_webhook_url: str):
        self.slack_webhook_url = slack_webhook_url
        parsed_url = urlparse(slack_webhook_url)
        # HTTPHandler.__init__(self, parsed_url.netloc, parsed_url.path, method="POST", secure=True)
        super().__init__(parsed_url.netloc, parsed_url.path, method="POST", secure=True)

    def emit(self, record: logging.LogRecord):
        map_record = self.mapLogRecord(record)
        # get the actual time
        created_at = datetime.fromtimestamp(map_record.get("created")).strftime("%Y-%m-%d %M:%s") # type: ignore
        log = f"{map_record.get('levelname')}:    {created_at} - {map_record.get('filename')} - {map_record.get('msg')} - lineno: {map_record.get('lineno')}"
        webhook = WebhookClient(self.slack_webhook_url)

        try:
            res = webhook.send(text=str(log))
            return res
        except Exception as e:
            print("error", e)
            pass
