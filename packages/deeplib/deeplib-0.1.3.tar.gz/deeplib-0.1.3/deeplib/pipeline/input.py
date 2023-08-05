from typing import TYPE_CHECKING, Optional, Union

from ..error import error
from ..gst_element_factory import GstElementFactory
from ..pipeline.elements import PipelineElement

if TYPE_CHECKING:
    from ..platform.director import Platform
    from ..platform.generic import GenericPlatform
    from ..platform.nvidia import NvidiaPlatform


class InputElement(PipelineElement):
    def __init__(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        super(InputElement, self).__init__(_id, link_to)


class FileInput(InputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        path: str,
        encoding: str = "H264",
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(FileInput, self).__init__(_id, link_to)

        source = GstElementFactory.element("filesrc", {"location": path})

        if encoding is "H264":
            parser = GstElementFactory.element("h264parse")
            decoder = platform.create_hw_accelerated_element(
                PipelineElement.ELEMENT_TYPE_H264_DECODE
            )
        else:
            raise error(f"Unkown encoding {encoding}")

        streammux = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_STREAM_MUX
        )

        self.add_multiple(source, parser, decoder)

        if streammux:
            self.add(streammux, gst_sink_pad="sink_0")
        else:
            queue = GstElementFactory.element("queue")
            self.add(queue)


class MipiCameraInput(InputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(MipiCameraInput, self).__init__(_id, link_to)

        cam = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_CAMERA_SOURCE
        )

        caps_filter = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_CAPS_FILTER_NV12_720P
        )

        self.add_multiple(cam, caps_filter)


class USBCameraInput(InputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        device: str = "/dev/video1",
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
        encoding: str = "H264",
    ) -> None:
        super(USBCameraInput, self).__init__(_id, link_to)

        # note: tested with Logitech C920
        v4l2src = GstElementFactory.element("v4l2src", {"device": device})

        self.add(v4l2src)

        if encoding is "H264":
            caps_filter = GstElementFactory.caps_filter(
                "video/x-h264, width=1280, height=720, framerate=30/1"
            )
            h264parse = GstElementFactory.element("h264parse")

            h264decode = platform.create_hw_accelerated_element(
                PipelineElement.ELEMENT_TYPE_H264_DECODE
            )

            self.add_multiple(caps_filter, h264parse, h264decode)


class HDMIInput(InputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(HDMIInput, self).__init__(_id, link_to)

        hdmi_input = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_HDMI_SOURCE
        )

        self.add(hdmi_input)
