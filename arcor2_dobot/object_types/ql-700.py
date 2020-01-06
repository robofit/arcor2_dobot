from typing import Optional

from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster
import qrcode
from PIL import Image

from arcor2.object_types import Generic
from arcor2.data.common import Pose, ActionMetadata
from arcor2.data.object_type import Models
from arcor2.action import action
from arcor2.exceptions import Arcor2Exception

PX_WIDTH = 696


class QL700Exception(Arcor2Exception):
    pass


class QL700(Generic):

    def __init__(self, obj_id: str, pose: Pose, collision_model: Optional[Models] = None) -> None:
        super(QL700, self).__init__(obj_id, pose, collision_model)

        self.qlr = BrotherQLRaster("QL-700")
        self.qlr.exception_on_warning = True

    @action
    def print(self, qr_text: str) -> None:

        qr = qrcode.make(qr_text)

        img = qr.get_image()
        img = img.resize((PX_WIDTH, PX_WIDTH))

        status = send(instructions=convert(self.qlr, [img], "62", cut=False), printer_identifier="usb://0x04f9:0x2042",
             backend_identifier="pyusb", blocking=True)

        if False in (status["did_print"], status["ready_for_next_job"]):
            raise QL700Exception()

    @action
    def cut(self) -> None:

        # kind of hack (it is so far not possible to only perform cut)
        img = Image.new('RGB', (PX_WIDTH, 1), (255, 255, 255))
        status = send(instructions=convert(self.qlr, [img], "62"), printer_identifier="usb://0x04f9:0x2042",
             backend_identifier="pyusb", blocking=True)

        if False in (status["did_print"], status["ready_for_next_job"]):
            raise QL700Exception()

    print.__action__ = ActionMetadata(free=True, blocking=True)
    cut.__action__ = ActionMetadata(free=True, blocking=True)

