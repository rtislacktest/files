import requests
import os

URL_POST_MESSAGE = 'https://slack.com/api/chat.postMessage'
URL_CHAT_UPD_MSG = 'https://slack.com/api/chat.update'
URL_REACTION_ADD = 'https://slack.com/api/reactions.add'
URL_REACTION_DEL = 'https://slack.com/api/reactions.remove'
URL_FILE_UPLOAD  = 'https://slack.com/api/files.upload'

def post_to_slack(slack_token, url_to_post, **kwargs):
    data_info = {'token': slack_token}
    data_info.update(kwargs)
    return requests.post(url_to_post, data_info).json()

def upload_file_to_slack(slack_token, file_path_name, **kwargs):
    data_info = {'token': slack_token, "filename": os.path.basename(file_path_name)}
    data_info.update(kwargs)
    return requests.post(URL_FILE_UPLOAD,
                         params=data_info,
                         files={'file':(file_path_name, open(file_path_name, 'rb'))})