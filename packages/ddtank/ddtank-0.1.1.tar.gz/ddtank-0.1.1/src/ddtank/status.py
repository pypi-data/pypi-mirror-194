import win32gui
import win32api
import win32con
import win32ui
import cv2
import numpy as np
import string
import time
import ddtcv

from threading import Thread
from ctypes import windll
from ddtank import stop_thread

VkKeyScanA = windll.user32.VkKeyScanA

keycode_dict = {
    "back": 0x08,
    "tab": 0x09,
    "enter": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "alt": 0x12,
    "pause": 0x13,
    "capital": 0x14,
    "esc": 0x1B,
    "space": 0x20,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "print": 0x2A,
    "snapshot": 0x2C,
    "insert": 0x2D,
    "delete": 0x2E,
    "lwin": 0x5B,
    "rwin": 0x5C,
    "numpad0": 0x60,
    "numpad1": 0x61,
    "numpad2": 0x62,
    "numpad3": 0x63,
    "numpad4": 0x64,
    "numpad5": 0x65,
    "numpad6": 0x66,
    "numpad7": 0x67,
    "numpad8": 0x68,
    "numpad9": 0x69,
    "multiply": 0x6A,
    "add": 0x6B,
    "separator": 0x6C,
    "subtract": 0x6D,
    "decimal": 0x6E,
    "divide": 0x6F,
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "f5": 0x74,
    "f6": 0x75,
    "f7": 0x76,
    "f8": 0x77,
    "f9": 0x78,
    "f10": 0x79,
    "f11": 0x7A,
    "f12": 0x7B,
    "numlock": 0x90,
    "scroll": 0x91,
    "lshift": 0xA0,
    "rshift": 0xA1,
    "lcontrol": 0xA2,
    "rcontrol": 0xA3,
    "lmenu": 0xA4,
    "rmenu": 0XA5
}

def get_keycode(key: str) -> int:
    """
    获取按键的键值
    :param key: 按键的名称
    :return: 按键的键值，如果没有找到该键键值，返回-1
    """
    if len(key) == 1 and key in string.printable:
        return VkKeyScanA(ord(key)) & 0xff
    elif key in keycode_dict.keys():
        return keycode_dict[key]
    else:
        return -1


class Status:
    def __init__(self, hwnd: int, title: str = None):
        self.handle = hwnd
        if title:
            self.name = title
        else:
            self.name = f'{hwnd}'

        self.thread = None

        self.capture = None
        self.image_path = './image'

        self.wind = None
        self.angle = None
        self.map_pos = None
        self.box_pos = None
        self.box_width = None
        self.blues = None
        self.cur_pos = None
        self.reds = None
        self.circle = None

    def __repr__(self) -> str:
        return self.name

    def task(self):
        pass

    def start(self):
        self.thread = Thread(target=self.task)
        self.thread.setDaemon(True)
        self.thread.start()
        return self.thread.ident

    def stop(self):
        stop_thread(self.thread)

    @staticmethod
    def __sleep(period: int):
        time.sleep(period / 1000)

    @staticmethod
    def __delay(period: int):
        start = time.perf_counter()
        while (time.perf_counter() - start) * 1000 < period:
            continue

    def __click(self, pos: tuple):
        long_position = win32api.MAKELONG(*pos)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)

    def __press(self, key: str, period: int = None):
        keycode = get_keycode(key)
        win32api.SendMessage(self.handle, win32con.WM_KEYDOWN, keycode, 0)
        if period:
            self.__delay(period)
        win32api.SendMessage(self.handle, win32con.WM_KEYUP, keycode, 0)

    def __capture(self, position: tuple = (0, 0, 1000, 600), r: bool = False):
        """
        对角色游戏窗口执行截图操作，默认将截图存储在self.capture而不是返回一个图片，如果需要返回值，请设置r = True
        注意，对于某些浏览器或登陆器，此方法可能无法正确获取截图(表现为全黑色截图)
        因此，您需要自己来选择合适的登陆器以正确运行脚本
        :param position: 指明截图位置的元组，分别为左上角x坐标、左上角y坐标、宽度、高度，默认为(0, 0, 1000, 600)即整个窗口
        :param r: 是否返回图片，默认为False
        """
        x, y, w, h = position
        hwnd_dc = win32gui.GetWindowDC(self.handle)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bit_map = win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bit_map)
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, (x, y), win32con.SRCCOPY)
        signed_ints_array = save_bit_map.GetBitmapBits(True)
        img = np.frombuffer(signed_ints_array, dtype="uint8")
        img.shape = (h, w, 4)
        win32gui.DeleteObject(save_bit_map.GetHandle())
        mfc_dc.DeleteDC()
        save_dc.DeleteDC()
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        if r:
            return img
        self.capture = img

    def activate(self):
        win32api.PostMessage(self.handle, win32con.WM_SETFOCUS, 0, 0)

    def find(self, method: str = 'point', **kwargs):
        if method in ('point', 'p'):
            pos = kwargs['pos']
            self.__capture()
            return self.capture[pos[1], pos[0]][::-1]
        elif method in ('image', 'i'):
            part = kwargs['part']
            img = kwargs['img']
            self.__capture()
            template_image = cv2.imread(self.image_path + '/' + img + '.png', 0)
            x, y, w, h = part
            image = cv2.cvtColor(self.capture, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(image[y:y+h, x:x+w], template_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if max_val >= 0.9:
                w, h = template_image.shape[::-1]
                return int(max_loc[0] + w / 2), int(max_loc[1] + h / 2)
            else:
                return None

    def click(self, method: str = 'normal', **kwargs):
        def convert(hex_str: str):
            rgb_list = []
            for i in range(3):
                rgb_list.append(int(hex_str[i*2: i*2+2], 16))
            return tuple(rgb_list)
        if method in ('normal', 'n'):
            pos = kwargs['pos']
            self.__click(pos=pos)
        elif method in ('find', 'f'):
            pos = kwargs['pos']
            if type(kwargs['rgb']) == str:
                kwargs['rgb'] = convert(kwargs['rgb'])
            if self.find('point', pos=pos) == kwargs['rgb']:
                self.__click(pos=pos)
        elif method in ('rfind', 'rf'):
            pos = kwargs['pos']
            if type(kwargs['rgb']) == str:
                kwargs['rgb'] = convert(kwargs['rgb'])
            while True:
                if self.find('point', pos=pos) == kwargs['rgb']:
                    self.__click(pos=pos)
                    break
                else:
                    if 'else' in kwargs.keys():
                        kwargs['else']()
                    elif 'period' in kwargs.keys():
                        self.__sleep(kwargs['period'])
                    else:
                        self.__sleep(1000)
        elif method in ('find_image', 'fi'):
            img = kwargs['img']
            if 'part' in kwargs.keys():
                part = kwargs['part']
            else:
                part = (0, 0, 1000, 600)
            pos = self.find('image', img=img, part=part)
            if pos:
                self.__click(pos)
        elif method in ('rfind_image', 'rfi'):
            img = kwargs['img']
            if 'part' in kwargs.keys():
                part = kwargs['part']
            else:
                part = (0, 0, 1000, 600)
            while True:
                pos = self.find('image', img=img, part=part)
                if pos:
                    self.__click(pos)
                    break
                else:
                    if 'period' in kwargs.keys():
                        self.__sleep(kwargs['period'])
                    else:
                        self.__sleep(1000)

    def press(self, key_series):
        for key in key_series:
            if type(key) == str:
                self.__press(key)
            elif type(key) == int:
                self.__sleep(key)
            elif type(key) == tuple:
                self.__press(*key)

    def read(self, is_circle: bool = False):
        def read_wind():
            image = self.capture
            b, g, r = image.item(21, 468, 0), image.item(21, 468, 1), image.item(21, 468, 2)
            if b == 252 and g == r and g > 240 and r > 240:
                face = 1
            else:
                face = -1
            return ddtcv.Wind(self.capture) * face

        def read_angle():
            return ddtcv.Angle(self.capture)

        def read_small_map():
            return np.argwhere(np.all(self.capture[1, 750:] == [160, 160, 160], axis=-1))[0, 0] + 742

        def read_white_box():
            img = np.where(np.any(self.capture[24:120, self.map_pos:998] != [153, 153, 153], axis=-1), 0, 255).astype('uint8')
            contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if w > 30:
                    white_box_pos = (x, y)
                    white_box_width = w / 10
                    return white_box_pos, white_box_width
            return None

        def read_blue():
            blue_list = []
            blue_triangle = None
            img = np.where(np.any(self.capture[24:120, self.map_pos:998] != [204, 51, 0], axis=-1), 0, 255).astype('uint8')
            contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h > 3:
                    blue = (x, y)
                    # blue = (x, y, w)
                    blue_list.append(blue)
                elif h == 3 and w == 5:
                    blue_triangle = (x, y)
            return blue_list, blue_triangle

        def read_red():
            red_list = []
            img = np.where(np.any(self.capture[24:120, self.map_pos:998] != [0, 0, 255], axis=-1), 0, 255).astype('uint8')
            contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if h > 3:
                    red = (x, y)
                    # red = (x, y, w)
                    red_list.append(red)
            return red_list

        def read_circle():
            def get_circle():
                capture_1 = self.__capture(position=(self.map_pos, 24, 998 - self.map_pos, 120 - 24), r=True)
                capture_1 = cv2.cvtColor(capture_1, cv2.COLOR_BGR2GRAY)
                self.__sleep(30)
                capture_2 = self.__capture(position=(self.map_pos, 24, 998 - self.map_pos, 120 - 24), r=True)
                capture_2 = cv2.cvtColor(capture_2, cv2.COLOR_BGR2GRAY)
                image = np.where(capture_1 == capture_2, 255, 0).astype('uint8')
                contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) < 2:
                    return None
                if len(contours) > 4:
                    return None
                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if 10 < w < 50 or 10 < h < 50:
                        self_x = int(x + w / 2)
                        self_y = int(y + h / 2)
                        return self_x, self_y
            while True:
                circle_pos = get_circle()
                if circle_pos:
                    return circle_pos
                else:
                    self.__sleep(100)

        self.__capture()
        self.wind = read_wind()
        self.angle = read_angle()
        self.map_pos = read_small_map()
        self.box_pos, self.box_width = read_white_box()
        self.blues, self.cur_pos = read_blue()
        self.reds = read_red()
        if is_circle:
            self.circle = read_circle()

    def shot(self, shot_angle, shot_strength: int, shot_item: tuple = None):
        """
        综合模拟发射炮弹操作
        注意，使用此方法前需要先执行self.read方法，否则信息得不到及时更新
        :param shot_angle: 发射的角度，若传递一个元组则执行变角操作
        :param shot_strength: 发射的力度
        :param shot_item: 使用的道具按键，多个道具之间用','分隔
        :return: 无返回值
        """
        def change_angle(current_angle: int, target_angle: int):
            """
            调整角度至指定角度
            :param current_angle: 当前角度
            :param target_angle: 目标角度
            :return: 无返回值
            """
            if current_angle == target_angle:
                return
            elif current_angle < target_angle:
                for i in range(target_angle - current_angle):
                    self.__press('W')
            elif current_angle > target_angle:
                for i in range(current_angle - target_angle):
                    self.__press('S')

        def press_shot(strength: int):
            """
            高精度模拟力度操作
            :param strength: 模拟的力度数值，为0-100之间的整数
            :return: 无返回值
            """
            if strength == 0:
                self.__press('space', period=0)
            x_pos, y_pos = 149 + int(strength * 5), 590
            if (x_pos + 1) % 5 == 0:
                x_pos += 1
            if strength == 100:
                x_pos = 647

            win32api.PostMessage(self.handle, win32con.WM_KEYDOWN, 32, 0)
            self.__delay(100)
            pixel = self.capture()[y_pos, x_pos]
            while True:
                if (self.capture()[y_pos, x_pos] != pixel).any():
                    win32api.PostMessage(self.handle, win32con.WM_KEYUP, 32, 0)
                    break

        if shot_item:
            self.press(shot_item)
        if type(shot_angle) == int:
            change_angle(self.angle, shot_angle)
            press_shot(shot_strength)
        elif type(shot_angle) == tuple or list:
            change_angle(self.angle, shot_angle[0])
            press_shot(shot_strength)
            for i in range(1, len(shot_angle)):
                self.__delay(800)
                change_angle(shot_angle[i-1], shot_angle[i])

    def move(self, move_face: str, move_period: int, reverse_face: bool = False):
        """
        角色移动
        :param move_face: 移动朝向
        :param move_period: 移动时间(毫秒)
        :param reverse_face: 移动完后是否逆转朝向
        :return: 无返回值
        """
        if move_face in ['left', 'l', '左']:
            self.__press('A')
            self.__press('A', period=move_period)
            if reverse_face:
                self.__press('D')
        elif move_face in ['right', 'r', '右']:
            self.__press('D')
            self.__press('D', period=move_period)
            if reverse_face:
                self.__press('A')





