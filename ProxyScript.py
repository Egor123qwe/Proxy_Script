from pynput import keyboard, mouse
import time
import datetime
import concurrent.futures
import psutil
import subprocess



# Инициализация
def GetCurTime():
    return datetime.datetime.now()

INACTION_MAX_TIME = 5 * 60
last_action = GetCurTime()

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
def changeProxyData(address, port, is_more, login, password):
    command = f"networksetup -setwebproxy Wi-Fi {address} {port}"
    if is_more:
        command += f" on"
        command += f" {login} {password}"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode != 0:
        print(f"Произошла ошибка при обновлении прокси-сервера: {error.decode('utf-8')}")


def SetProxyOff():
    command = "networksetup -setwebproxystate Wi-Fi off"
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def Proxy_EnabledCheck():
    command = "networksetup -getwebproxy Wi-Fi"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if process.returncode == 0 and "Enabled: Yes" in output.decode('utf-8'):
        return True
    else:
        return False


def DisableProxy():
    if not Proxy_EnabledCheck(): return
    print('Disable proxy')
    changeProxyData("\b", "0", True, "\b ", "0")
    SetProxyOff()
    

def EnableProxy():
    if Proxy_EnabledCheck(): return
    print('Enable proxy')
    changeProxyData("proxy.example.com", 8080, True, "ya", "1232222222223214124124")

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