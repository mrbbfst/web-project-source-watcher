#!/bin/python3
import argparse
import os
import shutil
from time import sleep
from datetime import datetime

argparser = argparse.ArgumentParser(
    prog="Angular deployer to Flask",
    description="Set the angular build folder and the flask project folder, and this script will be copied your sources to target folders."
)

argparser.add_argument(
    '--source', 
    type=str,
    help="Path to folder with a builded files, with slash on the end."
    )
argparser.add_argument(
    '--targetjs', 
    type=str,
    help="Path to target folder which contains JavaScript files, with slash on the end."
    )
argparser.add_argument(
    '--targethtml', 
    type=str,
    help="Path to target folder which contains HTML files, with slash on the end."
    )
argparser.add_argument(
    '--targetcss', 
    type=str,
    help="Path to target folder which contains CSS files, with slash on the end."
    )
argparser.add_argument(
    '--interval', 
    type=int,
    default=5,
    help="Check interval in seconds, default 5 sec.",
    )
argvs = argparser.parse_args()

def diff(path1,path2):
    for i in range(5):
        try:
            return os.path.getmtime(path1) > os.path.getmtime(path2)
        except FileNotFoundError:
            sleep(.5)
    
    return False

def copy(path1, path2):
    for i in range(5):
        try:
            shutil.copy2(path1, path2)
            break
        except FileNotFoundError:
            sleep(.5)

def main(source, js=None, html=None, css=None, interval=None):
    if source is None:
        print("Has no source folder.")
        return
    if js is None and html is None and css is None:
        print("Has no targets.")
        return
    for f in source,html,js,css:
        if f[-1:] != '/':
            print("The directory path must have a slash on the end.")
            return
    
    folders = [html,js,css]
    types = ['html' , 'js' , 'css']
    try:
        files = os.listdir(source)
    except FileNotFoundError as e:
        print(e)
        return

    os.system('clear')
    try:
        while True:
            for file in files:
                for folder,type in zip(folders,types):
                    if folder is None:
                        continue
                    if file[-len(type): ] == type:
                        if file in os.listdir(folder):
                            if diff(source+file, folder+file):
                                copy(source+file,folder+file)
                        else:
                            copy(source+file,folder+file)
            os.system('clear')
            print('checked at ', datetime.now())
            sleep(interval)
            os.system('clear')
            print('Work...')
    except KeyboardInterrupt:
        print("\b\bExit...")
        sleep(.1)
        os.system('clear')

if __name__=='__main__':
    main(
        argvs.source, 
        argvs.targetjs,
        argvs.targethtml,
        argvs.targetcss,
        argvs.interval
    )