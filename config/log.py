import logging

def log_init():
    """
    初始化log日志
    """
    logging.basicConfig(
        level=logging.INFO,
        filename='log.log',
        filemode='w',
        format='%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s',
        encoding='utf-8'
    )