#coding:gbk

"""
OS:Windows 10 רҵ��
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
import keyboard # �����¼�

from QuadraticElement import _library
from QuadraticElement import user_message as um
from QuadraticElement import new_user as new
from QuadraticElement import _open as op

from FolderProcessing import seefile as see
from FastDataTime import OStime as OS

# Poli
def run_Poli():
    from PyPoli import Poli

# �û���Ϣ
def user_message():
    print("\n")
    um.USERNAME()
# wget��dow
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
        print("\n����user.txt�ļ�")
        new.new_user()
        true = os.path.exists('user.txt')
        if true == True:
            print("\nuser.txt�ļ��Ѵ��ڣ�\n")
        else:
            print("\n���ɳɹ���\n")
    except:
        print("\n����ʧ�ܣ�\n")
# open

#/*open_file*/
def open_files():
    file = input("EXE_path>")
    if os.path.exists(file) == True:  # �ж��ļ���·���Ƿ����
        if os.path.isfile(file) == True:  # �ж��ļ�·���Ƿ����
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
    path = input("PATH>") # �ļ���λ��
    file = input("FILE_NAME>") # �ļ�������
    com = input("Export folder>") # �Ƿ�����ļ���
    if com == '':
        see.seefile(f'{path}', f'{file}')
    else:
        see.seefile(f'{path}', f'{file}', f'{com}')
# Suffix_lookup
def suffix():
    path = input("PATH>") # ·��
    Suffix = input("Suffix>") # ��׺��
    see.seeSuffix(f'{path}', f'{Suffix}')

# OSTime

def ostime():
    OS.OStime('jh')

