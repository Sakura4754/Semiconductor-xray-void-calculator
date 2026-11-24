import json
from pathlib import Path
from tempfile import TemporaryDirectory
import threading
import time
import tkinter as tk
import unittest
from unittest.mock import patch

import cv2
import numpy as np
from playwright.sync_api import sync_playwright

from app import XrayVoidDetector
from utils import ellipse_blackhat, img_to_base64


class DetectionSliderTest(unittest.TestCase):
    def test_ellipse_matches_opencv_at_edges(self):
        rng = np.random.default_rng(19)
        for shape in [(1, 29), (35, 1), (16, 12), (73, 96)]:
            image = rng.integers(0, 256, shape, np.uint8)
            for size in [11, 31, 51, 91, 151, 201]:
                with self.subTest(shape=shape, size=size):
                    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
                    expected = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
                    np.testing.assert_array_equal(ellipse_blackhat(image, size), expected)

    def test_desktop_uses_latest_slider_values(self):
        root = tk.Tk()
        self.addCleanup(root.destroy)
        app = XrayVoidDetector(root)
        root.withdraw()
        app.original_img = np.random.default_rng(3).integers(0, 220, (100, 139), np.uint8)
        app.update_base()
        source = app.filter_features
        started, release = threading.Event(), threading.Event()
        sizes = []

        def slow_first(image, size, diameter, blackhat):
            sizes.append(size)
            if size == 91:
                started.set()
                release.wait(timeout=5)
            return source(image, size, diameter, blackhat)

        def pump_until(done):
            end = time.monotonic() + 5
            while not done() and time.monotonic() < end:
                root.update()
                time.sleep(.005)
            self.assertTrue(done())

        with patch.object(app, "filter_features", side_effect=slow_first):
            app.bh_size_slider.set(91)
            app.schedule_detection()
            try:
                pump_until(started.is_set)
                for size in [99, 107, 113]:
                    app.bh_size_slider.set(size)
                    app.schedule_detection()
                app.bh_thresh_slider.set(31)
            finally:
                release.set()
            pump_until(lambda: app.detection_timer is None)
            self.assertEqual(sizes, [91, 113])
            self.assertEqual(app.feature_size, 113)
            self.assertEqual(app.region_threshold, 31)
            # Locking immediately after a change must consume the new mask.
            app.bh_thresh_slider.set(255)
            app.schedule_detection()
            app.accumulate_mask()
            self.assertFalse(app.accumulated_base_mask.any())
            self.assertEqual(sizes, [91, 113])

    def test_browser_worker_and_project_switch(self):
        with sync_playwright() as pw, TemporaryDirectory() as tmp:
            browser = pw.chromium.launch(channel="chrome")
            page = browser.new_page()
            page.goto((Path(__file__).resolve().parents[1] / "VoidCal.html").as_uri())
            page.wait_for_function("cvReady")
            rng = np.random.default_rng(7)

            def load(name, kernel):
                image = rng.integers(0, 210, (131, 173), np.uint8)
                data = dict(original_img=img_to_base64(image), bh_size=kernel, morph=0,
                            use_clahe=False, roi_pts=[[5, 6], [170, 129]])
                path = Path(tmp) / name
                path.write_text(json.dumps(data))
                page.locator("#projectInput").set_input_files(path)
                page.wait_for_function("name => filename === name", arg=name)
                return image

            load("first.vod", 31)
            page.evaluate("""() => {
                setSlider('bh_size', 151);
                $('bh_size').oninput();
                cancelAnimationFrame(frame);
                renderPending();
                setSlider('bh_size', 91);
                $('bh_size').oninput();
            }""")
            page.wait_for_function("!filterJob && !pendingStage && !frame")
            self.assertTrue(page.evaluate("!workerUnavailable && doc.filter.size === 91"))
            page.evaluate("""() => {
                setSlider('bh_size', 111);
                $('bh_size').oninput();
                cancelAnimationFrame(frame);
                renderPending();
            }""")
            image = load("second.vod", 51)
            page.wait_for_function("!filterJob && !pendingStage && !frame")
            got = page.evaluate("Array.from(doc.filter.blackhat)")
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (51, 51))
            np.testing.assert_array_equal(np.array(got).reshape(image.shape),
                                          cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel))
            page.evaluate("""() => {
                setSlider('bh_thresh', 255);
                $('bh_thresh').oninput();
                $('accumulate').click();
            }""")
            self.assertFalse(page.evaluate("doc.accumulated.some(Boolean)"))
            browser.close()
