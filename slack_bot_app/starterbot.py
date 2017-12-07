import os
import time
from slackclient import SlackClient
from django.conf import settings


# # starterbot's ID as an environment variable
# BOT_ID = "U8B4AM812" # settings.BOT_ID #os.environ.get("BOT_ID")
#
# # constants
# AT_BOT = "<@" + BOT_ID + ">"
# EXAMPLE_COMMAND = "do"
#
# # instantiate Slack & Twilio clients
# slack_client = SlackClient("xoxb-283146722036-v8pYN2wwFJ005hmqhiQo7SM0") # settings.SLACK_BOT_TOKEN) # SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
#
#
# def handle_command(command, channel):
#     """
#         Receives commands directed at the bot and determines if they
#         are valid commands. If so, then acts on the commands. If not,
#         returns back what it needs for clarification.
#     """
#     response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
#                "* command with numbers, delimited by spaces."
#     if command.startswith(EXAMPLE_COMMAND):
#         response = "Sure...write some more code then I can do that!"
#     slack_client.api_call("chat.postMessage", channel=channel,
#                           text=response, as_user=True)
#
#
# def parse_slack_output(slack_rtm_output):
#     """
#         The Slack Real Time Messaging API is an events firehose.
#         this parsing function returns None unless a message is
#         directed at the Bot, based on its ID.
#     """
#     output_list = slack_rtm_output
#     if output_list and len(output_list) > 0:
#         for output in output_list:
#             if output and 'text' in output and AT_BOT in output['text']:
#                 # return text after the @ mention, whitespace removed
#                 return output['text'].split(AT_BOT)[1].strip().lower(), \
#                        output['channel']
#     return None, None
#
#
# if __name__ == "__main__":
#     READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
#     if slack_client.rtm_connect():
#         print("StarterBot connected and running!")
#         while True:
#             command, channel = parse_slack_output(slack_client.rtm_read())
#             if command and channel:
#                 handle_command(command, channel)
#             time.sleep(READ_WEBSOCKET_DELAY)
#     else:
#         print("Connection failed. Invalid Slack token or bot ID?")

from django.core.management.base import BaseCommand
from slackclient import SlackClient
import time
from slack_bot_app.models import Team


class Command(BaseCommand):
    help = 'Starts the bot for the first'

    def handle(self, *args, **options):
        team = Team.objects.first()
        client = SlackClient(team.bot_access_token)
        if client.rtm_connect():
            while True:
                events = client.rtm_read()
                print("%s----%s" % (team, events))
                for event in events:
                    if 'type' in event and event['type'] == 'message' and event['text'] == 'hi':
                        client.rtm_send_message(event['channel'], "hello world")
                time.sleep(1)