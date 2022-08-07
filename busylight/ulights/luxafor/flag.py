"""
"""

from loguru import logger

from ..hidlight import HIDLight, HIDInfo


class Flag(HIDLight):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x4D8, 0xF372): "Flag",
        }

    @staticmethod
    def vendor() -> str:
        return "Luxafor"

    @classmethod
    def claims(cls, hid_info: HIDInfo) -> bool:

        if not super().claims(hid_info):
            return False

        try:
            product = hid_info["product_string"].split()[-1].casefold()
        except (KeyError, IndexError) as error:
            logger.debug(f"problem {error} processing {hid_info}")
            return False

        return product in map(str.casefold, cls.supported_device_ids().values())
