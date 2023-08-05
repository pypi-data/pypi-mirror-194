import logging


def does_not_contain_filter(reject_text: str, record: logging.LogRecord) -> bool:
    return reject_text not in record.msg
