import os

import requests
from slack_sdk import WebClient

from slack_sdk.errors import SlackApiError

from dvttestkit import testKitUtils

logger = testKitUtils.makeLogger(__name__, True, 'DEBUG')
slackClient = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


def archive_channel(channel_id: str, slack_app_token: str) -> dict:
    """Archive a channel in Slack.

    Parameters:
    channel_id (str): The ID of the channel to archive.
    slack_app_token (str): The token of the Slack app.

    Returns:
    dict: The response from the Slack API.
    """
    # Set the Slack API endpoint
    endpoint = f"https://slack.com/api/conversations.archive?" \
               f"token={slack_app_token}&channel={channel_id}"

    # Send the API request to archive the channel
    # Return the response from the API
    return requests.post(endpoint).json()


def post_slack_message(
        _msg: str = "testKitUtils.py tested successfully!",
        channel: str = os.environ.get('slack_channel', "C049467E5QQ"),
        ts: str = None,
        _reply_broadcast: bool = False
):
    """
    Posts a message to slack, If this file is run by itself, posts test msg.
    :param _reply_broadcast:
    :param ts:
    :param channel: Slack channel
    :param _msg: Message to post
    :return: "ts" id for reply messages
    """
    try:
        response = slackClient.chat_postMessage(
            channel=channel,
            thread_ts=ts,
            reply_broadcast=_reply_broadcast,
            text=str(_msg)
        )
        return response['ts']
    except SlackApiError as error:
        # You will get a SlackApiError if "ok" is False
        assert error.response["ok"] is False
        assert error.response["error"]
        print(f"Got an error: {error.response['error']}")


def get_slack_messages(
        channel_name: str = os.getenv('slack_channel', "C049467E5QQ")):
    conversation_id = None
    try:
        # Call the conversations.list method using the WebClient
        for result in slackClient.conversations_list():
            if conversation_id is not None:
                break
            for channel in result["channels"]:
                if channel["id"] == channel_name:
                    conversation_id = channel["id"]
                    # Print result
                    print(f"Found conversation ID: {conversation_id}")
                    break

    except SlackApiError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Replace YOUR-SLACK-APP-TOKEN with your Slack app's token
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
    # Replace CHANNEL-ID with the ID of the channel you want to archive
    CHANNEL_ID = os.getenv("SLACK_APP_CHANNEL")

    # Call the function to archive the channel
    print(archive_channel(CHANNEL_ID, SLACK_APP_TOKEN))
