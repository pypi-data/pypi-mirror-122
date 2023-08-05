from typing import Optional

from ..error import error
from ..gst_element_factory import GstElementFactory
from ..pipeline.elements import PipelineElement


class ProcessingElement(PipelineElement):
    def __init__(
        self, _id: Optional[str] = None, link_to: Optional[str] = None
    ) -> None:
        super(ProcessingElement, self).__init__(_id, link_to)


class Multiplexer(ProcessingElement):
    def __init__(
        self, nr_outputs: int, link_to: str, _id: Optional[str] = None
    ) -> None:
        super(Multiplexer, self).__init__(_id)

        if not self._id:
            raise error("_id wasn't created")

        tee = GstElementFactory.element("tees")
        tee_id = self._id + "-tee"
        self.add(tee, _id=tee_id, link_to=link_to, gst_source_pad="src_%u")

        for i in range(0, nr_outputs):
            queue = GstElementFactory.element("queue")
            self.add(queue, _id=self.output_id(i), link_to=tee_id)

    def output_id(self, nr: int) -> str:
        if not self._id:
            raise error("_id wasn't created")

        return self._id + "-queue-" + str(nr)
