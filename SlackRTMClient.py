from slack import RTMClient
import re
import os
import SlackPostRequests as slack_api
import SomeBackend as backend_api

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
PATH_TO_FILES   = os.environ['PATH_TO_FILES']

PATTERN_IS_PROGRAM_READY = 'программа готова?'
PATTERN_DRAW_GRAPH       = r'^бот, нарисуй график ([^;]+)$'
PATTERN_GRAPH_FROM_TO    = r'^бот, нарисуй график ([^;]+); x от ([^ ]+) до ([^ ]+) шаг ([^ ]+)$'
PATTERN_BOT              = '^бот'

def answer_is_program_ready(payload_data):
    slack_api.post_to_slack(SLACK_BOT_TOKEN,
                            slack_api.URL_POST_MESSAGE,
                            channel   = payload_data["channel"],
                            thread_ts = payload_data['ts'],
                            text      = backend_api.is_programm_is_ready())

def answer_draw_graph(payload_data, graph_func, x_from=-100.0, x_to=100.0, x_step=0.1):
    slack_api.post_to_slack(SLACK_BOT_TOKEN,
                            slack_api.URL_POST_MESSAGE,
                            channel   = payload_data["channel"],
                            thread_ts = payload_data["ts"],
                            text      = f'Кто просил нарисовать график y={graph_func}? Пожа-а-алуйста!')
    slack_api.post_to_slack(SLACK_BOT_TOKEN,
                            slack_api.URL_REACTION_ADD,
                            channel   = payload_data["channel"],
                            timestamp = payload_data["ts"],
                            name      = 'sonic')
    try:
        file_name = backend_api.draw_graph(graph_func, x_from, x_to, x_step,
                                           'График, который построил наш бот',
                                           PATH_TO_FILES)
        slack_api.upload_file_to_slack(SLACK_BOT_TOKEN,
                                       file_name,
                                       channels  = [payload_data["channel"]],
                                       thread_ts = payload_data["ts"])
        slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                slack_api.URL_REACTION_ADD,
                                channel   = payload_data["channel"],
                                timestamp = payload_data["ts"],
                                name      = 'heavy_check_mark')
    except Exception as e:
        slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                slack_api.URL_REACTION_ADD,
                                channel   = payload_data["channel"],
                                timestamp = payload_data["ts"],
                                name      = 'x')
        slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                slack_api.URL_POST_MESSAGE,
                                channel   = payload_data["channel"],
                                thread_ts = payload_data["ts"],
                                text      = f'Произошла ошибка {e}!')
    finally:
        slack_api.post_to_slack(SLACK_BOT_TOKEN,
                                slack_api.URL_REACTION_DEL,
                                channel   = payload_data["channel"],
                                timestamp = payload_data["ts"],
                                name      = 'sonic')

def answer_bot(payload_data):
    if 'user' in payload_data:
        data_user    = '<@'+payload_data['user']+'>'
    else:
        data_user    = ''
    slack_api.post_to_slack(SLACK_BOT_TOKEN,
                            slack_api.URL_POST_MESSAGE,
                            channel   = payload_data["channel"],
                            thread_ts = payload_data["ts"],
                            text      = 'Добрый день, {0}!\n Вы написали ```{1}``` Но я Вас не понял :white_frowning_face:'.format(
                                                data_user, payload_data["text"]))

@RTMClient.run_on(event='message')
def check_for_messages(**payload):
    payload_data = payload['data']
    print(payload_data)
    message_text = re.sub('^reminder: ', '', payload_data['text'].lower())
    try:
        if re.match(PATTERN_IS_PROGRAM_READY, message_text):
            answer_is_program_ready(payload_data)

        elif re.match(PATTERN_DRAW_GRAPH, message_text):
            graph_func = re.sub(PATTERN_DRAW_GRAPH, r'\1', message_text)
            answer_draw_graph(payload_data, graph_func)

        elif re.match(PATTERN_GRAPH_FROM_TO, message_text):
            graph_func = re.sub(PATTERN_GRAPH_FROM_TO, r'\1', message_text)
            x_from = float(re.sub(PATTERN_GRAPH_FROM_TO, r'\2', message_text))
            x_to   = float(re.sub(PATTERN_GRAPH_FROM_TO, r'\3', message_text))
            x_step = float(re.sub(PATTERN_GRAPH_FROM_TO, r'\4', message_text))
            answer_draw_graph(payload_data, graph_func, x_from, x_to, x_step)

        elif re.match(PATTERN_BOT, message_text):
            answer_bot(payload_data)

    except Exception as e:
        print(e)

def start_rtm_client():
    rtmclient = RTMClient(token=SLACK_BOT_TOKEN, connect_method='rtm.start')
    rtmclient.start()

if __name__ == '__main__':
    start_rtm_client()