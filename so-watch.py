#!/bin/python3
import argparse
import os
import shutil
from time import sleep
from datetime import datetime

argparser = argparse.ArgumentParser(
    prog="Web Project Source Watcher",
    description="Set the front-end build folder and the back-end target folder, and this script will be copied your sources to target folders."
)

argparser.add_argument(
    '-s','--source', 
    type=str,
    help="Path to folder with a builded files, with slash on the end."
    )
argparser.add_argument(
    '-tm','--targetmono', 
    type=str,
    help="Path to target folder which contains all files, with slash on the end."
    )
argparser.add_argument(
    '-tjs','--targetjs', 
    type=str,
    help="Path to target folder which contains JavaScript files, with slash on the end."
    )
argparser.add_argument(
    '-th','--targethtml', 
    type=str,
    help="Path to target folder which contains HTML files, with slash on the end."
    )
argparser.add_argument(
    '-tc','--targetcss', 
    type=str,
    help="Path to target folder which contains CSS files, with slash on the end."
    )
argparser.add_argument(
    '-i','--interval', 
    type=int,
    default=5,
    help="Check interval in seconds, default 5 sec.",
    )
argparser.add_argument(
    '-cd','--cleardir', 
    type=str,
    default='not',  # first - clear wirh start, always - clear each time
    help="delete old source files. not - no delete, first - delete only with starting, always - delete each time",
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

def getlfiles_or_none(path):
    er = None
    for i in range(5):
        try:
            er = None
            return os.listdir(path)
        except FileNotFoundError as e:
            er = e
            sleep(4)
    if(er):
        print(er)
        
    return None

def path_adjust(path:str) -> str:
    if path == '.':
        return path_adjust(os.getcwd())
    elif path[:2] == './':
        return path_adjust(os.getcwd()+path[1:])
    elif path[-1:] != '/':
        return path+'/'


def main(source, mono=None, js=None, html=None, css=None, interval=None):
    if source is None:
        print("Has no source folder.")
        return
    
    folders = tuple()
    oldfiles = set()
    
    if not mono:
        if js is None and html is None and css is None:
            print("Has no targets.")
            return
        folders = (
            path_adjust(html) ,
            path_adjust(js),
            path_adjust(css)
            )
    else:
        folders=(
            path_adjust(mono),
            path_adjust(mono),
            path_adjust(mono)
            )
        
    types = ['html' , 'js' , 'css']
    

    os.system('clear')
    try:
        while True:
            files = getlfiles_or_none(source)
            for file in files:
                for folder,type in zip(folders,types):
                    if folder is None:
                        continue
                    if file[-len(type): ] == type:
                        try:
                            if file in os.listdir(folder):
                                if diff(source+file, folder+file):
                                    copy(source+file,folder+file)
                            else:
                                copy(source+file,folder+file)
                            oldfiles.add(file)
                        except FileNotFoundError as e:
                            print("I can't continue working.")
                            print(e)
                            return
            os.system('clear')
            print('checked at ', datetime.now())
            sleep(interval)
            os.system('clear')
            print('Work...')
    except TypeError:
        print("Source directory is not exist.")
    except KeyboardInterrupt:
        print("\b\bExit...")
        sleep(.1)
        os.system('clear')

if __name__=='__main__':
    main(
        argvs.source,
        argvs.targetmono, 
        argvs.targetjs,
        argvs.targethtml,
        argvs.targetcss,
        argvs.interval
    )