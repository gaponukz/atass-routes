import time

class ConsoleLogger:
    def _publish_message(self, lvl: str, message: str):
        print(self._format_message(lvl, message))

    def info(self, message: str):
        self._publish_message("INFO", message)

    def warn(self, message: str):
        self._publish_message("WARN", message)

    def error(self, message: str):
        self._publish_message("ERROR", message)

    def _format_message(self, level: str, message: str):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return f"{current_time} | {level} | {message}"
