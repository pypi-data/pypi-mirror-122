from typing import TYPE_CHECKING, Optional, Union

from ..error import check_created
from ..gst_element_factory import GstElementFactory
from ..pipeline.elements import PipelineElement
from ..rtsp_utils import RTSPServer

if TYPE_CHECKING:
    from ..deeplib import DeepLib
    from ..platform.director import Platform
    from ..platform.generic import GenericPlatform
    from ..platform.nvidia import NvidiaPlatform


class OutputElement(PipelineElement):
    def __init__(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        super(OutputElement, self).__init__(_id, link_to)


class EGLOutput(OutputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(EGLOutput, self).__init__(_id, link_to)

        gl_sink = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_GL_SINK
        )
        gl_transform = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_GL_TRANSFORM
        )

        if gl_transform:
            self.add(gl_transform)

        self.add(gl_sink)


class RTSPOutput(OutputElement):
    def __init__(
        self,
        deep_lib: "DeepLib",
        bit_rate: int = 1000000,
        upd_port: int = 12222,
        name: str = "rtsp-output",
        path: str = "/test",
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(RTSPOutput, self).__init__(_id, link_to)

        if not hasattr(deep_lib, "rtsp_server") or deep_lib.rtsp_server is None:
            deep_lib.rtsp_server = RTSPServer()

        deep_lib.rtsp_server.add_path(path)

        print("Create RTSP stream\n")

        self.platform = check_created(deep_lib.platform(), "platform")

        vidconv = self.platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_VIDEO_CONVERT
        )
        caps_filter = self.platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_CAPS_FILTER_I420_RAW
        )
        h264_encoder = self.platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_H264_ENCODE, {"bit_rate": bit_rate}
        )
        rtph264_pay = GstElementFactory.element("rtph264pay")
        udp_sink = GstElementFactory.element(
            "udpsink",
            {"host": "127.0.0.1", "port": upd_port, "async": False, "sync": False},
        )

        self.add_multiple(vidconv, caps_filter, h264_encoder, rtph264_pay, udp_sink)


class TCPOutput(OutputElement):
    def __init__(
        self,
        bit_rate: int = 1000000,
        port: int = 8888,
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(TCPOutput, self).__init__(_id, link_to)

        videoconvert = GstElementFactory.element("videoconvert")
        theoraenc = GstElementFactory.element("theoraenc")
        oggmux = GstElementFactory.element("oggmux")
        tcpserversink = GstElementFactory.element(
            "tcpserversink", {"host": "0.0.0.0", "port": port}
        )

        self.add_multiple(videoconvert, theoraenc, oggmux, tcpserversink)


class HDMIOutput(OutputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(HDMIOutput, self).__init__(_id, link_to)

        hdmi_sink = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_HDMI_SINK
        )

        self.add(hdmi_sink)


class DisplayPortOutput(OutputElement):
    def __init__(
        self,
        platform: Union["GenericPlatform", "NvidiaPlatform", "Platform"],
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        super(DisplayPortOutput, self).__init__(_id, link_to)

        dp_sink = platform.create_hw_accelerated_element(
            PipelineElement.ELEMENT_TYPE_DISPLAYPORT_SINK
        )

        self.add(dp_sink)
