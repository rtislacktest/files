import matplotlib.pyplot as plt
from numpy import arange
import os
import datetime
import random
import math

PATH_TO_FILES = os.environ['PATH_TO_FILES']

def is_programm_is_ready():
    return 'Да' if random.randint(0,1) == 1 else 'Нет'

def draw_graph(func_text, x_from, x_to, x_step, graph_name, graph_dir=PATH_TO_FILES):
    try:
        os.mkdir(graph_dir)
    except:
        pass
    file_name = '{0}.png'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    res_file_name = f'{graph_dir}{file_name}'
    x = list(arange(x_from, x_to, x_step))
    y = [eval(func_text.replace('x', '__')) for __ in x]
    plt.figure(figsize=(9, 9))
    plt.plot(x, y)
    plt.title(graph_name)
    plt.xlabel('Значения x')
    plt.ylabel('Значения y')
    plt.grid()
    plt.savefig(res_file_name)
    return res_file_name