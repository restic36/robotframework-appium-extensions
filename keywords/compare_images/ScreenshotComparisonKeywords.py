from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os


class ScreenshotComparisonKeywords:
    """
    Library for capturing and comparing screenshots using Appium and OpenCV.
    Provides keywords to save screenshots and compare them visually using SSIM + pixel difference.
    """

    def __init__(self, default_path="screenshots"):
        self._builtin = BuiltIn()
        self.default_path = default_path
        os.makedirs(self.default_path, exist_ok=True)

    @property
    def driver(self):
        return self._builtin.get_library_instance('AppiumLibrary')._current_application()

    @keyword("Capture Initial Screenshot As")
    def capture_initial_screenshot(self, filename, path=None):
        """
        Captures a screenshot and saves it.
        - filename: name of the screenshot (e.g. "home.png")
        - path: optional path (default: screenshots/)
        """
        save_path = path or self.default_path
        os.makedirs(save_path, exist_ok=True)
        full_path = os.path.join(save_path, filename)

        self.driver.save_screenshot(full_path)
        logger.info(f"📸 Initial screenshot saved at: {full_path}")

    @keyword("Compare Final Screenshot With")
    def compare_final_screenshot(self, reference_file, tolerance=0.10, path=None):
        """
        Captures a final screenshot, compares it with reference image.
        Uses SSIM + pixel difference.
        - reference_file: path to reference image
        - tolerance: max allowed difference (0-1). Default = 0.10 (10%)
        - path: optional path (default: screenshots/)
        """
        save_path = path or self.default_path
        os.makedirs(save_path, exist_ok=True)

        final_image_path = os.path.join(save_path, "screenshot_final.png")
        diff_path = os.path.join(save_path, "diff.png")

        self.driver.save_screenshot(final_image_path)
        logger.info(f"📸 Final screenshot saved at: {final_image_path}")

        # Load images
        image1 = cv2.imread(reference_file)
        image2 = cv2.imread(final_image_path)

        if image1 is None or image2 is None:
            raise ValueError("❌ Failed to load one or both images.")

        if image1.shape != image2.shape:
            raise AssertionError("❌ Images have different sizes and cannot be compared.")

        # Convert to grayscale for SSIM
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

        # SSIM score
        score, diff = ssim(gray1, gray2, full=True)
        percent_difference = 1 - score

        # Pixel diff (extra check)
        pixel_diff = cv2.absdiff(gray1, gray2)
        non_zero_count = np.count_nonzero(pixel_diff)
        total_pixels = gray1.shape[0] * gray1.shape[1]
        pixel_diff_ratio = non_zero_count / total_pixels

        # Save diff visualization
        diff = (diff * 255).astype("uint8")
        cv2.imwrite(diff_path, diff)
        logger.info(f"📂 Visual diff saved: {diff_path}")

        logger.info(f"🔍 SSIM similarity: {score:.4f} — Difference: {percent_difference:.2%}")
        logger.info(f"🔍 Pixel difference ratio: {pixel_diff_ratio:.2%}")

        # Decision
        final_difference = max(percent_difference, pixel_diff_ratio)

        if final_difference > tolerance:
            raise AssertionError(f"❌ Visual difference greater than tolerated: {final_difference:.2%}")

        logger.info("✅ Images are visually similar within tolerance.")
