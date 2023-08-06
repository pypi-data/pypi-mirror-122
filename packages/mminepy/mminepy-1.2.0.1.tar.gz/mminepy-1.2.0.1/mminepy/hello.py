import os
import sys
import getpass
def gegus():
    print("loading")
    try:
        g = sys.version
        h = g.split(".")
        m = str(h[0])+str(h[1])
        path_dir = "C:/Users/"+getpass.getuser()+"/AppData/Local/Programs/Python"
        os.chdir("C:/Users/"+getpass.getuser()+"/AppData/Local/Programs/Python")
        file_list = os.listdir(path_dir)
        for i in file_list:
            if os.path.isdir(i+"/Lib/site-packages/mminepy"):
                program_list = os.listdir(i+"/Lib/site-packages")
                print(i+"/Lib/site-packages/"+f+"/mminepy.exe")
                for f in program_list:
                    if os.path.isfile(i+"/Lib/site-packages/"+f+"/mminepy.exe"):
                        os.chdir(i+"/Lib/site-packages/"+f)
                        os.system("move minepy.exe ..")
                        os.chdir("..")
                        os.system("move minepy.exe ..")
                        os.chdir("..")
                        os.system("move minepy.exe ..")
                        os.chdir("..")
    catch:
        print("fail")
    # setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python37/Lib/site-packages/mminepy-1.1.1.17.dist-info;