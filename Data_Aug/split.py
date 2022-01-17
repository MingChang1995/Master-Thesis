import os
import shutil

path_xml = "./train/"
filelist = os.listdir(path_xml)
path1 = "./train/"
path2 = "./img/"
path3 = "./xml/"


for files in filelist:
    filename1 = os.path.splitext(files)[1]  
    filename0 = os.path.splitext(files)[0]  
    # print(filename1)
    m = filename1 == '.png'
    # print(m)
    if m :
        full_path = os.path.join(path1, files)
        despath = path2 + filename0+'.png' 
        shutil.move(full_path, despath)

    else :
        full_path = os.path.join(path1, files)
        despath = path3 + filename0 + '.xml'  
        shutil.move(full_path, despath)
