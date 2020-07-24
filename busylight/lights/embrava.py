"""Embrava Blynclight support.
"""

from typing import Tuple

from .usblight import USBLight, UnknownUSBLight
from .usblight import USBLightAttribute
from .usblight import USBLightReadOnlyAttribute


class BlynclightCommandHeader(USBLightReadOnlyAttribute):
    """A constant 16-bit field with zero value."""


class BlynclightColor(USBLightAttribute):
    """An 8-bit color."""


class BlynclightOff(USBLightAttribute):
    """Toggle the light off and on: 1 == off, 0 == on."""


class BlynclightDim(USBLightAttribute):
    """Toggle the light from bright to dim. bright == 0, dim == 1."""


class BlynclightFlash(USBLightAttribute):
    """Toggle the light from steady to flash mode."""


class BlynclightSpeed(USBLightAttribute):
    """A four bit field that specifies the flash speed."""


class BlynclightRepeat(USBLightAttribute):
    """Toggle tune repeat: 0 once, 1 repeat"""


class BlynclightPlay(USBLightAttribute):
    """Toggle playing selected tune."""


class BlynclightMusic(USBLightAttribute):
    """Select a tune in firmware: 0 - 10"""


class BlynclightMute(USBLightAttribute):
    """Toggle muting the tune being played. 0 == play, 1 == mute."""


class BlynclightVolume(USBLightAttribute):
    """Volume of the tune when played: 0 - 10"""


class BlynclightCommandFooter(USBLightReadOnlyAttribute):
    """A 16-bit constant field with value 0xFF22."""


class Blynclight(USBLight):
    """An Embrava Blynclight device.

    """

    VENDOR_IDS = [0x2C0D, 0x03E5]

    __vendor__ = "Embrava"

    def __init__(self, vendor_id: int, product_id: int):
        """
        :param vendor_id: 16-bit int
        :param product_id: 16-bit int
        
        Raises:
        - UnknownUSBLight
        - USBLightInUse
        - USBLightNotFound
        """

        if vendor_id not in self.VENDOR_IDS:
            raise UnknownUSBLight(vendor_id)

        super().__init__(vendor_id, product_id, 0x00000000090080FF22, 72)

    header = BlynclightCommandHeader(64, 8)
    red = BlynclightColor(56, 8)
    blue = BlynclightColor(48, 8)
    green = BlynclightColor(40, 8)
    _off = BlynclightOff(32, 1)
    dim = BlynclightDim(33, 1)
    flash = BlynclightFlash(34, 1)
    speed = BlynclightSpeed(35, 3)
    repeat = BlynclightRepeat(29, 1)
    play = BlynclightPlay(28, 1)
    music = BlynclightMusic(24, 4)
    mute = BlynclightMute(23, 1)
    volume = BlynclightVolume(18, 4)
    footer = BlynclightCommandFooter(0, 16)

    def on(self, color: Tuple[int, int, int] = None) -> None:
        """Turn the light on with the specified color [default=green].
        """

        color = color or (0, 255, 0)

        self.bl_on(color)

    def off(self) -> None:
        """Turn the light off.
        """

        self.bl_off()

    def blink(self, color: Tuple[int, int, int] = None, speed: int = 1) -> None:
        """Turn the light on with specified color [default=red] and begin blinking.

        :param color: Tuple[int, int, int]
        :param speed: 1 == slow, 2 == medium, 3 == fast
        """

        self.bl_blink(color or (255, 0, 0), speed)

    def bl_on(self, color: Tuple[int, int, int], dim: bool = False) -> None:
        """
        """

        with self.batch_update():
            self.reset()
            self.color = color
            self.dim = dim
            self._off = 0

    def bl_off(self) -> None:
        """
        """

        with self.batch_update():
            self._off = 1

    def bl_blink(self, color: Tuple[int, int, int], speed: int = 1) -> None:
        """
        """

        with self.batch_update():
            self.color = color
            self.flash = 1
            self.speed = 1 << (speed - 1)
            if self.speed == 0:
                self.speed = 1
            self._off = 0