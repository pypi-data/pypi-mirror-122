from typing import TYPE_CHECKING, Any, Dict, Optional

from ..gst_element_factory import GstElementFactory
from ..pipeline.elements import PipelineElement
from ..platform.generic import GenericPlatform

if TYPE_CHECKING:
    import gi

    gi.require_version("Gst", "1.0")

    from gi.repository import Gst

# Xilinx UltraScale+ based platforms
class XilinxPlatform(GenericPlatform):
    @classmethod
    def create(cls) -> Optional["XilinxPlatform"]:
        import platform

        if "xilinx" not in platform.platform():
            return None

        return cls()

    def create_hw_accelerated_element(
        self, _type: str, props: Optional[Dict[str, Any]] = None
    ) -> Optional[Gst.Element]:
        if not isinstance(props, dict):
            props = {}

        if _type == PipelineElement.ELEMENT_TYPE_H264_DECODE:
            return GstElementFactory.element("omxh264dec")

        elif _type == PipelineElement.ELEMENT_TYPE_H264_ENCODE:
            return GstElementFactory.element(
                "omxh264enc",
                {
                    "target-bitrate": props["bitRate"],
                },
            )

        elif _type == PipelineElement.ELEMENT_TYPE_HDMI_SOURCE:
            # TODO device
            return GstElementFactory.element("v4l2src")

        elif _type == PipelineElement.ELEMENT_TYPE_HDMI_SINK:
            # TODO xlnxvideosink sink-type="hdmi" sync=false
            return GstElementFactory.element(
                "kmssink",
                {
                    "bus-id": "b00c0000.v_mix",
                    "plane-id": 30,
                    "sync": False,
                    "fullscreen-overlay": False,
                },
            )

        elif _type == PipelineElement.ELEMENT_TYPE_DISPLAYPORT_SINK:
            # TODO xlnxvideosink sink-type="dp" sync=false
            return GstElementFactory.element(
                "kmssink",
                {
                    "bus-id": "b00c0000.v_mix",
                    "plane-id": 30,
                    "sync": False,
                    "fullscreen-overlay": False,
                },
            )

        else:
            return super(XilinxPlatform, self).create_hw_accelerated_element(
                _type, props
            )
