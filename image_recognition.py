import cv2
import pytesseract
from pytesseract import Output
import pyautogui
import pygetwindow as gw
import os

# 指定Tesseract的安装路径
# 例如，Windows上可能是'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Linux上可能是'/usr/bin/tesseract'
# macOS上可能是'/usr/local/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = r'<YOUR_TESSERACT_PATH>'


def find_icon_in_window(window_title, icon_image_path):
    """
    在指定窗口中查找图标，并返回最下面的图标中心的坐标。

    参数:
    - window_title: 窗口的标题
    - icon_image_path: 图标图片的路径

    返回值:
    - 如果成功找到图标，返回最下面的图标中心的坐标（x, y）
    - 如果没有找到图标，或者窗口不可见或已最小化，返回0
    """
    try:
        # 获取窗口
        window = gw.getWindowsWithTitle(window_title)[0]
    except IndexError:
        print("没有找到标题为 '{}' 的窗口".format(window_title))
        return 0

    # 检查窗口是否最小化或不可见
    if window.isMinimized:
        print("窗口 '{}' 已最小化".format(window_title))
        return 0
    if not window.isVisible:
        print("窗口 '{}' 不可见".format(window_title))
        return 0

    # 在窗口中查找所有匹配的图标
    icon_positions = list(pyautogui.locateAllOnScreen(icon_image_path, region=(window.left, window.top, window.width, window.height)))

    if icon_positions:
        # 选择最后一个图标
        icon_position = icon_positions[-1]

        # 计算图标中心的坐标
        x = icon_position[0] + icon_position[2] / 2
        y = icon_position[1] + icon_position[3] / 2

        return x, y
    else:
        print("在窗口 '{}' 中没有找到图标 '{}'".format(window_title, os.path.basename(icon_image_path)))
        return 0

def capture_screen(region=None):
    """
    捕获屏幕的指定区域。
    如果没有指定区域，就捕获整个屏幕。

    参数:
    - region: (x, y, width, height)

    返回:
    - 截图的图像对象
    """
    return pyautogui.screenshot(region=region)

def find_room_names(image, pattern):
    """
    使用OCR在给定的图像中查找匹配特定模式的房间名。

    参数:
    - image: 要进行OCR的图像
    - pattern: 房间名的匹配模式（正则表达式）

    返回:
    - 匹配的房间名及其位置的列表
    """
    # 将图像转换为灰度图，以提高OCR的准确率
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用Tesseract进行OCR
    ocr_result = pytesseract.image_to_data(gray, output_type=Output.DICT)

    matched_rooms = []
    num_items = len(ocr_result['text'])
    for i in range(num_items):
        text = ocr_result['text'][i].strip()
        if pattern in text:
            x, y, w, h = ocr_result['left'][i], ocr_result['top'][i], ocr_result['width'][i], ocr_result['height'][i]
            matched_rooms.append((text, (x, y, x+w, y+h)))

    return matched_rooms


# 请替换<YOUR_TESSERACT_PATH>为你的Tesseract-OCR安装路径。这段代码提供了基础的屏幕捕获和文本识别功能。
# 你需要根据实际情况调整find_room_names函数中的pattern参数，以匹配你感兴趣的房间名。