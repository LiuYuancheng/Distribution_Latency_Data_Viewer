#-----------------------------------------------------------------------------
# Name:        distributionViewGlobal.py
#
# Purpose:     This module is used set the Local config file as global value 
#              which will be used in the other modules.
# Author:      Yuancheng Liu
#
# Created:     2019/08/01
# Version:     v_0.1.1
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import os
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)

#------<CONSTANTS>-------------------------------------------------------------
# Application name and version. setting
APP_NAME = 'Data Transmission Latency SIEM Log Distribution Data Viewer'
WINP = os.name == 'nt'
# Program title icon
ICON_PATH = os.path.join(dirpath, 'img', 'title.png')
# Module folder:
MODE_F_PATH = os.path.join(dirpath, 'model', '*.csv')
# Data folder:
DATA_F_PATH = os.path.join(dirpath, 'data', '*.csv')
# The config file for the netfetcher program.
CONFIG_FILE = ("model_scripted_exp.bat", "check_scripted_exp.bat")
# The experiment config data.
# Format: [IP Address, Port Num, File ID, Block Num, Iterations, Output File]
EXP_CONFIG = (('127.0.0.1', '5555', 'file_20180617.dat', '1024', '99999', 'exp-localHost.csv'),
              ('172.16.1.3', '5555', 'file_20180617.dat','1024', '99999', 'exp-netStorage.csv'),
              ('172.16.1.2', '5555', 'file_20180617.dat','1024', '99999', 'exp-remHost.csv'),
              ('172.16.1.4', '5555', 'file_20180617.dat', '1024', '99999', 'exp-data.csv'),)
              
#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFame = None    # mail frame
iDataMgr = None     # data manager.
iChartPanel0 = None # history chart panel for module
iChartPanel1 = None # history chart panel for data.
iMatchPanel = None  # Data match panel.
iChartPanel3 = None # compare panel for data and module.
iSetupPanel = None  # experiment setup panel.
iCPMode = False     # compare mode flag.
iModelType = 5      # Model Type currently displayed
iDataType = 5       # Data Type currently displayed
iUpdateRate = 2     # Time period to update the 
iLineStyle = 1      # width of the chart line
iMatchFlag = False  # whether we do match function. 
