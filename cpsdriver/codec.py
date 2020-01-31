from typing import NamedTuple
from base64 import b64decode

import numpy as np


class ProductId(NamedTuple):
    """Unique id of a product"""

    barcode_type: str
    barcode: str

    @classmethod
    def from_dict(cls, id_dict):
        """Creates a ProductId from it's recorded encoding

        Args:
            id_dict (dict): The dict of a mongo doc
        """
        return cls(
            barcode_type=id_dict.get("barcode_type", ""),
            barcode=id_dict.get("id", ""),
        )


class Product(NamedTuple):
    """Information of a possible product"""

    product_id: ProductId
    name: str
    thumbnail: str
    price: float
    weight: float

    @classmethod
    def from_dict(cls, recorded):
        """Creates a Product from it's recorded encoding

        Args:
            recorded (dict): The dict of a mongo doc
        """
        meta = recorded["metadata"]
        return cls(
            product_id=ProductId.from_dict(recorded.get("product_id", {})),
            name=meta.get("name", ""),
            thumbnail=meta.get("thumbnail", ""),
            price=meta.get("price", 0.0),
            weight=meta.get("weight", 0.0),
        )


class Facing(NamedTuple):
    """Locations of products in the store"""

    product_id: ProductId
    plate_ids: list
    coordinates: dict

    @classmethod
    def from_dict(cls, recorded):
        """Creates a Product from it's recorded encoding

        Args:
            recorded (dict): The dict of a mongo doc
        """
        plate_ids = [
            PlateId.from_nested_dict(d)
            for d in recorded.get("plate_ids", [])
        ]
        return cls(
            product_id=ProductId.from_dict(
                recorded.get("planogram_product_id", {})
            ),
            plate_ids=plate_ids,
            coordinates=recorded.get("global_coordinates", {}),
        )


class PlateId(NamedTuple):
    """Combines gondola, shelf, and plate info to make a unique plate id"""

    gondola_id: int
    shelf_index: int
    plate_index: int

    @classmethod
    def from_dict(cls, recorded):
        """Creates a PlateId from it's recorded encoding

        Args:
            recorded (dict): The dict of a mongo doc
        """
        return cls(
            plate_index=recorded.get("plate_index", 0),
            shelf_index=recorded.get("shelf_index", 0),
            gondola_id=recorded.get("gondola_id", 0),
        )

    @classmethod
    def from_nested_dict(cls, nested):
        """Creates a PlateId from it's planogram encoding

        Args:
            recorded (dict): The dict of a planogram doc
        """
        shelf = nested.get("shelf_id", {})
        gondola = shelf.get("gondola_id", {})
        return cls(
            plate_index=nested.get("plate_index", 0),
            shelf_index=shelf.get("shelf_index", 0),
            gondola_id=gondola.get("id", 0),
        )


class Target(NamedTuple):
    """A single target"""

    target_id: str
    head: dict

    @classmethod
    def from_dict(cls, target):
        """Returns a decoded Target recording

        Args:
            target (dict): The subdict of a mongo doc
        """
        return cls(
            target_id=target["target_id"]["id"],
            head=target["head"],
        )


class Targets(NamedTuple):
    """Snapshot of all targets in store at a given time"""

    timestamp: float
    targets: list

    @classmethod
    def from_dict(cls, recorded):
        """Returns a decoded Targets recording

        Args:
            recorded (dict): The dict of a mongo doc
        """
        targets = [
            Target.from_dict(d)
            for d in recorded["document"]["targets"]["targets"]
        ]
        return cls(
            timestamp=recorded["timestamp"],
            targets=targets,
        )


class PlateData(NamedTuple):
    """Houses a batch of plate samples"""

    plate_id: PlateId
    frequency: float
    timestamp: float
    data: object

    @classmethod
    def from_dict(cls, recorded):
        """Returns a decoded PlateData recording

        Args:
            recorded (dict): The dict of a mongo doc
        """
        doc = recorded["document"]
        vals = doc["plate_data"]["values"]
        return cls(
            plate_id=PlateId.from_dict(recorded),
            frequency=doc["plate_data"]["freq_samp"],
            timestamp=recorded["timestamp"],
            data=NumpyRecordCodec.decode(
                vals["data"],
                vals["shape"],
                vals["type"],
            ),
        )


class DepthFrame(NamedTuple):
    """DepthFrame np array of depth data with metadata"""

    timestamp: float
    camera_id: int
    frame: object

    @classmethod
    def from_dict(cls, recorded):
        """Returns a decoded DepthFrame recording

        Args:
            recorded (dict): The dict of a mongo doc
        """
        doc = recorded["document"]
        frames = doc["frame_message"]["frames"]
        depth = np.empty()
        for frame in frames:
            _type = frame['frame_source']['camera_id']['camera_type']
            if _type == "DEPTH":
                depth = NumpyRecordCodec.decode(
                    frame["frame"]["data"],
                    frame["frame"]["shape"],
                    frame["frame"]["type"],
                ),
                break
        return cls(
            timestamp=recorded["timestamp"],
            camera_id=recorded["camera_id"],
            frame=depth
        )


class RGBFrame(NamedTuple):
    """RGBFrame raw byte array of a JPEG with metadata"""

    timestamp: float
    camera_id: int
    frame: bytes

    @classmethod
    def from_dict(cls, recorded):
        """Returns a decoded DepthFrame recording

        Args:
            recorded (dict): The dict of a mongo doc
        """
        doc = recorded["document"]
        frames = doc["frame_message"]["frames"]
        rgb = b''
        for frame in frames:
            _type = frame['frame_source']['camera_id']['camera_type']
            if _type == "RGB":
                rgb = b64decode(frame["frame"]['data'])
            break
        return cls(
            timestamp=recorded["timestamp"],
            camera_id=recorded["camera_id"],
            frame=rgb
        )


class AggregatedDepth(NamedTuple):
    """Combines RGB and depth frames from a single camera at timestamp"""

    timestamp: float
    camera_id: int
    rgb_frame: RGBFrame
    depth_frame: DepthFrame

    @classmethod
    def from_dict(cls, recorded):
        """Returns a decoded DepthFrame recording

        Args:
            recorded (dict): The dict of a mongo doc
        """
        return cls(
            timestamp=recorded["timestamp"],
            camera_id=recorded["camera_id"],
            rgb_frame=RGBFrame.from_dict(recorded),
            depth_frame=DepthFrame.from_dict(recorded),
        )


class DocObjectCodec:
    """Converts from mongo docs to python objs"""

    RECORDED_TYPES = {
        "depth": AggregatedDepth.from_dict,
        "targets": Targets.from_dict,
        "planogram": Facing.from_dict,
        "products": Product.from_dict,
        "plate_data": PlateData.from_dict,
        "frame_message": RGBFrame.from_dict,
    }

    @classmethod
    def decode(cls, doc, collection):
        """Returns a named tuple representing the doc"""
        return cls.RECORDED_TYPES[collection](doc)


class NumpyRecordCodec:
    """Converts between Numpy and Recorded DataArrays"""

    # Converts Recorded DataArray types to numpy types
    TYPE_DECODER = {
        "DATATYPE_INT8": np.int8,
        "DATATYPE_INT16": np.int16,
        "DATATYPE_INT32": np.int32,
        "DATATYPE_INT64": np.int64,
        "DATATYPE_UINT8": np.uint8,
        "DATATYPE_UINT16": np.uint16,
        "DATATYPE_UINT32": np.uint32,
        "DATATYPE_UINT64": np.uint64,
        "DATATYPE_FLOAT32": np.float32,
        "DATATYPE_FLOAT64": np.float64,
        "DATATYPE_BOOL": np.bool,
    }
    # Converts numpy types to Recorded DataArray types
    TYPE_ENCODER = {v: k for k, v in TYPE_DECODER.items()}

    @classmethod
    def decode(cls, data, shape, enc_type):
        """Returns a numpy array decoded from a recorded DataArray

        Args:
            data (str): base64 encoded byte array
            shape (list): shape of the byte array
            enc_type (str): the underlying datatype encoded
        """
        type_ = cls.TYPE_DECODER[enc_type]
        array = np.frombuffer(b64decode(data), dtype=type_)
        return array.reshape(shape)
