# from slack_bot_app.models import Team
import psycopg2
from slackclient import SlackClient
from django.core.management.base import BaseCommand
import time
from django.db import models
# from slack_bot_app.models import Team, Message,Thread
from django.db import connection


BOT_ID = "U8CQ7DP53"
AT_BOT = "<@" + BOT_ID + ">"
slack_client = SlackClient("xoxb-284823465173-QKs8E9L0PQStyJLc3kTjRxQc")
connection = psycopg2.connect("dbname='slack_test' user='postgres' host='localhost' password='1'")

def handle_command(command, user, team):
    """
    send message to channel
    :param command:
    :param channel:
    :param user:
    :param team:
    :return:
    """
    results = []
    cursor = connection.cursor()
    cursor.execute('Select * FROM slack_bot_app_team WHERE '
                   'team_id = %s', [team])
    columns = ('id',
               'name',
               'team_id',
               'bot_id',
               'bot_token',
               'channel')

    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    channel = results[0]['channel']
    response = user + ": " + command
    slack_client.api_call("chat.postMessage", channel=channel, user=user,
                          text=response, as_user=True)


def direct_command(command, user, ts):
    """
    send direct message with answer
    :param command:
    :param user:
    :param ts:
    :return:
    """
    results = []
    cursor = connection.cursor()
    cursor.execute('Select * FROM slack_bot_app_message WHERE ts = %s', [ts])
    columns = ('id',
               'user_id',
               'user_name',
               'text',
               'team_id',
               'ts')
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    user_name = user
    api_call = slack_client.api_call("users.list")
    users = api_call.get('members')
    for us in users:
        if us.get('id') == user:
            user_name = us.get('real_name')
    slack_client.api_call(
        "chat.postMessage",
        channel=user,
        text=results[0]['text'] + ' //answer: ' + user_name + ": " + command,
        as_user=True
    )


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'team' in output:
                results = []
                cursor = connection.cursor()
                cursor.execute('Select * FROM slack_bot_app_team WHERE '
                               'team_id = %s', [output['team']])
                columns = ('id',
                           'name',
                           'team_id',
                           'bot_id',
                           'bot_token',
                           'channel')

                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                channel = results[0]['channel']

                if output and 'text' in output and AT_BOT in output['text'] and \
                                'user' in output and 'thread_ts' not in output:
                    thread = 0
                    api_call = slack_client.api_call("users.list")
                    users = api_call.get('members')
                    for user in users:
                        if user.get('id') == output['user']:
                            user_name = user.get('real_name')
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                           channel, user_name, thread, output['ts'], output['team']

                if output and 'text' in output and 'user' in output and 'thread_ts' in output:
                    thread = 1
                    api_call = slack_client.api_call("users.list")
                    users = api_call.get('members')
                    for user in users:
                        if user.get('id') == output['user']:
                            user_name = user.get('real_name')
                    results = []
                    cursor = connection.cursor()
                    cursor.execute('Select id, user_id FROM slack_bot_app_message WHERE '
                                   'ts = %s', [output['thread_ts']])
                    columns = ('i', 'u')
                    for row in cursor.fetchall():
                        results.append(dict(zip(columns, row)))

                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO slack_bot_app_thread (text, message_id) "
                                   "VALUES (%s, %s)",
                                   (output['text'], int(results[0]['i'])))
                    connection.commit()
                    return output['text'], \
                           output['channel'], results[0]['u'], thread, output['thread_ts'], output['team']

                if output and 'text' in output and output['user'] == BOT_ID and \
                                'event_ts' in output and 'thread_ts' not in output\
                        and output['channel'] == channel:
                    api_call = slack_client.api_call("users.list")
                    users = api_call.get('members')

                    text1 = output['text']
                    for_user = str(text1).find(":")
                    user_n = text1[:for_user]

                    for user in users:
                        if user.get('id') == output['user']:
                            user_name = user.get('real_name')
                        if user.get('real_name') == user_n:
                            user_id1 = user.get('id')
                            user_name1 = user.get('real_name')

                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO slack_bot_app_message (user_id, user_name, text, team_id, ts) "
                                   "VALUES (%s, %s, %s, %s, %s)",
                            (user_id1, user_name1, output['text'], 1, output['event_ts']))
                    connection.commit()

    return None, None, None, None, None, None


if __name__ == "__main__":
    slack_client = SlackClient("xoxb-284823465173-QKs8E9L0PQStyJLc3kTjRxQc")

    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user, thread, ts, team = parse_slack_output(slack_client.rtm_read())
            if command and channel and user and thread == 0:
                handle_command(command, user, team)
            if command and channel and user and thread == 1:
                direct_command(command, user, ts)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")