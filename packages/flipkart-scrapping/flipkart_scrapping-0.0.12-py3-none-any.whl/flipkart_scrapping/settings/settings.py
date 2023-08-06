from os.path import  sep
import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

#print(normpath(os.path.realpath(__file__)))
sys.path.append(root_dir + sep +  "mongo_operations")
sys.path.append(root_dir + sep +  "extract_details")
sys.path.append(root_dir + sep +  "modules")
sys.path.append(root_dir + sep +  "file_oper")
sys.path.append(root_dir + sep +  "config")
