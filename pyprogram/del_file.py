#! python3
# coding=UTF-8
import os
import sys
del_dir = ["./all_dict","./data","./cut_over","./tf-idf","./keyword"]
Folder_name = str(sys.argv[1])
if len(os.listdir("./cut_over"))>30:
    for dir_1 in del_dir:
        file_dir = os.listdir(dir_1)
        for dir_2 in file_dir:
            if os.path.isdir(dir_1+'/'+dir_2):
                if Folder_name in dir_2:
                    continue
                file = os.listdir(dir_1+'/'+dir_2) 
            else:
                continue
            for f in file:
                os.remove(dir_1+'/'+dir_2+'/'+f)
        
            os.removedirs(dir_1+'/'+dir_2)
            #print("delet"+dir_1+'/'+dir_2)
    for dir_1 in del_dir:
        if not(os.path.isdir(dir_1)):
            os.mkdir(dir_1)
len(os.listdir("./cut_over"))
#2u/4