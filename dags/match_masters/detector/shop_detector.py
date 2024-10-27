from pathlib import Path

import cv2
import numpy as np

from match_masters.detector.screen_fragment import ScreenFragment


class ShopDetector:

    def __init__(self):
        self.roi_enter_shop = ScreenFragment(top=1420, bottom=1510, left=20, right=130,
                                             expected_images={
                                             "shop_clicked": self._read_image("shop_clicked.png"),
                                             "shop_not_clicked": self._read_image("shop_not_clicked.png")
                                         })
        self.roi_init_gift_receive = ScreenFragment(top=760, bottom=800, left=20, right=45,
                                                    expected_images={
                                                    "init_gift_receive_green": self._read_image(
                                                        "init_gift_receive_green.png"),
                                                })
        self.roi_gift = ScreenFragment(top=1360, bottom=1405, left=240, right=480, expected_images={})
        self.roi_receive_gift = ScreenFragment(top=1375, bottom=1470, left=385, right=620, expected_images={})

    @staticmethod
    def _read_image(image_name: str) -> np.ndarray:
        return cv2.imread((Path(__file__).parent / 'resources' / image_name).as_posix())

    def detect_shop_button(self, screen_data: np.ndarray) -> bool:
        enter_shop = self.roi_enter_shop.extract(screen_data)
        return np.all(enter_shop == self.roi_enter_shop.expected_images["shop_clicked"])

    def detect_receive_free_gift_button(self, screen_data: np.ndarray) -> bool:
        init_gift_receive = self.roi_init_gift_receive.extract(screen_data)
        return np.all(init_gift_receive == self.roi_init_gift_receive.expected_images["init_gift_receive_green"])
