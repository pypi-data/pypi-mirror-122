import logging
from datetime import datetime


#ts = datetime.now().strftime("%Y%m%d_%I%M%S%s")[:-3]
ts="1"
file_name = "log_" + ts + ".txt"
formatter = logging.Formatter("%(levelname)s %(asctime)s %(filename)s %(message)s")

file_logger = logging.FileHandler(file_name, mode="w")
file_logger.setFormatter(formatter)

stream_logger = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
stream_logger.setFormatter(formatter)

log = logging.getLogger(' ')
log.setLevel(logging.DEBUG)
log.addHandler(file_logger)
log.addHandler(stream_logger)
#log.setLevel(logging.debug)


#logging.basicConfig(filename="log.txt", filemode="w", format = "%(asctime)s:%(levelno)s:%(filename)s:%(message)s")