from typing import Any, Dict, Optional

import gi

from .error import check_created

gi.require_version("Gst", "1.0")

from gi.repository import Gst


class GstElementFactory:
    @staticmethod
    def pipeline() -> Gst.Pipeline:
        print("Creating Pipeline")
        pipeline = Gst.Pipeline()
        return check_created(pipeline, "pipeline")

    @staticmethod
    def element(_type: str, properties: Optional[Dict[str, Any]] = None) -> Gst.Element:
        print(f"create_elem {_type}: props={properties}")
        element = Gst.ElementFactory.make(_type)

        if properties:
            for name, value in properties.items():
                element.set_property(name, value)
        return check_created(element, _type)

    @classmethod
    def caps_filter(cls, caps: str) -> Gst.Element:
        return cls.element("capsfilter", {"caps": Gst.caps_from_string(caps)})
