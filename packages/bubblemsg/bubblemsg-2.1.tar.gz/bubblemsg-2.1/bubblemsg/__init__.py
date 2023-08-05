'''

bubblemsg：版本1.0
一个基于气泡窗而生的模块。功能简化，无需任何复杂操作！

发明灵感：因为气泡窗操作太过复杂，作者想了个好方法，将其压缩成一个模块！
当前只有两个模块，以后作者可以根据灵感加入新模块！(＾Ｕ＾)ノ~ＹＯ
'''


def bubblemsg(titles:str,msgs:str,nx:int):
    '''
    
    bubblemsg介绍：
    可以弹出气泡窗，代码简化，易于使用，无需任何依赖项！


    bubblemsg(titles:str,msgs:str,nx:int)
    titles:气泡窗的标题
    msgs:气泡窗的主要内容
    nx:气泡窗类型，None为无声弹出，0为有声但无图标弹出，1为info，2为error，3为warning。
    '''
    import win32gui,win32api,win32con
    import random
    
    nxlist = [0,1,2,3,None]
    if nx not in nxlist:
        return 'error'
    else:
        class TestTaskbarIcon:
            def __init__(self):
                # 注册一个窗口类
                wc = win32gui.WNDCLASS()
                hinst = wc.hInstance = win32gui.GetModuleHandle(None)
                name_str = str(random.uniform(0,1000000000000))#随机字符串，防止报错pywintypes.error: (1410, 'RegisterClass', '类已存在。')
                wc.lpszClassName = name_str
                wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
                classAtom = win32gui.RegisterClass(wc)
                style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
                self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                                  0, 0, hinst, None)
                hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
                self.hicon=hicon
                nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
                win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
                
            def showMsg(self, title, msg):
                if nx == None:
                    nid = (self.hwnd,  # 句柄
                        0,  # 托盘图标ID
                        win32gui.NIF_INFO,  # 标识
                        0,  # 回调消息ID
                        0,  # 托盘图标句柄
                        "TestMessage",  # 图标字符串
                        msg,  # 气球提示字符串
                        0,  # 提示的显示时间←这个提示时间改了也没用的样子
                        title,  # 提示标题
                        win32gui.NIIF_NOSOUND  # 提示用到的图标
                    )
                elif nx == 0:
                    nid = (self.hwnd,  # 句柄
                            0,  # 托盘图标ID
                            win32gui.NIF_INFO,  # 标识
                            0,  # 回调消息ID
                            0,  # 托盘图标句柄
                            "TestMessage",  # 图标字符串
                            msg,  # 气球提示字符串
                            0,  # 提示的显示时间←这个提示时间改了也没用的样子
                            title,  # 提示标题
                            win32gui.NIIF_NONE  # 提示用到的图标
                            )
                elif nx == 1:
                    nid = (self.hwnd,  # 句柄
                    0,  # 托盘图标ID
                    win32gui.NIF_INFO,  # 标识
                    0,  # 回调消息ID
                    0,  # 托盘图标句柄
                    "TestMessage",  # 图标字符串
                    msg,  # 气球提示字符串
                    0,  # 提示的显示时间←这个提示时间改了也没用的样子
                    title,  # 提示标题
                    win32gui.NIIF_INFO  # 提示用到的图标
                        )
                elif nx == 2:
                    nid = (self.hwnd,  # 句柄
                    0,  # 托盘图标ID
                    win32gui.NIF_INFO,  # 标识
                    0,  # 回调消息ID
                    0,  # 托盘图标句柄
                    "TestMessage",  # 图标字符串
                    msg,  # 气球提示字符串
                    0,  # 提示的显示时间←这个提示时间改了也没用的样子
                    title,  # 提示标题
                    win32gui.NIIF_ERROR  # 提示用到的图标
                        )
                elif nx == 3:
                    nid = (self.hwnd,  # 句柄
                    0,  # 托盘图标ID
                    win32gui.NIF_INFO,  # 标识
                    0,  # 回调消息ID
                    0,  # 托盘图标句柄
                    "TestMessage",  # 图标字符串
                    msg,  # 气球提示字符串
                    0,  # 提示的显示时间←这个提示时间改了也没用的样子
                    title,  # 提示标题
                    win32gui.NIIF_WARNING  # 提示用到的图标
                        )
                self.nid = nid
                win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
            def OnDestroy(self, hwnd, msg, wparam, lparam):
                nid = (self.hwnd, 0)
                win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
                win32gui.PostQuitMessage(0)  # Terminate the app.
                        
        def show_msg(title,msg):
	        t = TestTaskbarIcon()
	        t.showMsg(title, msg)

        show_msg(titles,msgs)

def msgnosound(nx):
    '''
    
    本函数将会在任务栏右下角生成一个小图标
    但若鼠标移动到小图标，小图标将会立即消失，无影无踪。
    nx：0为有图标，1为无图标
    '''
    import win32gui,win32api,win32con
    import time
    import random
     
    nxlist = [0,1]
    if nx in nxlist:
        class TestTaskbarIcon:
            def __init__(self):
                # 注册一个窗口类
                wc = win32gui.WNDCLASS()
                hinst = wc.hInstance = win32gui.GetModuleHandle(None)
                name_str = str(random.uniform(0,1000000000000))#随机字符串，防止报错pywintypes.error: (1410, 'RegisterClass', '类已存在。')
                wc.lpszClassName = name_str
                wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
                classAtom = win32gui.RegisterClass(wc)
                style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
                self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                                  0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                                  0, 0, hinst, None)
                hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
                self.hicon=hicon
                nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
                win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
                
            def showMsg(self, title, msg):
                if nx == 0:
                    nid = (self.hwnd,  # 句柄
                           0,  # 托盘图标ID
                           win32gui.NIF_MESSAGE,  # 标识
                           0,  # 回调消息ID
                           0,  # 托盘图标句柄
                           "TestMessage",  # 图标字符串
                           msg,  # 气球提示字符串
                            0,  # 提示的显示时间←这个提示时间改了也没用的样子
                            title,  # 提示标题
                            win32gui.NIIF_NONE  # 提示用到的图标
                            )
                elif nx == 1:
                    nid = (self.hwnd,  # 句柄
                            0,  # 托盘图标ID
                            win32gui.NIF_ICON,  # 标识
                            0,  # 回调消息ID
                            0,  # 托盘图标句柄
                            "TestMessage",  # 图标字符串
                            msg,  # 气球提示字符串
                            0,  # 提示的显示时间←这个提示时间改了也没用的样子
                            title,  # 提示标题
                            win32gui.NIF_TIP  # 提示用到的图标
                            )
                self.nid = nid
                win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
            def OnDestroy(self, hwnd, msg, wparam, lparam):
                nid = (self.hwnd, 0)
                win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
                win32gui.PostQuitMessage(0)  # Terminate the app.
    
        def show_msg(title,msg):
    	    t = TestTaskbarIcon()
    	    t.showMsg(title, msg)
        show_msg('None','None')

    else:
        return 'error'
