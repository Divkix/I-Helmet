import os
from datetime import datetime
import logging

# Define LOGGER as None, so value can be defined later
LOGGER = None

# Logging - Log all the information to log file with name as format - date_month_year-hour_minute.log
def start_logging():
    global LOGGER

    updir = ".."  # Take one dir up
    dt_string = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")  # Filename to save log

    # Make a logs folder if it does not exists
    if not os.path.exists(f"{updir}/logs"):
        os.mkdir(f"{updir}/logs")

    log_file = f"{updir}/logs/{dt_string}.log"  # logs folder in main directory
    logging.basicConfig(
        filename=log_file, level=logging.DEBUG
    )  # Save Log file to logs folder | Level: DEBUG
    LOGGER = logging.getLogger(__name__)


# Log as INFO, then print in console
def loginfo(text: str):
    print(text)
    LOGGER.info(text)


# Log as ERROR, then print in console
def logerr(text: str):
    print(text)
    LOGGER.error(text)