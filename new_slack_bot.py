# from slack_bot_app.models import Team
from slackclient import SlackClient
from django.core.management.base import BaseCommand
import time
from django.db import models
# from slack_bot_app.models import Team, Message, Thread

BOT_ID = "U8CQ7DP53"
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient("xoxb-284823465173-p8VkMbMx9DDQhJ8kOo9Tdzxl")


def handle_command(command, channel, user):

    channel = 'for_new' # name channel for send
    response = user + " " + command
    slack_client.api_call("chat.postMessage", channel=channel, user=user,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    channel = 'for_new'
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text'] and 'user' in output:
                print(output['user'])
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       channel, output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            print(user)
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")