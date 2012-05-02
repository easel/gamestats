import sys
import wx
from wx import xrc
import re
import threading
import StringIO

import logparse

class ParserThread(threading.Thread):
    def __init__(self, filepath, mode='parse'):
        threading.Thread.__init__(self)
        self.__filepath = filepath
        self.__mode = mode
        self.stop = threading.Event()
        self.parser = logparse.Parser(debug=True, stopEvent=self.stop)
        
    def run(self):
        if not self.__filepath:
            raise Exception('Invalid path ' + self.__filepath)
        if self.__mode == 'parse':
            self.parser.parse(self.__filepath)
        elif self.__mode == 'monitor':
            self.parser.monitor(self.__filepath)
        else:
            raise Exception('Invalid mode ' + self.mode)
        self.stop.clear()
        
class ThreadSafeIOBuffer(list):
    def __init__(self):
        list.__init__(self)
        self.sem = threading.Semaphore()
                
    def write(self, val):
        self.sem.acquire()
        self.append(val)
        self.sem.release()
        wx.WakeUpIdle()
                
class LogParser(wx.App):
    def OnInit(self):
        sys.stdout = ThreadSafeIOBuffer()       
        self.res = xrc.XmlResource('lpgui.xrc')
        self.InitFrame()
        self.parser = None
        self.fmMain.Show()       
        return True    
        
    def InitFrame(self):
        self.fmMain = self.res.LoadFrame(None, "fmMain")
        self.teLog = xrc.XRCCTRL(self.fmMain, "teLog")
        self.teLogFileName = xrc.XRCCTRL(self.fmMain, "teLogFileName")
        self.btnParse = xrc.XRCCTRL(self.fmMain, "btnParse")
        self.btnMonitor = xrc.XRCCTRL(self.fmMain, "btnMonitor")
        self.btnStop = xrc.XRCCTRL(self.fmMain, "btnStop")
        self.fmMain.Bind(wx.EVT_BUTTON, self.SelectClick, id=xrc.XRCID("btnSelect"))
        self.fmMain.Bind(wx.EVT_BUTTON, self.ParseClick, id=xrc.XRCID("btnParse"))
        self.fmMain.Bind(wx.EVT_BUTTON, self.monitorClick, id=xrc.XRCID("btnMonitor"))
        self.fmMain.Bind(wx.EVT_BUTTON, self.StopClick, id=xrc.XRCID("btnStop"))
        self.fmMain.Bind(wx.EVT_BUTTON, self.RotateClick, id=xrc.XRCID("btnRotate"))
        self.fmMain.Bind(wx.EVT_BUTTON, self.ExitClick, id=xrc.XRCID("btnExit"))
        self.Bind (wx.EVT_IDLE, self.OnIdle)
        
    def UpdateButtonStates(self):
        hasFileSelected = self.teLogFileName.GetValue() != ''
        isRunning = bool(self.parser and self.parser.isAlive())
        self.btnParse.Enable(hasFileSelected and not isRunning)
        self.btnMonitor.Enable(hasFileSelected and not isRunning)
        self.btnStop.Enable(isRunning)

    def OnIdle(self, event):
        "idle loop to display output from the worker thread"
        if sys.stdout.sem.acquire(False):
            while len(sys.stdout):
                self.teLog.AppendText(sys.stdout.pop(0))
            sys.stdout.sem.release()
        self.UpdateButtonStates()
           
    def SelectClick(self, evt):
        dialog = wx.FileDialog(self.fmMain, style=wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.teLogFileName.SetValue(dialog.GetPath())
        print 'Selected ' + self.teLogFileName.GetValue()
    
    def ParseClick(self, evt):
        if self.teLog.GetNumberOfLines() > 1000:
            self.teLog.SetValue('')
        self.parser = ParserThread(filepath=self.teLogFileName.GetValue(), mode='parse')
        self.parser.start()
                
    def monitorClick(self, evt):
        if self.teLog.GetNumberOfLines() > 1000:
            self.teLog.SetValue('')
        self.parser = ParserThread(filepath=self.teLogFileName.GetValue(), mode='monitor')
        self.parser.start()
             
    def StopClick(self, evt):
        self.parser.stop.set()
        
    def RotateClick(self, evt):
        print 'rotate clicked'
           
    def ExitClick(self, evt):
        self.Exit()

def main():
    app = LogParser(0)
    app.MainLoop()
    
if __name__ == '__main__':
    main()
