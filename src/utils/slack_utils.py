import json
import logging

import requests

from src import PROJECT_ENVS
from src.constants import Envs, LogLevels

logger = logging.getLogger(__name__)


class SlackNotifier:
    def __init__(self, webhook_url: str, default_metadata: dict = None):
        """
        Initialize a generic Slack notifier.

        Args:
            webhook_url: Slack webhook URL for sending messages
            default_metadata: Optional default metadata to include in all messages
        """
        self.webhook_url = webhook_url
        self.default_metadata = default_metadata or {}

    def _send_to_slack(self, payload: dict):
        if PROJECT_ENVS.ENV_STATE == Envs.PROD.value:
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                logger.debug("Message sent to Slack successfully.")
            else:
                logger.warning(
                    f"Failed to send message to Slack. Status code: {response.status_code}, Response: {response.text}"
                )
        else:
            logger.info(payload)

    def post_message(
        self,
        message: str,
        level: LogLevels = LogLevels.DEBUG,
        metadata: dict = None,
        help_link: str = None,
    ):
        """Post an error message to Slack."""
        combined_metadata = {**self.default_metadata, **(metadata or {})}
        metadata_text = "\n".join(f"*{k}:* {v}" for k, v in combined_metadata.items())
        log_lvl_msg = f":{level.value}: "
        block_id = (
            "section_error"
            if level == LogLevels.ERROR
            else "section_warning" if level == LogLevels.WARNING else "section"
        )
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": metadata_text,
                },
            },
            {
                "type": "section",
                "block_id": block_id,
                "fields": [{"type": "mrkdwn", "text": f"{log_lvl_msg}\n```{message}```"}],
            },
        ]

        if help_link:
            blocks.append(
                {
                    "type": "section",
                    "block_id": "section_help",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{help_link}|Click here> for more details or troubleshooting.",
                    },
                }
            )

        payload = {
            "text": message,
            "blocks": blocks,
        }
        self._send_to_slack(payload)


if __name__ == "__main__":
    # Example usage with a webhook URL and optional metadata
    webhook_url = "https://hooks.slack.com/services/your-webhook-url-here"
    metadata = {"service": "example-service", "environment": "test"}

    notifier = SlackNotifier(webhook_url, metadata)
    notifier.post_message("Process started successfully.", level=LogLevels.INFO)
    notifier.post_message("Resource usage is high.", level=LogLevels.WARNING)
    notifier.post_message(
        "An error occurred during execution.",
        level=LogLevels.ERROR,
        help_link="https://example.com/help",
    )
