from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    if pressed:
        print(x,y)
    if not pressed:
        # Stop listener
        return False


with Listener(on_click=on_click) as listener:
    listener.join()