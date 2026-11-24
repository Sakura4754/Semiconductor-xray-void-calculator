"""Run with python -m unittest discover -s tests on a desktop with Tk, Chrome
and the Python playwright package. The page loads its normal OpenCV.js runtime.
"""
import base64
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import tkinter as tk
import unittest
from unittest.mock import patch

import cv2
import numpy as np
from playwright.sync_api import sync_playwright

from app import XrayVoidDetector
from utils import auto_void_threshold, bilateral_filter, img_to_base64


class WebParityTest(unittest.TestCase):
    def test_project_and_detection(self):
        root = tk.Tk()
        self.addCleanup(root.destroy)
        desktop = XrayVoidDetector(root)
        root.withdraw()
        y, x = np.mgrid[:104, :281]
        raw = (150 + x % 33 + y % 9).astype(np.uint8)
        cv2.circle(raw, (95, 48), 10, 60, -1)
        cv2.circle(raw, (210, 37), 6, 50, -1)
        manual = np.zeros_like(raw)
        manual[55, 12:14] = 255
        cv2.circle(manual, (95, 48), 3, 128, -1)
        data = dict(original_img=img_to_base64(raw), user_mask=img_to_base64(manual),
                    roi_pts=[[6, 9], [235, 90]], destripe=5, sharpen=.68, gamma=.879,
                    alpha=1.197, bh_size=32.2, morph=4, area=12, fill_gap=2, circ=.35,
                    solidify=False, show_void_labels=True, tool_mode="FILL")

        with TemporaryDirectory() as tmp, sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome")
            page = browser.new_page()
            page.goto((Path(__file__).resolve().parents[1] / "VoidCal.html").as_uri())
            page.wait_for_function("cvReady")
            page.evaluate("window.showSaveFilePicker = undefined")
            path = Path(tmp) / "desktop.vod"
            path.write_text(json.dumps(data), encoding="utf-8")

            def desktop_load(source):
                with patch("app.filedialog.askopenfilename", return_value=str(source)), \
                     patch("app.messagebox.showerror", side_effect=AssertionError):
                    desktop.load_project()

            def compare():
                for field, reference in [("processed", desktop.processed_img),
                                         ("composite", desktop.current_composite_mask)]:
                    encoded = page.evaluate("field => encodeGray(doc[field])", field)
                    png = np.frombuffer(base64.b64decode(encoded), np.uint8)
                    np.testing.assert_array_equal(cv2.imdecode(png, cv2.IMREAD_GRAYSCALE), reference)
                self.assertEqual(page.evaluate("rate"), desktop.current_void_rate)
                self.assertEqual(page.evaluate("labels.map(labelText)"),
                                 [text for text, _, _ in desktop.current_void_labels])

            desktop_load(path)
            page.locator("#projectInput").set_input_files(path)
            page.wait_for_function("statusKey === 'status_load_success'")
            self.assertTrue(page.locator("#edit").is_visible())
            compare()

            page.locator('[data-tab="void"]').click()
            page.locator("#optimize").click()
            desktop.auto_heuristic_search()
            self.assertEqual(page.evaluate("value('bh_thresh')"), desktop.bh_thresh_slider.get())
            controls = [desktop.morph_slider.get(), desktop.area_slider.get(), desktop.circ_slider.get()]
            self.assertEqual(controls, [4, 12, .35])
            self.assertEqual(page.evaluate("['morph','area','circ'].map(value)"), controls)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (33, 33))
            full = cv2.morphologyEx(desktop.processed_img, cv2.MORPH_BLACKHAT, kernel)
            sample = bilateral_filter(full, 9, 27, 27)[9:90, 6:235]
            self.assertEqual(desktop.bh_thresh_slider.get(), auto_void_threshold(sample))
            compare()
            page.locator("#accumulate").click()
            desktop.accumulate_mask()

            with page.expect_download() as download:
                page.keyboard.press("Control+s")
            saved = Path(tmp) / "web.vod"
            download.value.save_as(saved)
            desktop_load(saved)
            np.testing.assert_array_equal(desktop.user_mask, manual)
            np.testing.assert_array_equal(desktop.original_img, raw)
            self.assertIsNotNone(desktop.accumulated_base_mask)
            compare()

            with page.expect_download() as download:
                page.keyboard.press("Control+e")
            jpeg = np.frombuffer(Path(download.value.path()).read_bytes(), np.uint8)
            self.assertEqual(cv2.imdecode(jpeg, cv2.IMREAD_COLOR).shape, (81, 229, 3))
            page.locator('[data-tab="edit"]').click()
            page.locator("#clear").click()
            page.wait_for_function("!roi && rate === 0 && !doc.accumulated && !doc.manual.some(Boolean)")
            browser.close()

    def test_empty_background_and_ring(self):
        root = tk.Tk()
        self.addCleanup(root.destroy)
        desktop = XrayVoidDetector(root)
        root.withdraw()
        y, x = np.mgrid[:224, :256]
        gray = 155 + .09 * x + .035 * y + np.random.default_rng(0).normal(0, 2, x.shape)
        blank = np.rint(gray).astype(np.uint8)
        ring = np.full((72, 92), 180, np.uint8)
        cv2.circle(ring, (45, 36), 16, 55, -1)
        cv2.circle(ring, (45, 36), 8, 180, -1)
        ring[36, 45] = 55  # An independently rejected island inside the hole.

        with TemporaryDirectory() as tmp, sync_playwright() as pw:
            browser = pw.chromium.launch(channel="chrome")
            page = browser.new_page()
            page.goto((Path(__file__).resolve().parents[1] / "VoidCal.html").as_uri())
            page.wait_for_function("cvReady")
            for name, raw, options in [
                ("blank", blank, dict(roi_pts=[[16, 16], [240, 208]])),
                ("ring", ring, dict(use_clahe=False, morph=0, solidify=False, area=3)),
            ]:
                with self.subTest(name=name):
                    path = Path(tmp) / (name + ".vod")
                    path.write_text(json.dumps(dict(original_img=img_to_base64(raw), **options)))
                    with patch("app.filedialog.askopenfilename", return_value=str(path)), \
                         patch("app.messagebox.showerror", side_effect=AssertionError):
                        desktop.load_project()
                    page.locator("#projectInput").set_input_files(path)
                    page.wait_for_function("n => filename === n", arg=path.name)
                    page.locator('[data-tab="void"]').click()
                    page.locator("#optimize").click()
                    desktop.auto_heuristic_search()
                    self.assertEqual(page.evaluate("value('bh_thresh')"), desktop.bh_thresh_slider.get())
                    got = np.array(page.evaluate("Array.from(doc.composite)")).reshape(raw.shape)
                    np.testing.assert_array_equal(got, desktop.current_composite_mask)
                    if name == "blank":
                        self.assertFalse(got[16:208, 16:240].any())
                    else:
                        expected = np.where(raw == 55, 255, 0).astype(np.uint8)
                        expected[36, 45] = 0
                        np.testing.assert_array_equal(got, expected)
                        page.locator('[data-tab="edit"]').click()
                        page.locator("#solidify").check()
                        page.evaluate("flush()")
                        desktop.solidify_var.set(True)
                        cv2.circle(expected, (45, 36), 16, 255, -1)
                        np.testing.assert_array_equal(desktop.get_composite_mask(), expected)
                        got = np.array(page.evaluate("Array.from(doc.composite)")).reshape(raw.shape)
                        np.testing.assert_array_equal(got, expected)
            browser.close()
