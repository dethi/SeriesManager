#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import os
import sys
import shutil
import getopt
import re

# Globals variables
#-----------------------------------------------------------------------------

_VERSION = "0.1.0"
_AUTHOR = "Deutsch Thibault"
_EMAIL = "thibault.deutsch@gmail.com"
_WEB = "http://www.thionnux.fr/"

_CWD_ORIGINE = os.getcwd()
#CFG = dict()

# Functions
#-----------------------------------------------------------------------------

def main():
    file_pref = os.getcwd() + "/pref.cfg"
    if not os.path.isfile(file_pref):
        first_start()
    get_opts()
        
def first_start():
    pref = dict()
    with open("pref.cfg", "w") as file:
        pref["naming"] = input("Naming : ")
        
        pref_str = str(pref).replace(", ", "\n").replace(": ", "=")
        pref_str = pref_str.replace("'", "")
        file.write(pref_str[1:len(pref_str)-1])

def get_opts():
    cfg = read_config()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vha:", ["help", "add="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    for o, a in opts:
        if o == "-v":
            #global VERBOSE
            #VERBOSE = True
            pass
        elif o in ("-h", "-help"):
            usage()
        elif o in ("-a", "--add"):
            if os.path.isdir(a):
                auto_detect(a, cfg)
            else:
                print("This is not a valid folder. ", end="")
                print("Please see the documentation.")
                usage()
        else:
            print("Option {} inconnue".format(o))
            sys.exit(2)

def usage():
    pass

def read_config():
    pass

def auto_detect(dir, cfg):
    dir.replace("\\", "/")
    if re.search(r"/{1}$", dir):
        dir = dir[:len(dir)-1]
    
    if dir.startswith("/"):
        dir_cwd = dir.split("/")
        dir = dir_cwd[len(dir_cwd)-1]
        dir_cwd = dir_cwd[1:len(dir_cwd)-1]
        dir_cwd = "/" + "/".join(dir_cwd) + "/"
        os.chdir(dir_cwd)
    elif len(dir.split("/")) >= 2:
        dir_cwd = dir.split("/")
        dir = dir_cwd[len(dir_cwd)-1]
        dir_cwd = dir_cwd[:len(dir_cwd)-1]
        dir_cwd = "/".join(dir_cwd) + "/"
        os.chdir(dir_cwd)
    
    re_season = re.compile(r"(s|(s[aie]{2}sons?))[ .-]?[0-9]+")
    if re_season.search(dir.lower()):
        detect_episode(dir)
    else:
        detect_season(dir)

def detect_season(integral_folder):
    re_movie_file = re.compile(r"[(.avi)(.mkv)(.flv)(.mp4)(.m4v)(.wmv)]$")
    os.chdir(integral_folder)
    folder_list = os.listdir()
    other_file = list()
    for i,elt in enumerate(folder_list):
        if not os.path.isdir(elt):
            if re_movie_file.search(elt.lower()):
                other_file.append(elt)
            else:
                del folder_list[i]
    folder_list = rename_season(folder_list)
    for elf in folder_list:
        detect_episode(elf)

def detect_episode(season_folder):
    re_movie_file = re.compile(r"[(.avi)(.mkv)(.flv)(.mp4)(.m4v)(.wmv)]$")
    os.chdir(season_folder)
    file_list = os.listdir()
    episode_list = list()
    for i,elt in enumerate(file_list):
        if os.path.isdir(elt):
            os.chdir(elt)
            tmp_file_list = os.listdir()
            for file in tmp_file_list:
                if re_movie_file.search(file):
                    shutil.move(file, "..")
                    episode_list.append(file)
            os.chdir("..")
            shutil.rmtree(elt)
        else:
            if re_movie_file.search(elt.lower()):
                episode_list.append(elt)
            else:
                os.remove(elt)
    rename_episode(episode_list)
    os.chdir("..")
           
def rename_season(folder_list):
    new_folder_list = list()
    re_season = re.compile(r"(s|(s[aie]{2}sons?))[ .-]?(?P<id>[0-9]+)")
    for elt in folder_list:
        temp_name = elt
        result = re_season.search(elt.lower())
        elt = result.group("id")
        elt = "Season " + elt
        new_folder_list.append(elt)
        os.rename(temp_name, elt)
    return new_folder_list

def rename_episode(episode_list):
    re_episode = re.compile(r"(e|(episode)|(epi)|(ep))[ .-]?(?P<id>[0-9]+)")
    for elt in episode_list:
        temp_name = elt
        result = re_episode.search(elt.lower())
        if result is not None:
            file_extention = elt.split(".")
            file_extention = "." + file_extention[len(file_extention)-1]
            elt = result.group("id")
            elt = elt + file_extention
            os.rename(temp_name, elt)
        else:
            print("Episode number undetected. ", end="")
            print("Please rename the episode manually.")
            print(str(os.getcwd() + "/" + elt))

if __name__ == "__main__":
    main()