import logging


def log_init():
    """
    初始化log日志
    """
    log_format = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s')

    #log_file
    file_handler = logging.FileHandler('log.log', mode='w', encoding='utf-8')
    file_handler.setFormatter(log_format)

    #log_console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )