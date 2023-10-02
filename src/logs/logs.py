import datetime

from src.config import Config


class Log:
    @staticmethod
    def _write_log(content: str, type: str):
        current_datetime = datetime.datetime.now()
        formatted_datetime: str = current_datetime.strftime('%d/%m/%Y %H:%M:%S')

        with open(Config.LOGS_FILE_PATH, 'a') as file:
            file.write(f"{type} - {formatted_datetime} - {content} \n")

    @classmethod
    def info(cls, content: str):
        cls._write_log(content, "INFO")

    @classmethod
    def error(cls, content: str):
        cls._write_log(content, "ERROR")
