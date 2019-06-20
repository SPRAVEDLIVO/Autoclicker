from pynput import mouse
import pynput
from pynput.mouse import Listener
import threading
import pyautogui
import pickle
import tkinter as tk
from tkinter import simpledialog
import time
pressedList = []
root = tk.Tk()
default = 'AutoClicker'
root.title(default)
root.geometry('240x220')
title = lambda tl: root.title(tl)
def makelisten():
    title('Listening')
    def mousehook(x, y, button, pressed):
        if pressed:
            pressedList.append([x,y])
        if not pressed:
            return False
    with pynput.mouse.Listener(on_click=mousehook) as listener:
        listener.join()
    title(default)
def keyhook():
    title('Listening')
    def keyboardhook(key):
        pressedList.append(key)
        return False
    with pynput.keyboard.Listener(on_press=keyboardhook) as listener:
        listener.join()
    title(default)
def record():
    title('Recording')
    n = simpledialog.askfloat("Ввод", "Количество секунд", parent=root,minvalue=0)
    if n is not None:
        tm = time.time()
        tmvectors = []
        def on_click(x, y, button, pressed):
            if time.time() - tm <= n:
                if pressed:
                    tmvectors.append(time.time() - tm)
                    try:
                        newvector = (tmvectors[-2] - tmvectors[-1]) * -1
                        pressedList.append(newvector)
                    except:
                        pass
                    pressedList.append([x,y])
            else:
                return False
        def on_press(key):
            if time.time() - tm <= n:
                tmvectors.append(time.time() - tm)
                try:
                    newvector = (tmvectors[-2] - tmvectors[-1]) * -1
                    pressedList.append(newvector)
                except:
                    pass
                pressedList.append(key)
            else:
                return False
        def start_keyboard():
            with pynput.keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        def start_mouse():
            with pynput.mouse.Listener(on_click=on_click) as listener:
                    listener.join()
        t1 = threading.Thread(target=start_mouse)
        t2 = threading.Thread(target=start_keyboard)
        t1.start()
        t2.start()
        def killall():
            try:
                t1._stop()
                t2._stop()
                t3._stop()
                print('Запись остановлена')
            except:
                print('Запись остановлена')
                title(default)
        t3 = threading.Timer(n, killall)
        t3.start()
    else: title(default)
def repeat():
    title('Repeating')
    n = simpledialog.askinteger("Ввод", "Количество повторений", parent=root,minvalue=0)
    if n is not None and len(pressedList) != 0:
        for j in range(n):
            ms = mouse.Controller()
            kb = pynput.keyboard.Controller()
            for i in range(len(pressedList)):
                if type(pressedList[i]) is list:
                    pyautogui.moveTo(pressedList[i])
                    ms.press(mouse.Button.left)
                    ms.release(mouse.Button.left)
                elif type(pressedList[i]) is float:
                    time.sleep(pressedList[i])
                else:
                    kb.press(pressedList[i])
                    kb.release(pressedList[i])
        title(default)
    else: title(default)
def clear():
    del pressedList[:]
    title(default)
def read():
    title('Reading')
    global pressedList
    try:
        n = simpledialog.askstring(title='Loader', prompt='Load configuration')
        with open ('presets/'+n+'.cfg', 'rb') as fp:
            pressedList = pickle.load(fp)
    except: pass
    title(default)
def save():
    title('Saving')
    try:
        n = simpledialog.askstring(title='Saver', prompt='Save configuration')
        with open('presets/'+n+'.cfg', 'wb') as fp:
            pickle.dump(pressedList, fp)
    except: pass
    title(default)
display= lambda: print(pressedList)
tk.Button(text='Click', command = makelisten, width = 10).pack()
tk.Button(text='Key', command = keyhook, width = 10).pack()
tk.Button(text='Repeat', command = repeat, width = 10).pack()
tk.Button(text='Clear', command= clear, width = 10).pack()
tk.Button(text='Display', command= display, width = 10).pack()
tk.Button(text='Read', command= read, width = 10).pack()
tk.Button(text='Save', command= save, width = 10).pack()
tk.Button(text='Record', command= record, width = 10).pack()
root.mainloop()
