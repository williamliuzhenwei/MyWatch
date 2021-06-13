#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 00:03:36 2020

@author: liuzhenwei
"""

from ECE16Lib.Communication import Communication
from ECE16Lib.Communication import sleep
i = 0
if __name__ == "__main__":
  
  
  try:
    comms = Communication("/dev/cu.ECE16-ESP32_SPP_SERVER",115200)
    print(comms)
    comms.clear()
    while i < 30:
        i = i + 1
        timer = str(i)
        comms.send_message(timer + "seconds")
        sleep(1)
        print(comms.receive_message())
    print("Normal program execution finished")
  except KeyboardInterrupt:
    print("User stopped the program with CTRL+C input")
  finally:
    comms.close()
    print("Cleaning up and exiting the the program")
      