
#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        distributionViewPanel.py
#
# Purpose:     This module is used to provide different function panels for the 
#              distributionViewer. 
#              
# Author:      Yuancheng Liu
#
# Created:     2019/08/02
# Copyright:   NUS-Singtel Cyber Security Research & Development Laboratory
# License:     YC @ NUS
#-----------------------------------------------------------------------------

import wx
import wx.grid
import distributionViewGlobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelChart(wx.Panel):
    """ This function is used to provide lineChart wxPanel to show the all the 
        data as a distribution line.
    """
    def __init__(self, parent, dataSetNum, appSize=(1600, 290), recNum=750):
        """ Init the panel."""
        wx.Panel.__init__(self, parent, size=(appSize[0], 290))
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.recNum = recNum    # hole many revode we are going to show.
        self.appSize = appSize  # the panel size.
        self.updateFlag = True  # flag whether we update the diaplay area
        self.dataSetNum = dataSetNum
        self.dataD = [[0]*recNum for _ in range(dataSetNum)]
        # Above line can not use [[0]*num]*num, otherwise change one element 
        # all column will be change, the explaination is here: 
        # https://stackoverflow.com/questions/2739552/2d-list-has-weird-behavor-when-trying-to-modify-a-single-value
        self.times = [n for n in range(self.recNum//10)]  # X-Axis(time delay).
        self.maxCount = 0       # max count of the delay in the current data set.
        self.readDisMode = True # True: real display mode, False: fixed display mode.
        self.labelInfo = ['Data1', 'Data2', 'Data3']
        self.Bind(wx.EVT_PAINT, self.onPaint)
        
#-----------------------------------------------------------------------------        
    def clearData(self):
        """ Clear all the times data to 0 """
        self.dataD = [[0]*self.recNum for _ in range(self.dataSetNum)]

#-----------------------------------------------------------------------------  
    def _drawBG(self, dc):
        """ Draw the line chart background."""
        dc.SetPen(wx.Pen('WHITE'))
        dc.DrawRectangle(1, 1, self.appSize[0], 205)
        dc.DrawText('NetFetcher Delay Time Distribution', 2, 245)
        xlabel = 'occurences' if self.readDisMode else 'occurences[x10]'
        dc.DrawText(xlabel, -35, 225)
        dc.DrawText('Delay[x1000 ns]', 700, -25)
        # Draw Axis and Grids:(Y delay time, x occurences)
        dc.SetPen(wx.Pen('#D5D5D5'))  # dc.SetPen(wx.Pen('#0AB1FF'))
        w, _ = self.appSize
        dc.DrawLine(1, 1, w, 1)
        dc.DrawLine(1, 1, 1, w)
        self.maxCount = max([max(i) for i in self.dataD]) if self.readDisMode else 0
        # Draw the Y-Axis
        for i in range(2, 22, 2):
            dc.DrawLine(2, i*10, w, i*10)  # Y-Grid
            dc.DrawLine(2, i*10, -5, i*10)  # Y-Axis
            ylabel = str(self.maxCount//20 *i) if self.readDisMode else str(i).zfill(2)
            dc.DrawText(ylabel, -25, i*10+5)  # format to ## int, such as 02
        # Draw the X-Axis
        for i in range(len(self.times)):
            dc.DrawLine(i*20, 2, i*20, 200)  # X-Grid
            dc.DrawLine(i*20, 2, i*20, -5)  # X-Axis
            dc.DrawText(str(self.times[i]).zfill(2), i*20-5, -5)

#--PanelChart--------------------------------------------------------------------
    def _drawFG(self, dc):
        """ Draw the front ground data chart line."""
        item = ((self.labelInfo[0], 'RED'), 
                (self.labelInfo[1], '#A5CDAA'), 
                (self.labelInfo[2], 'BLUE'))
        lineW = 1 if self.readDisMode else 2
        # Draw the charts.
        for idx, data in enumerate(self.dataD):
            (label, color) = item[idx]
            # Draw the line sample.
            dc.SetPen(wx.Pen(color, width=lineW, style=wx.PENSTYLE_SOLID))
            dc.DrawText(label, idx*200+150, 220)
            dc.DrawLine(120+idx*200, 212, 120+idx*200+20, 212)
            if self.readDisMode: 
                dc.DrawSpline([(int(i*2+idx*2), int(data[i])*200//self.maxCount) for i in range(self.recNum)])
            else:
                dc.DrawSpline([(int(i*2+idx*2), min(200,int(data[i])*1)) for i in range(self.recNum)])

#----------------------------------------------------------------------------- 
    def onPaint(self, event):
        """ Main panel drawing function."""
        dc = wx.PaintDC(self)
        # set the axis orientation area and fmt to up + right direction.
        dc.SetDeviceOrigin(40, 250)
        dc.SetAxisOrientation(True, True)
        # set the text font 
        font = dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        # draw the background 
        self._drawBG(dc)
        # draw the distribution chart.
        self._drawFG(dc)

#----------------------------------------------------------------------------- 
    def periodic(self, event):
        """ Call back every periodic time."""
        # Set the title of the frame.
        pass

#-----------------------------------------------------------------------------  
    def setLabel(self, labelList):
        """ Set the chart color label. <labelList>: the list of the CSV file's path."""
        splitChr = '\\' if gv.WINP else '/'
        for i in range(len(labelList)):
            self.labelInfo[i] = str(labelList[i].split(splitChr)[-1])[:-3]

#----------------------------------------------------------------------------- 
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function 
            will set the self update flag.
        """
        if updateFlag is None and self.updateFlag: 
            self.Refresh(False)
            self.Update()
        else:
            self.updateFlag = updateFlag

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelSetting(wx.Panel):
    """ Experiment setup panel."""
    def __init__(self, parent):
        """ Init the panel."""
        wx.Panel.__init__(self, parent, size=(620, 250))
        self.SetBackgroundColour(wx.Colour(200, 200, 210))
        self.SetSizer(self.buidUISizer())

#-----------------------------------------------------------------------------
    def buidUISizer(self):
        """ Build the Panel UI"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        flagsR = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(
            self, label="Fill The Information In The Grid: "), flag=flagsR, border=2)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticLine(self, wx.ID_ANY, size=(640, -1),
                                style=wx.LI_HORIZONTAL), flag=flagsR, border=2)
        sizer.AddSpacer(5)
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(5, 6)
        # Set the Grid size.
        self.grid.SetRowLabelSize(40)
        self.grid.SetColSize(0, 80)
        self.grid.SetColSize(1, 80)
        self.grid.SetColSize(2, 80)
        self.grid.SetColSize(3, 80)
        self.grid.SetColSize(4, 80)
        self.grid.SetColSize(5, 150)
        # Set the Grid's labels.
        self.grid.SetColLabelValue(0, 'IP Address')
        self.grid.SetColLabelValue(1, 'Port Num ')
        self.grid.SetColLabelValue(2, 'File ID ')
        self.grid.SetColLabelValue(3, 'Block Num')
        self.grid.SetColLabelValue(4, 'Iterations ')
        self.grid.SetColLabelValue(5, 'Output File')
        #self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.highLightMap)
        sizer.Add(self.grid, flag=flagsR, border=2)
        sizer.AddSpacer(5)
        self.pauseBt = wx.Button(
            self, label='Construct Model', style=wx.BU_LEFT, size=(100, 23))
        self.pauseBt.Bind(wx.EVT_BUTTON, self.onConstruct)
        sizer.Add(self.pauseBt, flag=wx.ALIGN_CENTER_HORIZONTAL, border=2)
        return sizer

#-----------------------------------------------------------------------------
    def onConstruct(self, event):
        """ Create the experiment setup file based on data in the grid. """
        with open(gv.CONFIG_FILE, 'w') as fh:
            for i in range(5):
                if self.grid.GetCellValue(i, 0) == '':continue
                data = [self.grid.GetCellValue(i, j) for j in range(6)]
                line = 'Run: '+data[0]+':'+data[1]+' ' + \
                    data[2]+':'+data[3]+' '+data[4]+' '+data[5]
                fh.write(line+'\n')
                fh.write('sleep1\n\n')
