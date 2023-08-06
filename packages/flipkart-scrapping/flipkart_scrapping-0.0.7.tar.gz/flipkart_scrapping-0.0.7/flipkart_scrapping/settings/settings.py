from os.path import  sep, normpath
import sys
import os

root_dir = normpath(os.getcwd())
sys.path.append(root_dir + sep +  "mongo_operations")
sys.path.append(root_dir + sep +  "extract_details")
sys.path.append(root_dir + sep +  "modules")
sys.path.append(root_dir + sep +  "file_oper")
