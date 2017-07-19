import sys

import logging

# 日志模版
log_template = '%(asctime)s %(levelname)s [%(name)s]: %(message)s'
log_formatter = logging.Formatter(log_template)
# 异常信息模版
traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''
logger = logging.getLogger()


def init():
    # 配置日志
    logger.setLevel(logging.DEBUG)
    default_logger = logging.StreamHandler()
    default_logger.setFormatter(log_formatter)
    logger.addHandler(default_logger)


def traceback_detail():
    """
    异常详情
    :return:
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    '''
    Reason this _can_ be bad: If an (unhandled) exception happens AFTER this,
    or if we do not delete the labels on (not much) older versions of Py, the
    reference we created can linger.
    traceback.format_exc/print_exc do this very thing, BUT note this creates a
    temp scope within the function.
    '''
    traceback_details = {
        'filename': exc_traceback.tb_frame.f_code.co_filename,
        'lineno': exc_traceback.tb_lineno,
        'name': exc_traceback.tb_frame.f_code.co_name,
        'type': exc_type.__name__,
        'message': str(exc_value),  # or see traceback._some_str()
    }

    del (exc_type, exc_value, exc_traceback)  # So we don't leave our local labels/objects dangling
    # This still isn't "completely safe", though!
    # "Best (recommended) practice: replace all exc_type, exc_value, exc_traceback
    # with sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    return traceback_template % traceback_details


def add_log_handler(handler):
    handler.setFormatter(log_formatter)
    logger.addHandler(handler)


def d(target=None):
    """
    调试日志
    :param target: 日志内容
    :return:
    """
    if target is None:
        target = traceback_detail()
    logger.debug(target)


def e(target=None):
    """
    调试日志
    :param target: 日志内容
    :return:
    """
    if target is None:
        target = traceback_detail()
    logger.error(target)
