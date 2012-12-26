#!/usr/bin/env python3
# -*-coding:Utf-8 -*
#
# Renames the series downloaded.
#
# Syntax:
# ./rseries.py [options] series_dir
#
# Options:
#     -v    Verbose mode
#     -h    Print syntax
#
#
# Copyright (C) 2012 Deutsch Thibault <thibault.deutsch@gmail.com>
#
# This file is part of SeriesManager.
#
# SeriesManager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# SeriesManager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__APPNAME__ = "SeriesManager"
__VERSION__ = "0.1.0"
__AUTHOR__ = "Deutsch Thibault <thibault.deutsch@gmail.com>"
__WEB__ = "http://www.thionnux.fr/"
__LICENCE__ = "GPL"


# Libraries
#-----------------------------------------------------------------------------

import os
import sys
import platform
import shutil
import getopt
import re


# Classes
#-----------------------------------------------------------------------------

class Colors:
    """Defined colors"""
    
    def __init__(self):
        """Constructor funtion."""
        if platform.system() != "Windows":
            self.red = '\033[91m'
            self.green = '\033[92m'
            self.no = '\033[0m'
        else:
            self.red = ''
            self.green = ''
            self.no = ''
    
class disp:
    """Personnal print-like fonction."""
    
    verbose = False
    colors = Colors()
    
    def verbose_mod(function):
        """Manages the verbose mode."""
        def verbose_verification(*args, **kwargs):
            if disp.verbose:
                return function(*args, **kwargs)
        return verbose_verification
    
    def error(*args, **kwargs):
        """Print error."""
        print("|" + disp.colors.red + "|| ", end="")
        print(*args, **kwargs)
        print(disp.colors.no, end="")
        
    @verbose_mod
    def good(*args, **kwargs):
        """Print validation."""
        print("|" + disp.colors.green + "---> ", end="")
        print(*args, **kwargs)
        print(disp.colors.no, end="")
        
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
    get_opts()
    disp.line()

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
            disp.verbose = True
        elif o in ("-h", "--help"):
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
    disp.info("Syntax:")
    disp.info("./rseries.py [options] series_dir")
    disp.info("")
    disp.info("Options:")
    disp.info("    -v    Verbose mode")
    disp.info("    -h    Print syntax")
    disp.line()
    sys.exit(0)
    
def auto_detect(dir):
    """Analyzes the folder supplied as an argument."""
    disp.info("Starts detection...")
    disp.info("What is the name of the series ? ", end="")
    name = str(input())
    
    if re.search(r"/{1}$", dir):
        dir = dir[:len(dir)-1]
        
    dir_cwd = os.path.dirname(dir)
    dir = os.path.basename(dir)
    os.chdir(dir_cwd)
    
    detect_season(dir, name)

def detect_season(folder, name):
    """Detects seasons."""
    re_season = re.compile(r"(s|(s[aie]{2}sons?))[ .]?[0-9]+")
    re_movie_file = re.compile(r"[(.avi)(.mkv)(.flv)(.mp4)(.m4v)(.wmv)]$")
    
    if re_season.search(folder.lower()):
        disp.info("Folder season detected.")
        folder_list = list()
        folder_list.append(folder)
        disp.info("Renames folder season...")
        folder_list = rename_season(folder_list, name)
        detect_episode(folder_list[0][0], folder_list[0][1], name)
    else:
        disp.info("Integral series detected.")
        disp.info("Renames folder series...")
        os.rename(folder, name)
        disp.good("{} ==> {}".format(folder, name))
        os.chdir(name)
        folder_list = os.listdir()
        other_file = list()
        for i,elt in enumerate(folder_list):
            if elt.startswith("."):
                os.remove(elt)
                del folder_list[i]
            elif not os.path.isdir(elt):
                if re_movie_file.search(elt.lower()):
                    other_file.append(elt)
                    del folder_list[i]
                else:
                    disp.info("Removes other files (like .nfo)...")
                    os.remove(elt)
                    disp.good("{}".format(elt))
                    del folder_list[i]
        if len(other_file) > 0:
            disp.info("Keep video files (like bonus)...")
            for elt in other_file:
                disp.good("{}".format(elt))
        disp.info("Renames folders seasons...")
        folder_list = rename_season(folder_list, name)
        
        disp.info("Starts detection of episodes...")
        for i in range(len(folder_list)):
            detect_episode(folder_list[i][0], folder_list[i][1], name)

def detect_episode(season_folder, season, name):
    """Detects episodes."""
    disp.info("Process began in folder \"{}\"".format(season_folder))
    re_movie_file = re.compile(r"[(.avi)(.mkv)(.flv)(.mp4)(.m4v)(.wmv)]$")
    os.chdir(season_folder)
    file_list = os.listdir()
    episode_list = list()
    for i,elt in enumerate(file_list):
        if elt.startswith("."):
            os.remove(elt)
            del file_list[i]
        elif os.path.isdir(elt):
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
    rename_episode(episode_list, season, name)
    os.chdir("..")
           
def rename_season(folder_list, name):
    """Renames seasons."""
    new_folder_list = list()
    season = list()
    re_season = re.compile(r"(s|(s[aie]{2}sons?))[ .]?(?P<id>[0-9]{1,2})")
    for elt in folder_list:
        temp_name = elt
        result = re_season.search(elt.lower())
        elt = result.group("id")
        elt = int(elt)
        if elt < 10:
            season_number = "0{}".format(elt)
            elt = "{} - S0{}".format(name, elt)
        else:
            season_number = str(elt)
            elt = "{} - S{}".format(name, elt)

        new_folder_list.append([elt, season_number])
        disp.good("{} ==> {}".format(temp_name, elt))
        os.rename(temp_name, elt)
    return new_folder_list

def rename_episode(episode_list, season, name):
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
                elt = "{} - S{}E0{}{}".format(name, season, elt,
                    file_extention)
            else:
                elt = "{} - S{}E{}{}".format(name, season, elt,
                    file_extention)
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
