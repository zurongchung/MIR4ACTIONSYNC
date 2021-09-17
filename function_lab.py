import win32gui, win32api
import win32con
import time

'''
    Find the multiple windows of an app from a list of all running application windows
'''
def list_window():
    def p(hWnd, extra):
        _str_title = win32gui.GetWindowText(hWnd)
        # print(_str_title + ' : ' + str(hWnd))
        if _str_title.__contains__("BlueStacks"):
            print(_str_title + ' : ' + str(hWnd))
    win32gui.EnumWindows(p, 0)

'''
    Find a single app window by giving the window's title 
'''
def find_window() -> int:
    _hwnd = win32gui.FindWindow(None, 'MIR4_1')
    print(win32gui.GetWindowText(_hwnd))
    return _hwnd

    # _hwnd = win32gui.FindWindow('Notepad', 'test_doc.txt - Notepad')
    # _hwndChild = win32gui.GetWindow(_hwnd, win32con.GW_CHILD)
    # return _hwndChild

    # _hwndParent = win32gui.GetParent(_hwnd)
    # _str_title = win32gui.GetWindowText(_hwndParent)
    # print(_str_title + ' : ' + str(_hwndParent))

'''
    get active window's title and id
'''
def get_active():
    time.sleep(2)
    _hwnd = win32gui.GetForegroundWindow()
    print(_hwnd)
    print(win32gui.GetWindowText(_hwnd))
    return _hwnd

'''
    send one or a series of [ keyboard and or mouse actions ]
    to one or multiple windows
'''
def send_actions(_hwnd):
    # W_key
    # _action = 0x57
    # P_key
    _action = 0x50
    time.sleep(2)
    win32api.PostMessage(_hwnd, win32con.WM_KEYDOWN, _action, 0)
    _ret_msg = win32api.PostMessage(_hwnd, win32con.WM_CHAR, _action, 0)
    win32api.PostMessage(_hwnd, win32con.WM_KEYUP, _action, 0)
    # print('sent: ' + str(_action))
    # print(_ret_msg)

'''
    get window size
'''
def get_window_rect(_hwnd) -> tuple:
    l, t, r, b = win32gui.GetWindowRect(_hwnd)
    w = r - l
    h = b - t
    return (w, h)

'''
    get screen resolution
'''
def get_resolution() -> tuple:
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    return (w, h)

# mouse left click at poisition
def l_click(_x, _y):
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN, _x, _y)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP, _x, _y)

# mouse right click at position
def r_click(_x, _y):
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTDOWN, _x, _y)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_RIGHTUP, _x, _y)

# mouse left down at position
def l_down(_x, _y):
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTDOWN, _x, _y)

# mouse left up at position
def l_up(_x, _y):
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_LEFTUP, _x, _y)

# mouse move
def m_move(_dx, _dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, _dx, _dy)

# mouse click and move