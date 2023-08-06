import ddtank


def get_game_window_information() -> list:
    """
    获取所有游戏窗口信息
    :return: 由游戏窗口信息字典组成的列表
        platform: 代理平台
        service: 服务器
        name: 账号或备注
        index: 窗口编号
        hwnd: 游戏窗口句柄
    """
    windows_list, info_dict_list = [], []
    ddtank.win32gui.EnumWindows(lambda w, param: param.append(w), windows_list)
    pattern_for_36 = ddtank.re.compile(r'\[(.*)-(.*)-(.*)]\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)')
    for window in windows_list:
        title = ddtank.win32gui.GetWindowText(window)
        re_rst = pattern_for_36.search(title)
        if re_rst:
            rst = re_rst.groups()
            info_dict = {'platform': rst[0], 'service': int(rst[1]), 'name': rst[2], 'index': int(rst[3]), 'hwnd': int(rst[5])}
            info_dict_list.append(info_dict)
    return info_dict_list


def get_game_window_handle(title_pattern: str = r'.*') -> list:
    """
    获取所有游戏窗口句柄
    :param: 窗口标题匹配模式字符串，默认所有
    :return: 由游戏窗口句柄组成的列表
    """
    def get_all_child_window(parent):
        l = []
        ddtank.win32gui.EnumChildWindows(
            parent, lambda hwnd, param: param.append(hwnd), l)
        return l

    windows_list, hwnd_list = [], []
    ddtank.win32gui.EnumWindows(lambda w, param: param.append(w), windows_list)
    pattern_for_36 = ddtank.re.compile(r'\[(.*)-(.*)-(.*)]\|(.*)\|(.*)\|(.*)\|(.*)\|(.*)')
    if not title_pattern:
        title_pattern = pattern_for_36
    else:
        title_pattern = ddtank.re.compile(title_pattern)
    for window in windows_list:
        title = ddtank.win32gui.GetWindowText(window)
        re_rst = title_pattern.search(title)
        if re_rst:
            parent_title = re_rst.group()
            parent_hwnd = ddtank.win32gui.FindWindow(0, parent_title)
            child_hwnd_list = get_all_child_window(parent_hwnd)
            for child_hwnd in child_hwnd_list:
                class_name = ddtank.win32gui.GetClassName(child_hwnd)
                if class_name == 'MacromediaFlashPlayerActiveX':
                    shape = ddtank.win32gui.GetWindowRect(child_hwnd)
                    height = shape[3] - shape[1]
                    weight = shape[2] - shape[0]
                    if weight == 1000 and height == 600:
                        hwnd_list.append(child_hwnd)
    return hwnd_list


