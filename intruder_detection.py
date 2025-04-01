
#https://www.hackster.io/AlexWulff/ai-intruder-detection-system-with-huskylens-98e636
import time
import json
from huskylib import HuskyLensLibrary

# Program Parameters
text_on = True
sms_interval = 10
last_sms_time = 0

# Change for your Serial Port
hl = HuskyLensLibrary("SERIAL", "COM6", 3000000)

while True:
    blocks = hl.requestAll()

    for block in blocks:
        if block.learned == True:
            print("Known Face!")
        else:
            print("Unknown Face!")
            time.sleep(0.5)
    time.sleep(2);