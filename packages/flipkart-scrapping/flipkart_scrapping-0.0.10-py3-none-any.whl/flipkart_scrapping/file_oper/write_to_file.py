from create_file import create_file
from config.logger import *
import json

class __writeToFile:

    def __init__(self) -> None:
        pass

    def write(self, file, data):
        log.info("Writing to File")
        status = create_file(file)
        file = open(file, "a+")
        file.write(json.dumps(data) +"\n")
        file.close()


writeToFile = __writeToFile().write
        