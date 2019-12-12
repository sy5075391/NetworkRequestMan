

#! /usr/bin/env python3

import wx
import json
class ConvertDialog(wx.Dialog):
    def __init__(self, parent, title,jsonStr):
        super(ConvertDialog, self).__init__(parent = parent, title = title, size = (1200,800))
        self.jsonStr = jsonStr
        self.InitUI() #绘制Dialog的界面
    
    def InitUI(self):
        self.panel = wx.Panel(self)
        hBox = wx.BoxSizer() # 不带参数表示默认实例化一个水平尺寸器
        self.jsonTextCtrl = wx.TextCtrl(self.panel,style = wx.TE_MULTILINE|wx.TE_RICH|wx.TE_PROCESS_ENTER)
        self.modelHTextCtrl = wx.TextCtrl(self.panel,style = wx.TE_MULTILINE)
        self.modelMTextCtrl = wx.TextCtrl(self.panel,style = wx.TE_MULTILINE)
        self.jsonTextCtrl.SetValue(self.jsonStr)
        convert_button = wx.Button(self.panel,label = "convert",size = (70,30))
        self.Bind(wx.EVT_BUTTON, self.convert, convert_button)
        hBox.Add(self.jsonTextCtrl,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        hBox.Add(convert_button,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        vBox = wx.BoxSizer(wx.VERTICAL)
        vBox.Add(self.modelHTextCtrl,proportion = 3.5,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        vBox.Add(self.modelMTextCtrl,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        
        hBox.Add(vBox,proportion = 1,flag = wx.EXPAND|wx.ALL,border = 3) # 添加组件
        self.panel.SetSizer(hBox) # 设置主尺寸器

    def convert(self,event):
        text = self.jsonTextCtrl.GetValue()
        self.resultModelStr = ""
        self.resultModelStrForM = ""
        try:
            jsonDic = json.loads(text)
        except Exception as e:
            wx.MessageBox(repr(e), "json数据格式不正确" ,wx.OK | wx.ICON_INFORMATION)
        else:
            self.findRealJsonDic(jsonDic)

    def findRealJsonDic(self,jsonDic):
        try:
            realModelDic = {}
            if type(jsonDic) == dict:
                realModelDic = jsonDic
            elif type(jsonDic) == list:
                realModelDic = jsonDic[0]
                if type(realModelDic) != dict:
                    wx.MessageBox("不包含对象", "json数据格式不正确" ,wx.OK | wx.ICON_INFORMATION)
                    return
            else:
                wx.MessageBox("请检查", "json数据格式不正确" ,wx.OK | wx.ICON_INFORMATION)
                return

        except Exception as e:
            wx.MessageBox(repr(e), "错误" ,wx.OK | wx.ICON_INFORMATION)
                
        else:
            self.preClasses = []
            self.convertToModel(realModelDic)
            self.addPreClass()
            self.modelHTextCtrl.SetValue(self.resultModelStr)
            self.modelMTextCtrl.SetValue(self.resultModelStrForM)
    
    def addPreClass(self):
        pre = ""
        for className in self.preClasses:
            pre = pre + "@class " + className + ";\n"
        self.resultModelStr =  pre + "\n" + self.resultModelStr
    
    def convertToModel(self,jsonDic,ClassName = "XKJsonModel"):
        total = "@interface "+ClassName+" : NSObject"
        self.insertMImpletion(ClassName)
        total = total+"\n"
        remainDatas = []
        for key in jsonDic:
            value = jsonDic[key]
            valueType = type(value)
            if valueType == dict:
                innerClassName = "XK"+ key.title()
                total = total+"@property(nonatomic, strong) "+innerClassName+ "  *"+key+";\n"
                remainDatas.append([innerClassName,value])
                self.preClasses.append(innerClassName)
            elif valueType == list:
                innerClassName = "XK"+ key.title()
                if len(value) > 0:
                    dicOfList = value[0]
                    if type(dicOfList) == dict:
                        total = total+"@property(nonatomic, copy) NSArray <" +innerClassName+" *>*"+key+";\n"
                        remainDatas.append([innerClassName,dicOfList])
                        self.preClasses.append(innerClassName)
                    elif type(dicOfList) == list:
                        total = total+"@property(nonatomic, copy) NSArray < NSArray*>*"+key+";\n"
                        #数组里嵌数组的数据太捉急 就不继续处理了
                    else:
                        total = total+"@property(nonatomic, copy) NSArray *"+key+";\n"
                else:
                    total = total+"@property(nonatomic, copy) NSArray *"+key+";\n"
            else:
                classType = ""
                if valueType == int:
                    total = total+"@property(nonatomic, assign) NSInteger "+ key +";\n"
                else:
                    total = total+"@property(nonatomic, copy) NSString *"+ key +";\n"
        
        total = total + "@end" + "\n\n"
        self.resultModelStr = self.resultModelStr + total
        for remainData in remainDatas:
            self.convertToModel(remainData[1],remainData[0])
        
    def insertMImpletion(self,className):
        self.resultModelStrForM = self.resultModelStrForM + "@implementation " + className +"\n\n"+ "@end" +"\n\n"
