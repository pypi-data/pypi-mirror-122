import os
from config.logger import *

class __createFile:

    def __init__(self) -> None:
        self.fileCreated = False

    def create(self, file_name):
        if self.fileExits(file_name) and  self.fileCreated:
            return True
        
        file = open(file_name, "w")
        file.close()

        self.fileCreated = True


    def fileExits(self, file_name):
        return os.path.exists(file_name)


create_file = __createFile().create

#print(createFile().fileExits(""))
#print(createFile().create("/home/rajesh/imp/ineuron/ineuron-full-stack-data-science/flipkart_scrapping/scrapping/file_oper/create.py"))