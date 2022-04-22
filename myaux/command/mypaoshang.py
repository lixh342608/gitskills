#coding=utf-8

from .Base import *
import pyautogui
import os
pyautogui.PAUSE=1

class paoshang(myBase):
    def __init__(self,hwndkey):
        super(paoshang, self).__init__(hwndkey)