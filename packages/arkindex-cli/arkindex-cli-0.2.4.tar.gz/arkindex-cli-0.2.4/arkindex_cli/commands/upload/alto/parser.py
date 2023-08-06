# -*- coding: utf-8 -*-
from lxml import etree as ET


def _is_alto_namespace(namespace: str) -> bool:
    return (
        namespace.startswith("http://www.loc.gov/standards/alto/")
        # Older URLs for ALTO≤2.0
        or namespace.startswith("http://schema.ccs-gmbh.com/docworks/")
    )


class AltoElement:
    def __init__(self, node, page_width=None, page_height=None, alto_namespace=None):
        if alto_namespace:
            self.namespaces = {"alto": alto_namespace}
        else:
            alto_namespaces = set(filter(_is_alto_namespace, node.nsmap.values()))

            if len(alto_namespaces) == 1:
                self.namespaces = {"alto": alto_namespaces.pop()}
            elif len(alto_namespaces) > 1:
                raise ValueError(f"Multiple ALTO namespaces found: {alto_namespaces}")
            else:
                raise ValueError("ALTO namespace not found")

        self.node_name = ET.QName(node).localname.lower()
        self.has_text = node.findall("{*}String", namespaces=self.namespaces)
        self.page_width = page_width or self.get_width(node)
        self.page_height = page_height or self.get_height(node)
        # If there are more than one Page node in the file, the image id required
        # to build the IIIF url for the images is retrieved from the Page's
        # PHYSICAL_IMG_NR attribute and stored as page_image_id.
        self.page_image_id = self.get_page_image_id(node)
        self.content = node
        self.children = []

    def xml_int_value(self, node, attr_name):
        value = node.get(attr_name)
        if value is None:
            raise ValueError(f"Missing required value: {attr_name}")
        # The ALTO specification accepts float coordinates, but Arkindex only supports integers
        return round(float(value))

    def get_polygon_coordinates(self, node):
        if not (
            "HPOS" in node.attrib
            and "VPOS" in node.attrib
            and "WIDTH" in node.attrib
            and "HEIGHT" in node.attrib
        ):
            return

        # Skip elements with polygons with w or h <= 0 (invalid polygons)
        width = self.xml_int_value(node, "WIDTH")
        height = self.xml_int_value(node, "HEIGHT")
        if width <= 0 or height <= 0:
            return

        return {
            "x": self.xml_int_value(node, "HPOS"),
            "y": self.xml_int_value(node, "VPOS"),
            "width": width,
            "height": height,
        }

    def get_width(self, node):
        if "WIDTH" not in node.attrib:
            return
        return self.xml_int_value(node, "WIDTH")

    def get_height(self, node):
        if "HEIGHT" not in node.attrib:
            return
        return self.xml_int_value(node, "HEIGHT")

    def get_page_image_id(self, node):
        if "PHYSICAL_IMG_NR" not in node.attrib:
            return
        return node.get("PHYSICAL_IMG_NR")

    def ark_polygon(self, dict):
        """
        A polygon compatible with Arkindex.
        """
        if dict:
            polygon = [
                [dict["x"], dict["y"]],
                [dict["x"], dict["y"] + dict["height"]],
                [dict["x"] + dict["width"], dict["y"] + dict["height"]],
                [dict["x"] + dict["width"], dict["y"]],
                [dict["x"], dict["y"]],
            ]
            # We trim the polygon of the element in the case where its dimensions are bigger than the dimensions of the image
            return [
                [min(self.page_width, max(0, x)), min(self.page_height, max(0, y))]
                for x, y in polygon
            ]

    @property
    def has_children(self):
        return len(list(self.content)) > 0

    @property
    def polygon(self):
        return self.ark_polygon(self.get_polygon_coordinates(self.content))

    @property
    def width(self):
        return self.get_width(self.content)

    @property
    def height(self):
        return self.get_height(self.content)

    @property
    def name(self):
        return self.content.get("ID")

    def parse_children(self):
        if not self.has_children:
            return
        for child in self.content:
            child_element = AltoElement(
                child,
                page_width=self.page_width,
                page_height=self.page_height,
                alto_namespace=self.namespaces["alto"],
            )
            # String nodes are not sent to Arkindex as Elements, but their "CONTENT"
            # is sent as the transcription for their parent node.
            if child_element.node_name != "string":
                self.children.append(child_element)
                child_element.parse_children()

    def serialize(self):
        """
        Convert an Alto XML node and its children to a dictionary that will serve
        as a base for creating elements on Arkindex.
        """
        node_dict = {"type": self.node_name, "name": self.name, "children": []}
        if self.polygon:
            node_dict["polygon"] = self.polygon
        if len(self.has_text) > 0:
            full_text = " ".join(
                item.attrib["CONTENT"] for item in self.has_text
            ).strip()
            if len(full_text) > 0:
                node_dict["text"] = full_text
        if len(self.children):
            for item in self.children:
                node_dict["children"].append(item.serialize())
        return node_dict

    @property
    def serialized_children(self):
        return self.serialize()["children"]


class RootAltoElement(AltoElement):
    def __init__(self, node, alto_namespace=None):
        super().__init__(node, alto_namespace=alto_namespace)
        # Retrieve the file's measurement unit, used to specify the image(s) and polygons
        # dimensions; we only support pixels.
        try:
            self.unit = node.find(
                "{*}Description/{*}MeasurementUnit", namespaces=self.namespaces
            ).text
            assert self.unit == "pixel", f"Unsupported measurement unit {self.unit}"
        except AttributeError:
            raise ValueError("The MesurementUnit is missing.")
        try:
            # Retrieve the fileName node, which contains the identifier required to build the
            # IIIF url for the image (if there is only one Page node in the file.)
            self.filename = node.find(
                "{*}Description/{*}sourceImageInformation/{*}fileName",
                namespaces=self.namespaces,
            ).text
            assert self.filename, "Missing image file name"
        except AttributeError:
            raise ValueError("The fileName node is missing.")
