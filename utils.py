import os
import sys
import cv2
import numpy as np
import base64

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def img_to_base64(img):
    if img is None: return None
    success, buffer = cv2.imencode('.png', img)
    if success: return base64.b64encode(buffer).decode('utf-8')
    return None

def base64_to_img(b64_str, is_gray=True):
    if not b64_str: return None
    img_data = base64.b64decode(b64_str)
    nparr = np.frombuffer(img_data, np.uint8)
    mode = cv2.IMREAD_GRAYSCALE if is_gray else cv2.IMREAD_COLOR
    return cv2.imdecode(nparr, mode)