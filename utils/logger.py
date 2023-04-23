import logging
import sys
import os
import datetime
import pathlib

# Logger
# ---------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

path_logs = pathlib.Path(__file__).parents[1] / 'logs'

if not os.path.exists(path_logs):
    os.makedirs(path_logs)

file_logs = '{0}\{1}_{2}.log'.format(path_logs, 'log', datetime.date.today().strftime('%Y_%m_%d'))
handler_file = logging.FileHandler(filename=file_logs, mode='a+', encoding='utf-8')
handler_file.setLevel(logging.DEBUG)
handler_file.setFormatter(logging.Formatter(fmt='%(asctime)s [%(filename)s %(lineno)4d] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(handler_file)

handler_stdout = logging.StreamHandler(sys.stdout)
handler_stdout.setLevel(logging.INFO)
handler_stdout.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%H:%M:%S'))
logger.addHandler(handler_stdout)
