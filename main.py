import os
import SlackPostRequests as slack_api

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
PATH_TO_FILES = os.environ['PATH_TO_FILES']
START_CHANNEL = os.environ['START_CHANNEL']

if __name__ == '__main__':
    #Тест отправки сообщения
    r_msg = slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                    slack_api.URL_POST_MESSAGE,
                                    channel = START_CHANNEL,
                                    text    = 'slack bot test')
    print(f'r_msg: {r_msg}')
    # Тест редактирования сообщения
    r_upd = slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                    slack_api.URL_CHAT_UPD_MSG,
                                    channel = r_msg["channel"],
                                    ts      = r_msg["ts"],
                                    text    = 'Слак бот тест')
    print(f'r_upd: {r_upd}')
    # Тест добавления эмоций в сообщения
    r_radd = slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                     slack_api.URL_REACTION_ADD,
                                     channel   = r_msg["channel"],
                                     timestamp = r_msg["ts"],
                                     name      = 'grin')
    print(f'r_rad: {r_radd}')
    # Тест удаления эмоций в сообщения
    r_rdel = slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                     slack_api.URL_REACTION_DEL,
                                     channel   = r_msg["channel"],
                                     timestamp = r_msg["ts"],
                                     name      = 'grin')
    print(f'r_rad: {r_rdel}')
    # Тест загрузки файла в сообщения
    r_file = slack_api.upload_file_to_slack(SLACK_BOT_TOKEN,
                                            r'{0}TEST.png'.format(PATH_TO_FILES),
                                            channels  = [r_msg["channel"]])
    print(f'r_file: {r_file}')

