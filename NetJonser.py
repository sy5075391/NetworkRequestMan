
#! /usr/bin/env python3


#!/bin/python
"""
    Hello World, but with more meat.
    """

import wx
import os
import requests
import json
import subprocess
import XKModelConverter
import HeaderConfigDialog
class Myframe(wx.Frame):
    

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(Myframe, self).__init__(*args, **kw)
        panel = wx.Panel(self)
        self.panel = panel
        
        self.initData()
        
        l1 = wx.StaticText(panel,label = "Enter URL：",size = (50,40))
        # Url
        self.path_text = wx.TextCtrl(panel,size = (350,24))
        self.request_button = wx.Button(panel,label = "请求",size = (70,30))
        self.Bind(wx.EVT_BUTTON, self.request, self.request_button)

        # []顶部框
        topBox = wx.BoxSizer() # 不带参数表示默认实例化一个水平尺寸器
        topBox.Add(l1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        topBox.Add(self.path_text,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        topBox.Add(self.request_button,flag = wx.EXPAND|wx.ALL,border = 10) # 添加组件
        
        ## []参数配置框 左下box
        btmleftVBox = wx.BoxSizer(wx.VERTICAL)
        tipLbl = wx.StaticText(panel,label = "参数配置",size = (60,20))
        btmleftVBox.Add(tipLbl,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        header_button = wx.Button(panel,label = "Header配置",size = (70,30))
        self.Bind(wx.EVT_BUTTON, self.headerConfigClick, header_button)
        btmleftVBox.Add(header_button,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
            # 添加post get方式
        self.rbox = wx.RadioBox(panel, pos = (0,0), choices = ['GET','POST'],
                                majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
        self.rbox.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        btmleftVBox.Add(self.rbox)
        
        # 滚动视图
        list =  wx.ScrolledWindow(panel,style=wx.VSCROLL)
        self.list = list
        self.fgs = wx.BoxSizer(wx.VERTICAL)
        list.SetSizer(self.fgs)
        
        btmleftVBox.Add(self.list,1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        add_button = wx.Button(panel,label = "add",pos = (0,0),size = (70,30))
        self.Bind(wx.EVT_BUTTON, self.addParamsBox, add_button)
        btmleftVBox.Add(add_button,border = 3) # 添加组件
        ## []参数配置框 右下box
        btmRightVBox = wx.BoxSizer(wx.VERTICAL)
        tip2Lbl = wx.StaticText(panel,label = "响应数据",size = (80,20))
        open_button = wx.Button(panel,label = "打开本地json",size = (70,30))
        convert_button = wx.Button(panel,label = "json To OC—Model")
        self.Bind(wx.EVT_BUTTON, self.openFile, open_button)
        self.Bind(wx.EVT_BUTTON, self.convert, convert_button)
        btmRightVBox.Add(tip2Lbl,flag = wx.EXPAND|wx.ALL) # 添加组件
        btmRightVBox.Add(open_button) # 添加组件
        btmRightVBox.Add(convert_button) # 添加组件
        self.content_text= wx.TextCtrl(panel,style = wx.TE_MULTILINE)
        btmRightVBox.Add(self.content_text,proportion = 3,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        self._addParamsBox()
        self._addParamsBox()
        self._addParamsBox()
        self._addParamsBox()
        list.SetScrollbars(1, 1, 400, 500)
        list.Layout()
        ## []下box
        btmBox = wx.BoxSizer()
        
        btmBox.Add(btmleftVBox,proportion = 3,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件

        btmBox.Add(btmRightVBox,proportion = 5,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        v_box = wx.BoxSizer(wx.VERTICAL) # wx.VERTICAL参数表示实例化一个垂直尺寸器
        v_box.Add(topBox,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        v_box.Add(btmBox,proportion = 5,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件

        panel.SetSizer(v_box) # 设置主尺寸器
        self.Centre()
        self.Show()
    
    def initData(self):
        self.parmas = {}
        self.parmasDelBtnArr = []
        self.parmasBoxArr = []
        self.parmasTextArr = []
        self.method = "GET"
        self.headerData =  {'content-type': 'application/json'}
    
    def addParamsBox(self,event):
        box = self.getParamsBox()
        self.fgs.Add(box,flag = wx.EXPAND|wx.ALL)
        self.panel.Layout()
    
    def _addParamsBox(self):
        box = self.getParamsBox()
        self.fgs.Add(box,flag = wx.EXPAND|wx.ALL)
        self.panel.Layout()
    
    def setParams(self):
        self.parmas = {}
        for arr in self.parmasTextArr:        # 第二个实例
            tc1 = arr[0]
            tc2 = arr[1]
            key = tc1.GetLineText(0)
            value = tc2.GetLineText(0)
            if len(key) != 0 and len(value) != 0:
                self.parmas[key] = value
        print(self.parmas)
    
    def deleteClick(self,event):     # 定义打开文件事件
        btn = event.GetEventObject()
        index =  self.parmasDelBtnArr.index(btn)
        child = self.parmasBoxArr[index]
        child.hidden = True
        self.fgs.Hide(child)
        self.fgs.Remove(child)
        self.parmasDelBtnArr.pop(index)
        self.parmasBoxArr.pop(index)
        self.parmasTextArr.pop(index)
        self.panel.Layout()
        self.fgs.Layout()
        self.list.Layout()
    
    def getParamsBox(self):
        parmasBox = wx.BoxSizer() # 不带参数表示默认实例化一个水平尺寸器
        tc1 = wx.TextCtrl(self.list)
        tc2 = wx.TextCtrl(self.list)
        self.parmasTextArr.append([tc1,tc2])
        deleteBtn = wx.Button(self.list,label = "del",size = (40,30))
        self.parmasDelBtnArr.append(deleteBtn)
        self.parmasBoxArr.append(parmasBox)
        self.Bind(wx.EVT_BUTTON, self.deleteClick, deleteBtn)
        parmasBox.Add(tc1,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        parmasBox.Add(tc2,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        parmasBox.Add(deleteBtn,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        return parmasBox

    def request(self,event):     # 定义打开文件事件
        self.content_text.SetValue('')
        path = self.path_text.GetValue()

        self.setParams()
 
        if self.method == "GET":
            print("GET")
            r = requests.get(path,params = self.parmas,headers = self.headerData)
        else:
            print("GET")
            r = requests.post(path, json=self.parmas,headers = self.headerData)
        
        r.encoding = 'utf-8'
        response = r.json()
        
        print("response:")
        print(response)
        str = json.dumps(response, indent=2, ensure_ascii=False)
        rootDir= os.environ['HOME']
        os.chdir(rootDir+'/Desktop')
        with open('data.json', 'w', encoding='utf-8') as file:
            file.write(str) #ensure_ascii=False可以消除json包含中文的乱码问题
        self.content_text.SetValue(str)
    
    def headerConfigClick(self,event):
        def changeResult(y):
            print(y)
            self.headerData = y
        HeaderConfigDialog.HeaderConfigDialog(self,"Header配置",self.headerData,changeResult).Show()
    
    
    def openFile(self,event):     # 定义打开文件事件
        subprocess.call("open data.json",shell=True)
    
    def onRadioBox(self,e):
        self.method = self.rbox.GetStringSelection()
        print(self.rbox.GetStringSelection(),' is clicked from Radio Box')
    
    def convert(self,event):     # 定义打开文件事件
        XKModelConverter.ConvertDialog(self, "模型转化",self.content_text.GetValue()).Show()


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    
    app = wx.App()
    Myframe(None,title = "network to json",size = (800,500))
    app.MainLoop()

