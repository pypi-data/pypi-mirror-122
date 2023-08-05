import json
from typing import TYPE_CHECKING, Any, Dict, Optional

from ..error import error

if TYPE_CHECKING:
    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import Gst

    from ..deeplib import DeepLib
    from ..pipeline.builder import PipelineBuilder


class JsonPipelineConfigLoader:
    def __init__(self, deep_lib: "DeepLib"):
        self.deep_lib = deep_lib
        self.pipeline_builder: "PipelineBuilder" = self.deep_lib.pipeline()

    def load_from_file(self, path: str) -> Gst.Pipeline:
        with open(path) as json_file:
            data = json.load(json_file)
            for element in data["elements"]:
                _id = element["_id"]
                _type = element["_type"]
                properties = element.get("properties")
                links = element.get("links")
                self.parse_element(_id, _type, properties, links)

        return self.pipeline_builder.build()

    def parse_element(
        self,
        _id: str,
        _type: str,
        properties: Optional[Dict[str, Any]],
        connections: Optional[Dict[str, Any]],
    ) -> None:
        print(f"parse element {_id} {_type} {properties} {connections}")
        if _type == "file-input":
            if not isinstance(properties, dict):
                raise error("invalid configuration for properties of file-input")

            self.pipeline_builder.with_file_input(_id=_id, path=properties["path"])

        elif _type == "mipi-camera-input":
            self.pipeline_builder.with_mipi_camera_input(_id=_id)

        elif _type == "usb-camera-input":
            self.pipeline_builder.with_usb_camera_input(_id=_id)

        elif _type == "nv-infer":
            if not isinstance(connections, dict):
                raise error("invalid configuration for connections of nv-infer")

            if not isinstance(properties, dict):
                raise error("invalid configuration for properties of nv-infer")

            self.pipeline_builder.with_nv_infer(
                _id=_id,
                config_path=properties["path"],
                link_to=self.connection_to_component_id(connections["in"]),
            )

        elif _type == "nv-tracker":
            if not isinstance(connections, dict):
                raise error("invalid configuration for connections of nv-tracker")

            if not isinstance(properties, dict):
                raise error("invalid configuration for properties of nv-tracker")

            self.pipeline_builder.with_nv_tracker(
                _id=_id,
                config_path=properties["path"],
                link_to=self.connection_to_component_id(connections["in"]),
            )

        elif _type == "nv-osd":
            if not isinstance(connections, dict):
                raise error("invalid configuration for connections of nv-osd")

            self.pipeline_builder.with_nv_osd(
                _id=_id, link_to=self.connection_to_component_id(connections["in"])
            )

        elif _type == "egl-output":
            if not isinstance(connections, dict):
                raise error("invalid configuration for connections of egl-output")

            self.pipeline_builder.with_egl_output(
                _id=_id, link_to=self.connection_to_component_id(connections["in"])
            )

        elif _type == "rtsp-output":
            if not isinstance(properties, dict):
                raise error("invalid configuration for properties of rtsp-output")

            if not isinstance(connections, dict):
                raise error("invalid configuration for connections of rtsp-output")

            self.pipeline_builder.with_rtsp_output(
                _id=_id, path=properties["path"], link_to=connections["in"]
            )

        elif _type == "tcp-output":
            if not isinstance(connections, dict):
                raise error("invalid configuration for connections of tcp-output")

            self.pipeline_builder.with_tcp_output(_id=_id, link_to=connections["in"])

    @staticmethod
    def connection_to_component_id(connection: str) -> str:
        return connection.split("/")[0]
