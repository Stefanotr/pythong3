import os
from datetime import datetime
import traceback


class Logger:
    LOG_DIR = "logs"
    ENABLED = True

    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    LOG_DIR = os.path.join(BASE_DIR, "logs")
    
    @staticmethod
    def error(function_name, exception):
        """
        Save errors in timestamped log file
        """
        # Create log folder if needed
        os.makedirs(Logger.LOG_DIR, exist_ok=True)

        # File name: log_YYYY-MM-DD.txt
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(Logger.LOG_DIR, f"log_{date_str}.txt")

        # log info
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = traceback.format_exc()

        log_entry = (
            f"\n{'='*60}\n"
            f"Date        : {timestamp}\n"
            f"Fonction    : {function_name}\n"
            f"Erreur      : {error_type}\n"
            f"Message     : {error_message}\n"
            f"Traceback   :\n{stack_trace}"
        )

        # writing in the file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(log_entry)
    
    @staticmethod
    def debug(function_name, message, **values):
        """
        Log de debug with key values
        """
        if not Logger.ENABLED:
            return

        os.makedirs(Logger.LOG_DIR, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(Logger.LOG_DIR, f"debug_{date_str}.txt")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        values_str = ", ".join(f"{k}={v}" for k, v in values.items())

        log_entry = (
            f"[{timestamp}] "
            f"{function_name} | "
            f"{message}"
        )

        if values_str:
            log_entry += f" | {values_str}"

        log_entry += "\n"

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(log_entry)


    