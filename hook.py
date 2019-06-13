from pynput import mouse
import pynput
from pynput.mouse import Listener
import threading
import pyautogui
import numpy as np
import tkinter as tk
from tkinter import simpledialog
import time
pressedList = []
root = tk.Tk()
def makelisten():
    def mousehook(x, y, button, pressed):
        if pressed:
            pressedList.append([x,y])
        if not pressed:
            return False
    with pynput.mouse.Listener(on_click=mousehook) as listener:
        listener.join()
def keyhook():
    def keyboardhook(key):
        pressedList.append(key)
        return False
    with pynput.keyboard.Listener(on_press=keyboardhook) as listener:
        listener.join()
def record():
    try:
        n = simpledialog.askfloat("Ввод", "Количество секунд", parent=root,minvalue=0)
    except: pass
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
        t1._stop()
        t2._stop()
        t3._stop()
        print('Запись остановлена')
    t3 = threading.Timer(n, killall)
    t3.start()
def repeat():
    try:
        n = simpledialog.askinteger("Ввод", "Количество повторений", parent=root,minvalue=0) if len(pressedList) != 0 else 0
    except:
        pass
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
def clear():
    try:
        del pressedList[:]
    except:
        print('Я не могу отчистить пустой список')
def read():
    global pressedList
    try:
        n = simpledialog.askstring(title='Конфигурации', prompt='Загрузить конфигрузацию')
        pressedList = np.load('presets/'+n+'.npy', allow_pickle=True).tolist()
    except: pass
def save():
    try:
        n = simpledialog.askstring(title='Конфигурации', prompt='Сохранить конфигрузацию')
        np.save('presets/'+n,np.array(pressedList))
    except: pass
display= lambda: print(pressedList)
tk.Button(text='Click', command = makelisten).pack()
tk.Button(text='Key', command = keyhook).pack()
tk.Button(text='Repeat', command = repeat).pack()
tk.Button(text='Clear', command= clear).pack()
tk.Button(text='Display', command= display).pack()
tk.Button(text='Read', command= read).pack()
tk.Button(text='Save', command= save).pack()
tk.Button(text='Record', command= record).pack()
root.mainloop()
