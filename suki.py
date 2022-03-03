#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import PIL
import pyautogui
import win32gui
import win32com.client
import pyautogui
import win32api
import win32con
import time
from tkinter import *
import threading
import pythoncom


# In[2]:


list_ing = np.array( [['chocolate', 'matcha', 'strawberry'], ['milk','coconut','soy'], ['2','5','7'], ['blueberry','olive','banana'],['honey','almon','chocolatechips'], ['pudding','bread','pie'] ])
list_ing_get = np.full([6], None)
rows = list_ing.shape[0]
cols = list_ing.shape[1]
program = ''
savePath = ''
saveFormat = ''
screenshootPath = 'D:/AI/BlueStacks 62.png'
running = True  # Global flag


# In[3]:


def screenshot(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            im.save(screenshootPath)
        else:
            print('Window not found!')
    else:
        im = pyautogui.screenshot()
        im.save(screenshootPath)


# In[4]:


def click(x, y):
    hWnd = win32gui.FindWindow(None, program)
    lParam = win32api.MAKELONG(x, y)

    hWnd1= win32gui.FindWindowEx(hWnd, None, None, None)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hWnd1, win32con.WM_LBUTTONUP, None, lParam)


# In[ ]:





# In[5]:


def getListIng(test):
    ing = 0
    for x in range(0, rows):
        for y in range(0, cols):
            img = cv2.imread('D:/AI/SM/' + list_ing[x,y] + '.png' , cv2.IMREAD_COLOR)
            result = cv2.matchTemplate(test ,img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.82:
                list_ing_get[x] = list_ing[x,y]


# In[6]:


def start(test):
    start_img = cv2.imread('D:/AI/start.png' , cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(test ,start_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if (max_val > 0.8):
        getListIng(test)
        click(max_loc[0] + 5, max_loc[1]+5)
    else:
        time.sleep(0.5)
        screenshot(program)
        test = cv2.imread(screenshootPath , cv2.IMREAD_COLOR)
        start(test)


# In[7]:


def getListIngAndStart():
    time.sleep(1.5)
    list_ing_get = np.full([6], None)
    test = cv2.imread(screenshootPath , cv2.IMREAD_COLOR)
    start(test)
    time.sleep(1.5)


# In[8]:


def next(test):
    time.sleep(0.15)
    nextIng = cv2.imread('D:/AI/next.png' , cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(test ,nextIng, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if (max_val < 0.8):
        nextIng = cv2.imread('D:/AI/finish.png' , cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(test ,nextIng, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    click(max_loc[0] + 10 , max_loc[1] + 20)


# In[9]:


def choseIng():
    for x in range(0, 6):
        if list_ing_get[x] is None:
            break
        screenshot(program)
        test = cv2.imread(screenshootPath , cv2.IMREAD_COLOR)
        img = cv2.imread('D:/AI/LG/' + list_ing_get[x] + '.png' , cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(test ,img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        time.sleep(0.2)
        click(max_loc[0] + 20, max_loc[1]+20)
        next(test)
        time.sleep(1.0)


# In[10]:


def sukiStillGoing():
    time.sleep(0.25)
    screenshot(program)
    test = cv2.imread(screenshootPath , cv2.IMREAD_COLOR)
    img = cv2.imread('D:/AI/endsuki.png' , cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(test ,img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if (max_val > 0.8):
        return False
    return True


# In[11]:


def nextSuki():
    time.sleep(0.4)
    click(100,100)
    time.sleep(3.25)
    screenshot(program)
    test = cv2.imread(screenshootPath , cv2.IMREAD_COLOR)
    img = cv2.imread('D:/AI/nextsuki.png' , cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(test ,img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    click(max_loc[0] + 10, max_loc[1]+10)
    time.sleep(1)


# In[12]:


def resize(programName):
    import pygetwindow
    win = pygetwindow.getWindowsWithTitle(programName)[0]
    win.size = (434, 802)


# In[13]:


def main(programName):
    resize(programName)
    global program, savePath, saveFormat, screenshootPath
    program = programName
    savePath = 'D:/AI/'
    saveFormat = ".png"
    screenshootPath = savePath+program+saveFormat
    while(sukiStillGoing() and running == True):
        getListIngAndStart()
        choseIng()
        for x in range(0,6):
            list_ing_get[x] = None
        nextSuki()


# In[ ]:





# In[ ]:


master = Tk()
master.geometry('200x100')
e = Entry(master)
e.pack()
e.focus_set()

def callback():
    main(e.get())

    
b = Button(master, text = "OK", width = 10, command = callback)
b.pack()
master.mainloop()



