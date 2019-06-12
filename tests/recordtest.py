import pynput
import threading
import time
tm = time.time()
times = []
pressedList = []
n = 4
tmvectors = []
tm = time.time()
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
			print(pressedList)
	else:
		return False
def on_press(key):
	if time.time() - tm <= n:
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
threading.Timer(n, killall).start()