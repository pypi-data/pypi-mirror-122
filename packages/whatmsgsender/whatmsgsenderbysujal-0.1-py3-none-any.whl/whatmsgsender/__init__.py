#made by sujal
import webbrowser as w
import time 
from datetime import datetime
import pyautogui
def sendmsg(number,message,hour,minute):
    sending_time = hour*60 + minute
    now = datetime.now()
    current_time_hour = int(now.strftime("%H"))*60
    current_time_min = int(now.strftime("%M"))
    current_time_sec = int(now.strftime("%S"))
    current_time =  current_time_hour+current_time_min
    timeformsg = (sending_time-current_time)*60 - current_time_sec
    if timeformsg <= 30:
        print("time is less than 30 seconds")
        exit()
    print("the msg will send after:",timeformsg,"seconds")
    time.sleep(timeformsg-20)
    w.open('https://api.whatsapp.com/send?phone='+number+'&text='+message)
    time.sleep(4)
    pyautogui.click(1000, 400)
    time.sleep(16)
    pyautogui.press("enter")
    pyautogui.press('enter')
