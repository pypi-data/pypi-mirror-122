from typing import TYPE_CHECKING, Any, Optional

from ..error import check_created
from ..gst_element_factory import GstElementFactory
from ..pipeline.input import FileInput, HDMIInput, MipiCameraInput, USBCameraInput
from ..pipeline.nvidia import NVInfer, NVOsd, NVTracker
from ..pipeline.output import (
    DisplayPortOutput,
    EGLOutput,
    HDMIOutput,
    RTSPOutput,
    TCPOutput,
)
from ..pipeline.pipeline import Pipeline
from ..pipeline.xilinx import (
    XilinxFaceDetect,
    XilinxPersonDetect,
    XilinxSingleShotDetector,
)

if TYPE_CHECKING:
    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import Gst

    from ..deeplib import DeepLib


class PipelineBuilder:
    def __init__(self, deep_lib: "DeepLib"):
        self.deep_lib = deep_lib
        self.platform = deep_lib.platform()
        self.pipeline = Pipeline(GstElementFactory.pipeline())

    def add(self, element: Any) -> "PipelineBuilder":
        self.pipeline.add(element)
        return self

    def with_file_input(
        self, path: str, encoding: str = "H264", _id: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(
            FileInput(check_created(self.platform, "platform"), path, encoding, _id=_id)
        )

    def with_mipi_camera_input(self, _id: Optional[str] = None) -> "PipelineBuilder":
        return self.add(
            MipiCameraInput(check_created(self.platform, "platform"), _id=_id)
        )

    def with_usb_camera_input(
        self,
        device: str = "/dev/video1",
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
        encoding: str = "H264",
    ) -> "PipelineBuilder":
        return self.add(
            USBCameraInput(
                check_created(self.platform, "platform"),
                device,
                _id=_id,
                encoding=encoding,
            )
        )

    def with_hdmi_input(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(
            HDMIInput(
                check_created(self.platform, "platform"), _id=_id, link_to=link_to
            )
        )

    def with_egl_output(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(
            EGLOutput(
                check_created(self.platform, "platform"), _id=_id, link_to=link_to
            )
        )

    def with_rtsp_output(
        self,
        bit_rate: int = 1000000,
        upd_port: int = 12222,
        name: str = "rtsp-output",
        path: str = "/test",
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> "PipelineBuilder":
        return self.add(
            RTSPOutput(
                self.deep_lib, bit_rate, upd_port, name, path, _id=_id, link_to=link_to
            )
        )

    def with_tcp_output(
        self,
        bit_rate: int = 1000000,
        port: int = 8888,
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> "PipelineBuilder":
        return self.add(TCPOutput(bit_rate, port, _id=_id, link_to=link_to))

    def with_hdmi_output(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(
            HDMIOutput(
                check_created(self.platform, "platform"), _id=_id, link_to=link_to
            )
        )

    def with_display_port_output(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(
            DisplayPortOutput(
                check_created(self.platform, "platform"), _id=_id, link_to=link_to
            )
        )

    # Nvidia specific
    def with_nv_infer(
        self, config_path: str, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(NVInfer(config_path, _id=_id, link_to=link_to))

    def with_nv_tracker(
        self, config_path: str, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(NVTracker(config_path, _id=_id, link_to=link_to))

    def with_nv_osd(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(NVOsd(_id=_id, link_to=link_to))

    # Xilinx specific
    def with_xilinx_face_detect(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(XilinxFaceDetect(_id=_id, link_to=link_to))

    def with_xilinx_person_detect(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(XilinxPersonDetect(_id=_id, link_to=link_to))

    def with_single_shot_detector(
        self, model: Any, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> "PipelineBuilder":
        return self.add(XilinxSingleShotDetector(model, _id=_id, link_to=link_to))

    def build(self) -> Gst.Pipeline:
        return self.pipeline.as_gst_pipeline()
