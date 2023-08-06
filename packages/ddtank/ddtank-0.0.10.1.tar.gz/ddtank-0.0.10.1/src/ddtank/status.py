from typing import Union
import ddtank

keycode_dict = {
    "back": 0x08,
    "tab": 0x09,
    "enter": 0x0D,
    "shift": 0x10,
    "control": 0x11,
    "menu": 0x12,
    "pause": 0x13,
    "capital": 0x14,
    "escape": 0x1B,
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
    if len(key) == 1 and key in ddtank.string.printable:
        return ddtank.VkKeyScanA(ord(key)) & 0xff
    elif key in keycode_dict.keys():
        return keycode_dict[key]
    else:
        return -1


class Status:
    def __init__(self, info: Union[dict, int]):
        if type(info) == dict:
            self.platform = info['platform']
            self.service = info['service']
            self.name = info['name']
            self.index = info['index']
            self.hwnd = info['hwnd']
        elif type(info) == int:
            self.hwnd = info
            self.name = f'窗口句柄{self.hwnd}'

        self.image_path = None
        self.model_path = None
        self.load_image()
        self.load_model()

    def __repr__(self) -> str:
        return self.name

    # 重写方法
    def task(self):
        pass

    # 加载方法
    def load_image(self, path: str = './image') -> bool:
        """
        加载图片资源，图片必须为png格式
        :param path: 图片资源文件夹的路径
        :return: 文件夹存在返回True，否则返回False
        """
        if ddtank.os.path.exists(path):
            self.image_path = path
            # for image_name in ddtank.os.listdir(self.image_path):
            #     if image_name.endswith('.png'):
            #         image = ddtank.cv2.imread(self.image_path + '/' + image_name)
            #         exec(f'self.{image_name.strip(".png")} = image')
            return True
        return False

    def load_model(self, path: str = './model') -> bool:
        """
        加载识别模型
        :param path: 模型文件夹的路径
        :return: 文件夹存在返回True，否则返回False
        """
        if ddtank.os.path.exists(path):
            self.model_path = path
            return True
        return False

    # 基本方法
    @staticmethod
    def sleep(period: int, precise: bool = True):
        """
        角色等待一段时间
        :param period: 按键间隔时长(ms)
        :param precise: 是否使用高精度计时，默认为是
        :return: 无返回值
        """
        if precise:
            time_start = ddtank.time.perf_counter()
            while ((ddtank.time.perf_counter() - time_start) * 1000) < period:
                continue
        else:
            ddtank.time.sleep(period / 1000)

    @staticmethod
    def aim(angle: int, wind: float, distance_x: float, distance_y: float) -> float:
        """
        根据给定条件，计算击中目标所需的力度
        :param angle: 角度
        :param wind: 风力，顺风为正，逆风为负
        :param distance_x: 横向距离，单位为屏距
        :param distance_y: 纵向距离，单位为屏距
        :return: 拟合得到的力度结果
        """
        if angle > 90:
            angle = 180 - angle
        r, w, g = [0.90289815, 6.33592869, -184.11666458]
        shot_angel = angle
        position_angel = ddtank.math.atan(distance_y / distance_x)
        position_angel = position_angel * 180 / ddtank.math.pi
        x_angel = shot_angel - position_angel
        y_angel = 90 - shot_angel + position_angel
        x_angel = x_angel * ddtank.math.pi / 180
        y_angel = y_angel * ddtank.math.pi / 180
        position_angel = position_angel * ddtank.math.pi / 180

        def solve(F):
            vx = ddtank.math.cos(x_angel) * F
            vy = ddtank.math.cos(y_angel) * F
            fx = ddtank.math.cos(position_angel) * w * wind + ddtank.math.sin(position_angel) * g
            fy = -ddtank.math.sin(position_angel) * w * wind + ddtank.math.cos(position_angel) * g

            def computePosition(v0, f, r, t):
                temp = f - r * v0
                ert = ddtank.np.power(ddtank.math.e, -r * t)
                right = temp * ert + f * r * t - temp
                return right / (r * r)

            def getTime(v0):
                solve_l = lambda t1: computePosition(v0, fy, r, t1)
                time = ddtank.fsolve(solve_l, [2])
                assert time[0] != 0
                return time[0]

            t = getTime(vy)
            return computePosition(vx, fx, r, t) - ddtank.math.sqrt(distance_x ** 2 + distance_y ** 2)

        f = ddtank.fsolve(solve, [100])
        if f[0] > 100:
            return 100.0
        elif f[0] < 0:
            return 0.0
        return f[0]

    def activate(self, period: int = 100):
        """
        激活角色游戏窗口
        :param period: 发送激活信息后的等待时长(ms)，默认为100ms
        :return: 无返回值
        """
        ddtank.win32api.PostMessage(self.hwnd, ddtank.win32con.WM_SETFOCUS, 0, 0)
        self.sleep(period)

    def click(self, coordinate_x: int, coordinate_y: int, period: int = 10) -> bool:
        """
        对角色模拟单击操作
        :param coordinate_x: 单击点的x坐标
        :param coordinate_y: 单击点的y坐标
        :param period: 按键间隔时长(ms)
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        if 0 <= coordinate_x <= 1000 and 0 <= coordinate_y <= 600:
            coordinate = ddtank.win32api.MAKELONG(coordinate_x, coordinate_y)
            ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_LBUTTONDOWN, ddtank.win32con.MK_LBUTTON,
                                        coordinate)
            self.sleep(period)
            ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_LBUTTONUP, ddtank.win32con.MK_LBUTTON, coordinate)
            return True
        else:
            return False

    def press(self, key_string: str, period: int = 10) -> bool:
        """
        对角色模拟按键操作，多个按键之间用','分隔，如'A, B, C'，将依次模拟按下A、B、C键
        :param key_string: 模拟按键的名称，多个按键之间用','分隔，允许加入空格
        :param period: 按键间隔时长(ms)
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        for key in key_string.split(','):
            key = key.strip()
            keycode = get_keycode(key)
            if keycode == -1:
                return False
            else:
                ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_KEYDOWN, keycode,
                                            (ddtank.win32api.MapVirtualKey(keycode, 0) << 16) | 1)
                self.sleep(period)
                ddtank.win32api.SendMessage(self.hwnd, ddtank.win32con.WM_KEYUP, keycode,
                                            (ddtank.win32api.MapVirtualKey(keycode, 0) << 16) | 0XC0000001)
        return True

    def capture(self, position: tuple = (0, 0, 1000, 600), save_capture: bool = False) -> ddtank.np.ndarray:
        """
        对角色游戏窗口执行截图操作
        :param position: 指明截图位置的元组，分别为左上角x坐标、左上角y坐标、宽度、高度，默认为(0, 0, 1000, 600)即整个窗口
        :param save_capture: 是否保存截图。默认保存图片的路径为: ./capture/capture.png
        :return: 返回cv2格式的图片
        """
        x, y, w, h = position
        hwnd_dc = ddtank.win32gui.GetWindowDC(self.hwnd)
        mfc_dc = ddtank.win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bit_map = ddtank.win32ui.CreateBitmap()
        save_bit_map.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bit_map)
        save_dc.BitBlt((0, 0), (w, h), mfc_dc, (x, y), ddtank.win32con.SRCCOPY)
        signed_ints_array = save_bit_map.GetBitmapBits(True)
        img = ddtank.np.frombuffer(signed_ints_array, dtype="uint8")
        img.shape = (h, w, 4)
        ddtank.win32gui.DeleteObject(save_bit_map.GetHandle())
        mfc_dc.DeleteDC()
        save_dc.DeleteDC()
        img = ddtank.cv2.cvtColor(img, ddtank.cv2.COLOR_RGBA2RGB)
        if save_capture:
            if not ddtank.os.path.exists('./capture'):
                ddtank.os.mkdir('./capture')
            ddtank.cv2.imwrite(f'./capture/{self.hwnd}.png', img)
        return img

    def ocr(self, model: str) -> Union[int, float, str, type(None)]:
        """
        文字识别功能，需要预先运行 self.load_model 函数
        :param model: 需要识别文字的类型，包括: ['angle']
        :return: 返回识别结果
        """
        assert self.model_path, '未加载识别模型！'
        ocr_list = ['angle', 'wind']
        if model not in ocr_list:
            return None
        elif model == 'angle':
            onnx_model_fp = self.model_path + '/angle/angle.onnx'
            character_dict_fp = self.model_path + '/angle/angle_dict.txt'

            image = self.capture()
            image = image[555:576, 27:71]
            input_image_shape = (3, 576 - 555, 71 - 27)  # 模型的输入维度：通道数，高度，宽度

            preprocess_func = ddtank.build_preprocess()  # 获取预处理函数
            postprocess_func = ddtank.build_postprocess(character_dict_fp)  # 获取后处理函数
            session = ddtank.load_onnx(onnx_model_fp)  # 加载模型

            norm_image = preprocess_func(image, input_image_shape)  # 进行数据预处理

            # 使用模型对预处理数据进行运算
            input_name = session.get_inputs()[0].name
            output = session.run([], {input_name: norm_image})

            # 将模型的输出进行后处理，得到识别结果
            res = postprocess_func(output)[0][0]
            return int(res)
        elif model == 'wind':
            onnx_model_fp = self.model_path + '/wind/wind.onnx'
            character_dict_fp = self.model_path + '/wind/wind_dict.txt'

            image = self.capture()
            b, g, r = image.item(21, 468, 0), image.item(21, 468, 1), image.item(21, 468, 2)
            if b == 252 and g == r and g > 240 and r > 240:
                face = 1
            else:
                face = -1

            image = image[17:48, 461:537]
            input_image_shape = (3, 48 - 17, 537 - 461)  # 模型的输入维度：通道数，高度，宽度

            preprocess_func = ddtank.build_preprocess()  # 获取预处理函数
            postprocess_func = ddtank.build_postprocess(character_dict_fp)  # 获取后处理函数
            session = ddtank.load_onnx(onnx_model_fp)  # 加载模型

            norm_image = preprocess_func(image, input_image_shape)  # 进行数据预处理

            # 使用模型对预处理数据进行运算
            input_name = session.get_inputs()[0].name
            output = session.run([], {input_name: norm_image})

            # 将模型的输出进行后处理，得到识别结果
            res = postprocess_func(output)[0][0]
            return float(res) * face

    def input(self, input_string: str):
        """
        对角色模拟输入操作
        :param input_string: 模拟输入的内容
        :return: 无返回值
        """
        input_char = [ord(c) for c in input_string]
        for char in input_char:
            ddtank.win32api.PostMessage(self.hwnd, ddtank.win32con.WM_CHAR, char, 0)

    # 条件识别
    def click_pixel(self, coordinate_x: int, coordinate_y: int, pixel: tuple, repeat: bool = True) -> bool:
        """
        当指定位置像素符合条件时，对角色模拟单击操作
        :param coordinate_x: 单击点的x坐标
        :param coordinate_y: 单击点的y坐标
        :param pixel: 指定点像素的RGB值
        :param repeat: 是否重复判断，默认为是
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        status_img = self.capture()
        pixel = pixel[::-1]
        while repeat:
            if (status_img[coordinate_y, coordinate_x] == pixel).all():
                self.click(coordinate_x, coordinate_y)
                return True
            status_img = self.capture()
        if (status_img[coordinate_y, coordinate_x] == pixel).all():
            self.click(coordinate_x, coordinate_y)
            return True
        return False

    def click_pixel_back(self, coordinate_x: int, coordinate_y: int, pixel_x: int, pixel_y: int, pixel: tuple,
                         period: int = 500) -> bool:
        """
        对角色模拟单击操作后等待一段时间，如果指定位置像素不符合条件时将继续模拟单击操作直到符合条件
        :param coordinate_x: 单击点的x坐标
        :param coordinate_y: 单击点的y坐标
        :param pixel_x: 检测点的x坐标
        :param pixel_y: 检测点的y坐标
        :param pixel: 检测点像素的RGB值
        :param period: 模拟单击操作后等待的时间(ms)
        :return: 返回布尔类型变量，代表模拟信息传递是否成功
        """
        pixel = pixel[::-1]
        self.click(coordinate_x, coordinate_y)
        self.sleep(period)
        status_img = self.capture()
        while True:
            if (status_img[pixel_y, pixel_x] == pixel).all():
                return True
            self.click(coordinate_x, coordinate_y)
            self.sleep(period)
            status_img = self.capture()

    def find_pixel(self, coordinate_x: int, coordinate_y: int, pixel: tuple, repeat: bool = True):
        """
        判断指定位置像素是否符合条件
        :param coordinate_x: 像素点的x坐标
        :param coordinate_y: 像素点的y坐标
        :param pixel: 指定点像素的RGB值
        :param repeat: 是否重复判断，默认为是
        :return: 返回布尔类型变量，代表指定位置像素是否符合条件
        """
        status_img = self.capture()
        pixel = pixel[::-1]
        while repeat:
            if (status_img[coordinate_y, coordinate_x] == pixel).all():
                return True
            status_img = self.capture()
        if (status_img[coordinate_y, coordinate_x] == pixel).all():
            return True
        return False

    def find_image(self, template_image_name: str, position: tuple = (0, 0, 1000, 600)) -> Union[tuple, type(None)]:
        """
        寻找指定图像位置，需要先调用load_image方法指定图片资源文件夹路径
        :param template_image_name: 所要寻找的图片
        :param position: 寻找图片的范围: (x1, y1, x2, y2)，默认为全部
        :return: 返回图片中心点坐标元组，若找不到图片则返回None
        """
        assert self.image_path is not None
        template_image = ddtank.cv2.imread(self.image_path + '/' + template_image_name + '.png', 0)
        x1, y1, x2, y2 = position
        image = self.capture()
        image = ddtank.cv2.cvtColor(image, ddtank.cv2.COLOR_BGR2GRAY)
        res = ddtank.cv2.matchTemplate(image[y1:y2, x1:x2], template_image, ddtank.cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = ddtank.cv2.minMaxLoc(res)
        if max_val >= 0.9:
            w, h = template_image.shape[::-1]
            return int(max_loc[0] + w / 2), int(max_loc[1] + h / 2)
        else:
            return None

    # 综合操作
    def press_shot(self, strength: int):
        """
        高精度模拟力度操作
        :param strength: 模拟的力度数值，为0-100之间的整数
        :return: 无返回值
        """
        if strength == 0:
            self.press('space', period=0)
        x_pos, y_pos = 149 + int(strength * 5), 590
        if (x_pos + 1) % 5 == 0:
            x_pos += 1
        if strength == 100:
            x_pos = 647

        # self.activate()

        ddtank.win32api.PostMessage(self.hwnd, ddtank.win32con.WM_KEYDOWN, 32, 0)
        self.sleep(100)
        pixel = self.capture()[y_pos, x_pos]
        while True:
            if (self.capture()[y_pos, x_pos] != pixel).any():
                ddtank.win32api.PostMessage(self.hwnd, ddtank.win32con.WM_KEYUP, 32, 0)
                break

    def change_angle(self, current_angle: int, target_angle: int):
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
                self.press('W', period=0)
        elif current_angle > target_angle:
            for i in range(current_angle - target_angle):
                self.press('S', period=0)

    # 综合识别
    def get_map_info(self) -> tuple:
        """
        获取小地图信息，返回白框位置与宽度、蓝色点位置
        :return: 返回信息元组: ((白框左下角x坐标，白框左下角y坐标，每距像素长度)，(蓝色点中心点x坐标，蓝色点中心点y坐标))
        """
        status_img = self.capture()

        white_box = (-1, -1, -1)
        blue_point = (-1, -1)

        small_map_left_x = ddtank.np.argwhere(ddtank.np.all(status_img[1, 750:] == [160, 160, 160], axis=-1))[
                               0, 0] + 742

        img_res = ddtank.np.where(ddtank.np.any(status_img[24:120, small_map_left_x:998] != [153, 153, 153], axis=-1),
                                  0, 255).astype('uint8')
        contours, hierarchy = ddtank.cv2.findContours(img_res, ddtank.cv2.RETR_TREE, ddtank.cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = ddtank.cv2.boundingRect(cnt)
            if w > 30:
                white_box = (x, y, w / 10)
                break

        img_res = ddtank.np.where(ddtank.np.any(status_img[24:120, small_map_left_x:998] != [204, 51, 0], axis=-1), 0,
                                  255).astype('uint8')
        contours, hierarchy = ddtank.cv2.findContours(img_res, ddtank.cv2.RETR_TREE, ddtank.cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = ddtank.cv2.boundingRect(cnt)
            if h > 2:
                blue_point = (int(x + w / 2), int(y + h / 2))
                break

        return white_box, blue_point

    # 顶级操作
    def shot(self, shot_angle: Union[int, tuple, list], shot_strength: int, shot_item: str = None):
        """
        综合模拟发射炮弹操作
        :param shot_angle: 发射的角度，若传递一个元组则执行变角操作
        :param shot_strength: 发射的力度
        :param shot_item: 使用的道具按键，多个道具之间用','分隔
        :return: 无返回值
        """
        if shot_item:
            self.press(shot_item)
        if type(shot_angle) == int:
            self.change_angle(self.ocr('angle'), shot_angle)
            self.press_shot(shot_strength)
        elif type(shot_angle) == tuple or list:
            self.change_angle(self.ocr('angle'), shot_angle[0])
            self.press_shot(shot_strength)
            for i in range(1, len(shot_angle)):
                self.sleep(800)
                self.change_angle(self.ocr('angle'), shot_angle[i])

    def move(self, move_face: str, move_period: int, reverse_face: bool = False):
        """
        角色移动
        :param move_face: 移动朝向
        :param move_period: 移动时间(毫秒)
        :param reverse_face: 移动完后是否逆转朝向
        :return: 无返回值
        """
        if move_face in ['left', 'l', '左']:
            self.press('A')
            self.press('A', period=move_period)
            if reverse_face:
                self.press('D')
        elif move_face in ['right', 'r', '右']:
            self.press('D')
            self.press('D', period=move_period)
            if reverse_face:
                self.press('A')
