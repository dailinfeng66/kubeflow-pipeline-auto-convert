# 导入模块
import win32gui

if __name__ == '__main__':
    win = win32gui.FindWindow(None, u'李凯伦')
    # 将窗口调到前台
    win32gui.ShowWindow(win, win32con.SW_SHOWNORMAL)
    # 得到窗口左上角右下角位置，如(954, 299, 1470, 798)
    winRect = win32gui.GetWindowRect(win)
    # 将剪贴板消息到窗体
    win32gui.SendMessage(win, 258, 22, 2080193)
    win32gui.SendMessage(win, 770, 0, 0)
    # 模拟按下回车键
    win32gui.SendMessage(win, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(win, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
