#########PTB+ API#########
###########V 1.0##########
##Follow the MIT license##

import json
import os
import time
from subprocess import Popen
import easygui as g

def openApp(App):
    try:
        Popen("python.exe " + App)
    except Exception as e:
        error = repr(e)
        log(error)


def command(command):
    try:
        Popen(command)

    except Exception as e:
        error = repr(e)
        log(error)


def log(text):
    with open("../log.txt", "a") as l:
        ti = time.asctime(time.localtime(time.time()))
        ti = "\n" + ti + "\n"
        info = ti + text + "\n"
        l.write(info)

def proFile(filedir, mode, content):
    if mode == "w" or mode == "wb" or mode == "a":
        with open(filedir, mode) as w:
            w.write(content)
    elif mode == "r":
        with open(filedir, mode)as r:
            cont = r.read()
            return cont


def proJSON(filedir, mode, content=None):
    if mode == "w" or mode == "wb" or mode == "a":
        with open(filedir, mode) as wj:
            json.dump(content, wj)
    elif mode == "r":
        with open(filedir, mode) as rj:
            cont = json.load(rj)
            return cont


def judgeEXT(fileDir):
    ext = os.path.splitext(fileDir)[-1]
    return ext


def musicPlay(com, musicFile = None):
    import pygame
    if com == "play":
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(1, 0)
    elif com == "stop":
        pygame.mixer.music.stop()
    elif com == "pause":
        pygame.mixer.music.pause()
    elif com == "unpause":
        pygame.mixer.music.unpause()
    elif com == "stop":
        pygame.mixer.music.stop()


def imgShow(image):
    from matplotlib import pyplot
    from PIL import Image
    img = Image.open(image)
    pyplot.imshow(img)
    pyplot.show()


def download(url, filedir, headers):
    import requests
    bt = requests.get(url, headers=headers)
    print("开始下载")
    proFile(filedir=filedir, mode="wb", content=bt)
    print("下载完成")


def openDir(mode):
    if mode == "dir":
        input_dir = g.diropenbox()
        return input_dir
    elif mode == "file":
        select_file = g.fileopenbox()
        return select_file
