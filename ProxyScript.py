from pynput import keyboard, mouse
import time
import datetime
import concurrent.futures
import psutil


# Инициализация
def GetCurTime():
    return datetime.datetime.now()

INACTION_MAX_TIME = 5 * 60
last_action = GetCurTime()
is_proxy_enable = False

# Слушатели
def on_key(key):
    UpdateLastAction()

def on_move(x, y):
    UpdateLastAction()

def on_click(x, y, button, pressed):
    UpdateLastAction()

def on_scroll(x, y, dx, dy):
    UpdateLastAction()

def UpdateLastAction():
    global last_action
    last_action = GetCurTime()

def is_browser_work():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'Safari' == proc.info['name']: # Add Google, FireFox ...
            return True
    return False

# Основная часть
def Proxy_EnabledCheck():
    return is_proxy_enable

def DisableProxy():
    if not Proxy_EnabledCheck(): return
    #####
    global is_proxy_enable
    is_proxy_enable = False
    #####
    print('Disable proxy')

def EnableProxy():
    if Proxy_EnabledCheck(): return
    #####
    global is_proxy_enable
    is_proxy_enable = True
    #####
    print('Enable proxy')

def InactionCheck(last_action):
    return (GetCurTime() - last_action).total_seconds() > INACTION_MAX_TIME

def start_listeners():
    with keyboard.Listener(on_press=on_key) as key_listener, \
         mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as mouse_listener:
        key_listener.join()
        mouse_listener.join()

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(start_listeners)

    while True:
        if InactionCheck(last_action):
           DisableProxy()
        else:
            if is_browser_work():
                EnableProxy()
            else:
                DisableProxy()

            print("Scanning...")

        time.sleep(1)