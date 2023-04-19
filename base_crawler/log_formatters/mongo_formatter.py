import datetime as dt
import logging


class MongoFormatter(logging.Formatter):

    DEFAULT_PROPERTIES = logging.LogRecord(
        "", "", "", "", "", "", "", ""
    ).__dict__.keys()

    def format(self, record):
        """Formats LogRecord into python dictionary."""
        # Standard document
        document = {
            "timestamp": dt.datetime.utcnow(),
            "level": record.levelname,
            "thread": record.thread,
            "threadName": record.threadName,
            "message": record.getMessage(),
            "loggerName": record.name,
            "fileName": record.pathname,
            "module": record.module,
            "method": record.funcName,
            "lineNumber": record.lineno,
        }
        # Standard document decorated with exception info
        if record.exc_info is not None:
            document.update(
                {
                    "exception": {
                        "message": str(record.exc_info[1]),
                        "code": 0,
                        "stackTrace": self.formatException(record.exc_info),
                    }
                }
            )

        return document
