import os
import shutil

wlan = "WLAN-bashiru-secret.xml"

new_name = wlan[::-1]
this_name = new_name[4:][::-1].lower()
for each in wlan:
    if "-" in each:
        idx = wlan.index("-")
        break

filename = this_name[idx+1:]
print(filename)

shutil.move("wifi.py", "dist")
