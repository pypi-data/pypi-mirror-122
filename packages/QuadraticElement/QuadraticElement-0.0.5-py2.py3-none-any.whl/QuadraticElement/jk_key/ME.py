#coding:gbk

"""
OS:Windows 10 专业版
Python version:3.9.7
Time:2021/9/xx
author:PYmili
"""

import wget
import os
import os.path
import cv2
import numpy as np
from urllib import request
import keyboard # 键盘事件

from QuadraticElement import _library
from QuadraticElement import user_message as um
from QuadraticElement import new_user as new
from QuadraticElement import _open as op

from FolderProcessing import seefile as see
from FastDataTime import OStime as OS

# Poli
def run_Poli():
    from PyPoli import Poli

# 用户信息
def user_message():
    print("\n")
    um.USERNAME()
# wget—dow
def dow():
    try:
        url = input("URL>")
        file = input("FILE>")
        wget.download(url, out=f"{file}")
    except:
        print("error!")
# new user.txt
def new_user():
    try:
        print("\n生成user.txt文件")
        new.new_user()
        true = os.path.exists('user.txt')
        if true == True:
            print("\nuser.txt文件已存在！\n")
        else:
            print("\n生成成功！\n")
    except:
        print("\n生成失败！\n")
# open

#/*open_file*/
def open_files():
    file = input("EXE_path>")
    if os.path.exists(file) == True:  # 判断文件夹路径是否存在
        if os.path.isfile(file) == True:  # 判断文件路径是否存在
            op.open_file(f"{file}")
        elif os.path.exists(file) == False:
            print("There is no such file !")
    elif os.path.exists(file) == False:
        print("There is no such path !")
#/*open_url*/
def open_files():
    urls = input("URL>")
    op.open_url(urls)
# color
def _colors():
    color_ = input("color>")
    os.system(f"color {color_}")

# Find_folder>
def find_folder():
    path = input("PATH>") # 文件夹位置
    file = input("FILE_NAME>") # 文件夹名字
    com = input("Export folder>") # 是否输出文件夹
    if com == '':
        see.seefile(f'{path}', f'{file}')
    else:
        see.seefile(f'{path}', f'{file}', f'{com}')
# Suffix_lookup
def suffix():
    path = input("PATH>") # 路径
    Suffix = input("Suffix>") # 后缀名
    see.seeSuffix(f'{path}', f'{Suffix}')

# OSTime

def ostime():
    OS.OStime('jh')

