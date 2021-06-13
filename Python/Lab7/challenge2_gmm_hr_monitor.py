#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:30:52 2020

@author: siyuanzhang
"""

from ECE16Lib.HRMonitor import HRMonitor 
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import sleep
import numpy as np

if __name__ == "__main__":
    hrm = HRMonitor() 
    #hrm.train()
    hrm.predict()
    