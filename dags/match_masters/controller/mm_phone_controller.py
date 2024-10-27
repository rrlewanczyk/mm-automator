import time

from common.phone_controller import PhoneController
from match_masters.detector.shop_detector import ShopDetector


class MMPhoneController(PhoneController):
    MM_PACKAGE = "com.funtomic.matchmasters"
    MM_MAIN_ACTIVITY = "com.unity3d.player.UnityPlayerActivity"

    def __init__(self):
        super().__init__()
        self.shop_detector = ShopDetector()

    def get_phone_id(self):
        return "ZY326QS87X"

    def get_client_host(self):
        return "host.docker.internal"

    def open_match_masters(self):
        self.open_application(self.MM_PACKAGE, self.MM_MAIN_ACTIVITY)
        time.sleep(30)

    def close_match_masters(self):
        self.close_application(self.MM_PACKAGE)

    def try_to_enter_shop(self) -> bool:
        for press_num in range(1, 5):
            self.tap(*self.shop_detector.roi_enter_shop.mid())
            time.sleep(1)

        return True

    def try_to_init_gift_receive(self) -> bool:
        is_enter_available = self.shop_detector.detect_receive_free_gift_button(self.take_screenshot())
        if not is_enter_available:
            return False
        self.tap(*self.shop_detector.roi_init_gift_receive.mid())
        time.sleep(5)
        return True

    def tap_gift(self):
        self.tap(*self.shop_detector.roi_gift.mid())
        time.sleep(5)

    def tap_receive_gift(self):
        self.tap(*self.shop_detector.roi_receive_gift.mid())
        time.sleep(5)
