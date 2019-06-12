from pynput.keyboard import Key, Listener

def on_press(key):
    print('{0}'.format(key))
with Listener(
        on_press=on_press) as listener:
    listener.join()