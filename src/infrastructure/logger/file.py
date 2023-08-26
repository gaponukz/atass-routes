import time

class FileWriter:
    def __init__(self, filename: str):
        self._filename = filename

    def _publish_message(self, lvl: str, message: str):
        with open(self._filename, 'a', encoding='utf-8') as out:
            out.write(self._format_message(lvl, message) + "\n")

    def info(self, message: str):
        self._publish_message("INFO", message)

    def warn(self, message: str):
        self._publish_message("WARN", message)

    def error(self, message: str):
        self._publish_message("ERROR", message)

    def _format_message(self, level: str, message: str):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return f"{current_time} | {level} | {message}"
