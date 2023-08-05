

from annotator.util import resize_image, HWC3
from annotator.canny import CannyDetector
from annotator.midas import MidasDetector
from annotator.hed import HEDdetector, nms
from annotator.mlsd import MLSDdetector
from annotator.openpose import OpenposeDetector
from annotator.uniformer import UniformerDetector

from PIL import Image
import numpy as np
import torch
import cv2

annotators = {}


def hint_canny(image: Image.Image, width=512, height=512, low_threshold=100, high_threshold=200):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        img = resize_image(HWC3(input_image), image_resolution)

        if not 'canny' in annotators:
            annotators['canny'] = CannyDetector()
        detected_map = annotators['canny'](img, low_threshold, high_threshold)
        detected_map = HWC3(detected_map)
        return Image.fromarray(detected_map)


def hint_depth(image: Image.Image, width=512, height=512, detect_resolution=384):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)

        if not 'midas' in annotators:
            annotators['midas'] = MidasDetector()

        detected_map, _ = annotators['midas'](
            resize_image(input_image, detect_resolution))
        detected_map = HWC3(detected_map)
        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(detected_map)


def hint_fake_scribble(image: Image.Image, width=512, height=512, detect_resolution=512):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)

        if not 'hed' in annotators:
            annotators['hed'] = HEDdetector()

        detected_map = annotators['hed'](
            resize_image(input_image, detect_resolution))
        detected_map = HWC3(detected_map)
        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        detected_map = nms(detected_map, 127, 3.0)
        detected_map = cv2.GaussianBlur(detected_map, (0, 0), 3.0)
        detected_map[detected_map > 4] = 255
        detected_map[detected_map < 255] = 0
        return Image.fromarray(detected_map)


def hint_hed(image: Image.Image, width=512, height=512, detect_resolution=512):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)

        if not 'hed' in annotators:
            annotators['hed'] = HEDdetector()

        detected_map = annotators['hed'](
            resize_image(input_image, detect_resolution))
        detected_map = HWC3(detected_map)
        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(detected_map)


def hint_hough(image: Image.Image, width=512, height=512, detect_resolution=512,
               value_threshold=0.1, distance_threshold=0.1):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)
        if not 'mlsd' in annotators:
            annotators['mlsd'] = MLSDdetector()
        detected_map = annotators['mlsd'](resize_image(
            input_image, detect_resolution), value_threshold, distance_threshold)
        detected_map = HWC3(detected_map)
        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_NEAREST)
        return Image.fromarray(detected_map)


def hint_normal(image: Image.Image, width=512, height=512, detect_resolution=384, bg_threshold=0.4):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)

        if not 'midas' in annotators:
            annotators['midas'] = MidasDetector()

        _, detected_map = annotators['midas'](
            resize_image(input_image, detect_resolution), bg_th=bg_threshold)
        detected_map = HWC3(detected_map)
        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(detected_map)


def hint_openpose(image: Image.Image, width=512, height=512, detect_resolution=512):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)

        if not 'openpose' in annotators:
            annotators['openpose'] = OpenposeDetector()

        detected_map, _ = annotators['openpose'](
            resize_image(input_image, detect_resolution))
        detected_map = HWC3(detected_map)
        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(detected_map)


def hint_scribble(image: Image.Image, width=512, height=512):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        img = resize_image(HWC3(input_image), image_resolution)
        H, W, C = img.shape

        detected_map = np.zeros_like(img, dtype=np.uint8)
        detected_map[np.min(img, axis=2) < 127] = 255
        return Image.fromarray(detected_map)


def hint_segmentation(image: Image.Image, width=512, height=512, detect_resolution=512):
    with torch.no_grad():
        input_image = np.array(image)
        image_resolution = width

        input_image = HWC3(input_image)

        if not 'uniformer' in annotators:
            annotators['uniformer'] = UniformerDetector()

        detected_map = annotators['uniformer'](
            resize_image(input_image, detect_resolution))

        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(
            detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        return Image.fromarray(detected_map)
