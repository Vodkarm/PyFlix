import os, zipfile, requests, ctypes

ctypes.windll.user32.MessageBoxW(0, "Please do not stop your computer during update. (It will be short)", "PyFlix Updater", 0)
os.remove("main.py")

open("new.zip", "wb").write(requests.get("https://raw.githubusercontent.com/Vodkarm/PyFlix/main/actual.zip").content)
zipfile.ZipFile("new.zip", "r").extractall()
ctypes.windll.user32.MessageBoxW(0, "Update finished ! Restarting PyFlix...", "PyFlix Updater", 0)
os.remove("new.zip")
os.system("python main.py")
exit()