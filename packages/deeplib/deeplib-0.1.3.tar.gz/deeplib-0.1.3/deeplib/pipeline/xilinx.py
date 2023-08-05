from typing import Any, Optional

from ..gst_element_factory import GstElementFactory
from ..pipeline.processing import ProcessingElement


class XilinxFaceDetect(ProcessingElement):
    def __init__(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        ProcessingElement.__init__(self, _id, link_to)

        videoconvert = GstElementFactory.element("videoconvert")
        facedetect = GstElementFactory.element("vaifacedetect")

        self.add_multiple(videoconvert, facedetect)


class XilinxPersonDetect(ProcessingElement):
    def __init__(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        ProcessingElement.__init__(self, _id, link_to)

        persondetect = GstElementFactory.element("vaipersondetect")
        videoconvert = GstElementFactory.element("videoconvert")

        self.add_multiple(videoconvert, persondetect)


class XilinxSingleShotDetector(ProcessingElement):
    def __init__(
        self, model: Any, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        ProcessingElement.__init__(self, _id, link_to)

        vaissd = GstElementFactory.element("vaissd", {"model": model})
        videoconvert = GstElementFactory.element("videoconvert")

        self.add_multiple(videoconvert, vaissd)
