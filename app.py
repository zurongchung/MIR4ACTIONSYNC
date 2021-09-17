import function_lab


if __name__ == "__main__":
    # function_lab.list_window()
    hwnd = function_lab.get_active()
    # hwnd = function_lab.find_window()
    # function_lab.send_actions(hwnd)
    # size = function_lab.get_window_rect(hwnd)
    # size = function_lab.get_resolution()
    # print(size)
    function_lab.m_move(120, 240)
    # function_lab.r_click()