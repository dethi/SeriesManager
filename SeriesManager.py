#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import os
import sys
import shutil
import getopt
import re


# Globals variables
#-----------------------------------------------------------------------------

_VERSION = "0.0.4"
_AUTHOR = "Deutsch Thibault"
_EMAIL = "thibault.deutsch@gmail.com"
_WEB = "http://www.thionnux.fr/"

_CWD_ORIGINE = os.getcwd()
#CFG = dict()

VERBOSE = False

# Classes
#-----------------------------------------------------------------------------

class colors:
    """Defined colors"""
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    NO = '\033[0m'
    
class disp:
    """Personnal print-like fonction."""
    
    def verbose(function):
        """Manages the verbose mode"""
        def verbose_verification(*args, **kwargs):
            global VERBOSE
            if VERBOSE:
                return function(*args, **kwargs)
        return verbose_verification
    
    def error(*args, **kwargs):
        """Print error."""
        print("|" + colors.RED + "|| ", end="")
        print(*args, **kwargs)
        print(colors.NO, end="")
        
    @verbose
    def good(*args, **kwargs):
        """Print validation."""
        print("|" + colors.GREEN + "---> ", end="")
        print(*args, **kwargs)
        print(colors.NO, end="")
        
    def info(*args, **kwargs):
        """Print info."""
        print("|", *args, **kwargs)
        
    def line():
        """Print a long line."""
        print("+" + "-" * 70 + "+")


# Functions
#-----------------------------------------------------------------------------

def main():
    """Start the script."""
    disp.line()
    file_pref = os.getcwd() + "/pref.ini"
    if not os.path.isfile(file_pref):
        first_start()
    get_opts()
    disp.line()
        
def first_start():
    """Create config file at first start."""
    pref = dict()
    with open("pref.ini", "w") as file:
        pref["naming"] = input("Naming : ")
        
        pref_str = str(pref).replace(", ", "\n").replace(": ", "=")
        pref_str = pref_str.replace("'", "")
        file.write(pref_str[1:len(pref_str)-1])
        
    syntax()
    

def get_opts():
    """Addresses the arguments passed to the command line."""
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vh", ["help"])
    except getopt.GetoptError as err:
        disp.error(err)
        disp.line()
        sys.exit(2)
    
    for o, a in opts:
        if o == "-v":
            global VERBOSE = True
        elif o in ("-h", "-help"):
            syntax()
                
    if len(args) == 1:
        if os.path.isdir(args[0]):
            auto_detect(args[0])
        else:
            disp.error("This is not a valid folder.", 
                "Please see the documentation.")
            syntax()
    else:
        disp.error("You have not specified folder.",
            "Please see the documentation.")
        syntax()

def syntax():
    disp.line()
    sys.exit(0)

def read_config():
    pass

def auto_detect(dir):
    """Analyzes the folder supplied as an argument."""
    disp.info("Starts detection...")
    
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
    
    detect_season(dir)

def detect_season(folder):
    """Detects seasons."""
    re_season = re.compile(r"(s|(s[aie]{2}sons?))[ .]?[0-9]+")
    re_movie_file = re.compile(r"[(.avi)(.mkv)(.flv)(.mp4)(.m4v)(.wmv)]$")
    
    if re_season.search(folder.lower()):
        disp.info("Folder season detected.")
        folder_list = list()
        folder_list.append(folder)
        disp.info("Renames folder season...")
        folder_list = rename_season(folder_list)
        detect_episode(folder_list[0])
    else:
        disp.info("Integral series detected.")
        os.chdir(folder)
        folder_list = os.listdir()
        other_file = list()
        for i,elt in enumerate(folder_list):
            if not os.path.isdir(elt):
                if re_movie_file.search(elt.lower()):
                    other_file.append(elt)
                else:
                    disp.info("Removes other files (like .nfo)...")
                    os.remove(elt)
                    disp.good("{}".format(elt))
                    del folder_list[i]
        disp.info("Renames folders seasons...")
        folder_list = rename_season(folder_list)
        disp.info("Starts detection of episodes...")
        for elf in folder_list:
            detect_episode(elf)

def detect_episode(season_folder):
    """Detects episodes."""
    disp.info("Process began in folder \"{}\"".format(season_folder))
    re_movie_file = re.compile(r"[(.avi)(.mkv)(.flv)(.mp4)(.m4v)(.wmv)]$")
    os.chdir(season_folder)
    file_list = os.listdir()
    episode_list = list()
    for i,elt in enumerate(file_list):
        if os.path.isdir(elt):
            disp.info("Episode is in separate folders.")
            os.chdir(elt)
            tmp_file_list = os.listdir()
            disp.info("Moving episodes in a single folder.")
            for file in tmp_file_list:
                if re_movie_file.search(file):
                    shutil.move(file, "..")
                    episode_list.append(file)
            os.chdir("..")
            disp.info("Delete the old folder.")
            shutil.rmtree(elt)
        else:
            if re_movie_file.search(elt.lower()):
                episode_list.append(elt)
            else:
                disp.info("Removes other files (like .nfo)...")
                disp.good("{}".format(elt))
                os.remove(elt)
    
    disp.info("Renames episodes...")
    rename_episode(episode_list)
    os.chdir("..")
           
def rename_season(folder_list):
    """Renames seasons."""
    new_folder_list = list()
    re_season = re.compile(r"(s|(s[aie]{2}sons?))[ .]?(?P<id>[0-9]{1,2})")
    for elt in folder_list:
        temp_name = elt
        result = re_season.search(elt.lower())
        elt = result.group("id")
        elt = int(elt)
        elt = "Saison {}".format(elt)
        new_folder_list.append(elt)
        disp.good("{} ==> {}".format(temp_name, elt))
        os.rename(temp_name, elt)
    return new_folder_list

def rename_episode(episode_list):
    """Renames episodes."""
    re_episode = re.compile(r"(e|(ep(isode)?))(?P<id>[0-9]{1,2})")
    new_name = list()
    for elt in episode_list:
        temp_name = elt
        result = re_episode.search(elt.lower())
        if result is not None:
            file_extention = elt.split(".")
            file_extention = "." + file_extention[len(file_extention)-1]
            elt = result.group("id")
            elt = int(elt)
            if elt < 10:
                elt = "0{}{}".format(elt, file_extention)
            else:
                elt = "{}{}".format(elt, file_extention)
            if not elt in new_name:
                os.rename(temp_name, elt)
                new_name.append(elt)
                disp.good("{} ==> {}".format(temp_name, elt))
            else:
                disp.error("Episode number \"{}\" already exists.".format(elt),
                    "Please rename the episode manually.")
                disp.error("-->> {}".format(temp_name))
        else:
            disp.error("Episode number undetected.", 
                "Please rename the episode manually.")
            disp.error("-->> " + str(os.getcwd() + "/" + elt))


if __name__ == "__main__":
    main()