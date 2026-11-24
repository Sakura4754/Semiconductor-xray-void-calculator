import os
import sys
import cv2
import numpy as np
import base64

def auto_void_threshold(sample):
    otsu, _ = cv2.threshold(sample, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # Estimate noise from the lower-response class. Use lower medians for
    # discrete grayscale values, matching the browser histogram.
    background = sample[sample <= otsu]
    if not background.size:
        return max(1, int(otsu))
    rank = (background.size - 1) // 2
    center = int(np.partition(background, rank)[rank])
    deviations = np.abs(background.astype(np.int16) - center)
    mad = int(np.partition(deviations, rank)[rank])
    return min(255, max(1, int(otsu), int(center + 5 * 1.4826 * mad)))


def ellipse_blackhat(image, size):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    if size < 31:
        return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)

    # Each horizontal band of the exact OpenCV footprint has a constant width.
    # From the poles toward the center the runs only grow, so expand the
    # previous horizontal extremum by the width difference at each step.
    radius = size // 2
    h = image.shape[0]
    pad = min(radius, h - 1)
    bands = []
    for dy in range(pad, -1, -1):
        width = int(np.sum(kernel[radius + dy]))
        if bands and bands[-1][0] == width:
            bands[-1][1] = dy
        else:
            bands.append([width, dy, dy])

    def extrema(src, operation, merge, neutral):
        rows = cv2.copyMakeBorder(src, pad, pad, 0, 0, cv2.BORDER_REPLICATE)
        out = np.full_like(src, neutral)
        previous = 1
        for width, first, last in bands:
            if width > previous:
                expand = np.ones((1, width - previous + 1), np.uint8)
                operation(rows, expand, dst=rows)
            values = rows
            if last > first:
                vertical = np.ones((last - first + 1, 1), np.uint8)
                values = operation(rows, vertical, anchor=(0, 0))
            merge(out, values[pad + first:pad + first + h], out=out)
            if last:
                merge(out, values[pad - last:pad - last + h], out=out)
            previous = width
        return out

    high = extrema(image, cv2.dilate, np.maximum, 0)
    closed = extrema(high, cv2.erode, np.minimum, 255)
    return cv2.subtract(closed, image)


def void_regions(feature, threshold):
    _, mask = cv2.threshold(feature, threshold, 255, cv2.THRESH_BINARY)
    count, ids = cv2.connectedComponents(mask, connectivity=8)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    areas = np.zeros(count)
    circularities = np.zeros(count)
    for i, contour in enumerate(contours):
        if hierarchy[0, i, 3] >= 0: continue
        x, y = contour[0, 0]
        label = ids[y, x]
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        areas[label] = area
        if perimeter:
            circularities[label] = 4 * np.pi * area / perimeter ** 2
    return ids, areas, circularities


def bilateral_filter(image, diameter, sigma_color, sigma_space):
    # Use the same OpenCV filter as the WebAssembly build. IPP's 8-bit
    # rounding can change threshold crossings after contrast enhancement.
    ipp = getattr(cv2, "ipp", None)
    use_ipp = ipp is not None and ipp.useIPP()
    if use_ipp:
        ipp.setUseIPP(False)
    try:
        return cv2.bilateralFilter(image, diameter, sigma_color, sigma_space)
    finally:
        if use_ipp:
            ipp.setUseIPP(True)

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