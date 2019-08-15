### 基于python3，wxPython开发的网络请求工具，同时包含json数据转模型的功能。
## 工具界面
![UI界面](https://upload-images.jianshu.io/upload_images/1956050-056515b9ef18b206.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![模拟请求](https://upload-images.jianshu.io/upload_images/1956050-d161a041c02a7fa5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![Json转Model](https://upload-images.jianshu.io/upload_images/1956050-f1027ac98a65c195.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 使用说明
### 1. 命令行执行
>需要安装python3

cd 到工程目录
```python3 NetJonser.py```
### 2. 打包执行
>需要安装python3

![可执行app](https://upload-images.jianshu.io/upload_images/1956050-233ce464e673c32a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以使用工程中已经打包好`NetJonser`的app。
也可以自定义修改后重新打包
#### pyinstall 打包:
>- pyinstaller是能将py程序编译成应用程序形式的一个pip组件。它使用pip安装。
安装 `pip3 install pyinstaller`

cd 到项目路径，
运行程序入口，也就是main函数所在文件 NetJonser.py
在项目所在工作路径输入命令：

`sudo pyinstaller --windowed --onefile --clean --noconfirm NetJonser.py`
`sudo pyinstaller --clean --noconfirm --windowed --onefile NetJonser.spec`


sudo 获取权限，可能要求输入密码
如果想要打出来的包有图标第一条命了替换：

`pyinstaller --windowed --onefile --icon=sat_tool_icon.icns --clean --noconfirm NetJonser.py`

一般很少一次通过，主要是一些包导入问题和项目文件配置路径
我遇到问题时找不到项目的配置文件
获取包路径的父路径，不可将路径写成绝对路径

