import logging

from TaoBao import conf
from tools import log

if conf.debug:
    log.init()
    # log.add_log_handler(logging.FileHandler(conf.log_path))
