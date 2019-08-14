

#! /usr/bin/env python3

import wx
import json
class HeaderConfigDialog(wx.Dialog):
    def __init__(self, parent, title,headerData,resultFunc):
        super(HeaderConfigDialog, self).__init__(parent = parent, title = title, size = (400,400))
        self.initData()
        self.headerData = headerData
        self.InitUI() #绘制Dialog的界面
        self.resultFunc = resultFunc

    
    def InitUI(self):

        # 滚动视图
        self.panel = panel = wx.Panel(self)

        self.Bind(wx.EVT_CLOSE, self.close)
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        
        list =  wx.ScrolledWindow(panel,style=wx.VSCROLL)
        self.list = list
        self.fgs = wx.BoxSizer(wx.VERTICAL)
        list.SetSizer(self.fgs)
        
        vBox.Add(self.list,1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        if len(self.headerData.keys()) == 0:
            self._addParamsBox()
            self._addParamsBox()
            self._addParamsBox()
            self._addParamsBox()
            self._addParamsBox()
            self._addParamsBox()
        else:
            for key in self.headerData:
              
                self._addParamsBox(key,self.headerData[key])
        
        list.SetScrollbars(1, 1, 400, 500)

        list.Layout()
        
        add_button = wx.Button(panel,label = "add",pos = (0,0),size = (70,30))
        self.Bind(wx.EVT_BUTTON, self.addParamsBox, add_button)
        vBox.Add(add_button,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        self.panel.SetSizer(vBox) # 设置主尺寸器
    
    def configParams(self):
        self.params = {}
        for arr in self.paramsTextArr:        # 第二个实例
            tc1 = arr[0]
            tc2 = arr[1]
            key = tc1.GetLineText(0)
            value = tc2.GetLineText(0)
            if len(key) != 0 and len(value) != 0:
                self.params[key] = value
    
        return self.params
    
    def initData(self):
        self.paramsDelBtnArr = []
        self.paramsBoxArr = []
        self.paramsTextArr = []
        self.headerData = {}
    
    def addParamsBox(self,event):
        box = self.getParamsBox()
        self.fgs.Add(box,flag = wx.EXPAND|wx.ALL)
        self.panel.Layout()
    
    def _addParamsBox(self,key = "",value = ""):
        box = self.getParamsBox(key,value)
        self.fgs.Add(box,flag = wx.EXPAND|wx.ALL)
        self.panel.Layout()
            
    def deleteClick(self,event):     # 定义打开文件事件
        btn = event.GetEventObject()
        index =  self.paramsDelBtnArr.index(btn)
        child = self.paramsBoxArr[index]
        child.hidden = True
        self.fgs.Hide(child)
        self.fgs.Remove(child)
        self.paramsDelBtnArr.pop(index)
        self.paramsBoxArr.pop(index)
        self.paramsTextArr.pop(index)
       
        self.fgs.Layout()
        self.panel.Layout()
                        
    def getParamsBox(self,key = "",value = ""):
        
        paramsBox = wx.BoxSizer() # 不带参数表示默认实例化一个水平尺寸器
        tc1 = wx.TextCtrl(self.list)
        tc1.SetValue(key)
        tc2 = wx.TextCtrl(self.list)
        tc2.SetValue(value)
        self.paramsTextArr.append([tc1,tc2])
        deleteBtn = wx.Button(self.list,label = "del",size = (40,30))
        self.paramsDelBtnArr.append(deleteBtn)
        self.paramsBoxArr.append(paramsBox)
        self.Bind(wx.EVT_BUTTON, self.deleteClick, deleteBtn)
        paramsBox.Add(tc1,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        paramsBox.Add(tc2,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        paramsBox.Add(deleteBtn,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        return paramsBox

    def close(self,event):
        self.resultFunc(self.configParams())
        self.Destroy()
