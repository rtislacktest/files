from slack import WebClient
import os

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

client = WebClient(token=SLACK_BOT_TOKEN)

r = client.conversations_list()
print(r["channels"])

channel_id = r["channels"][0]['id']
r = client.conversations_info(channel=channel_id)
print(r["channel"])

r = client.users_list()
print(r["members"])

r = client.conversations_members(channel=channel_id)
print(r["members"])

user_id = r["members"][0]
r = client.users_info(user=user_id)
print(r["user"])

r = client.emoji_list()
print(r["emoji"])