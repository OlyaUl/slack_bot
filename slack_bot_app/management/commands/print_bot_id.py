import os
from slackclient import SlackClient
from django.conf import settings


# BOT_NAME = 'workbot'
BOT_NAME = 'new'
slack_client = SlackClient("xoxb-284823465173-QKs8E9L0PQStyJLc3kTjRxQc") #"xoxb-283146722036-v8pYN2wwFJ005hmqhiQo7SM0")
# SlackClient(os.environ.get('SLACK_BOT_TOKEN')) # SlackClient(settings.SLACK_BOT_TOKEN)


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)

# Bot ID for 'workbot' is U8B4AM812

