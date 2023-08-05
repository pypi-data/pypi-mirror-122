from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import Gst


class PipelineElement:
    ELEMENT_TYPE_H264_DECODE = "h264decode"
    ELEMENT_TYPE_H264_ENCODE = "h264encode"
    ELEMENT_TYPE_CAPS_FILTER_I420_RAW = "capsfilterI420raw"
    ELEMENT_TYPE_CAPS_FILTER_NV12_720P = "capsfilterNV12p720"
    ELEMENT_TYPE_VIDEO_CONVERT = "videoconvert"
    ELEMENT_TYPE_STREAM_MUX = "streammux"
    ELEMENT_TYPE_CAMERA_SOURCE = "camsource"
    ELEMENT_TYPE_GL_SINK = "glsink"
    ELEMENT_TYPE_GL_TRANSFORM = "gltransform"
    ELEMENT_TYPE_HDMI_SOURCE = "hdmiSource"
    ELEMENT_TYPE_HDMI_SINK = "hdmiSink"
    ELEMENT_TYPE_DISPLAYPORT_SINK = "displayPortSink"

    _auto_nr = 1
    _id: Optional[str] = None

    @classmethod
    def auto_nr(cls) -> str:
        nr = cls._auto_nr
        PipelineElement._auto_nr += 1
        return str(nr)

    def __init__(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        if not _id:
            _id = type(self).__name__ + self.auto_nr()

        self._id = _id
        self.gst_elements: List[Any] = []
        self.gst_elements_by_id: Dict[str, Any] = dict()
        self.last_element: Optional[str] = None
        self.link_to = link_to

    def add(
        self,
        element: Optional[Gst.Element],
        gst_source_pad: Optional[str] = None,
        gst_sink_pad: Optional[str] = None,
        gst_probes: Optional[Dict[str, Any]] = None,
        _id: Optional[str] = None,
        link_to: Optional[str] = None,
    ) -> None:
        if not _id:
            _id = self.auto_nr() + "-gst-" + type(element).__name__

        if not link_to:
            link_to = self.last_element

        component = {
            "_id": _id,
            "link_to": link_to,
            "gst_element": element,
            "gst_source_pad": gst_source_pad,
            "gst_sink_pad": gst_sink_pad,
            "gst_probes": gst_probes,
        }

        self.gst_elements.append(component)
        self.gst_elements_by_id[_id] = component
        self.last_element = _id

    def add_multiple(self, *elements: Optional[Gst.Element]) -> None:
        for element in elements:
            self.add(element)
