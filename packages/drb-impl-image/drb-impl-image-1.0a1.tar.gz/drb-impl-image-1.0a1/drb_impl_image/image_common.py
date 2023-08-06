import enum
from typing import Optional, List, Any, Dict, Tuple

from drb import DrbNode
from drb.exceptions import DrbException
from drb.utils.logical_node import DrbLogicalNode


class DrbImageNodesValueNames(enum.Enum):
    IMAGE = 'image'
    TAGS = 'tags'
    FORMAT = 'FormatName'
    WIDTH = 'width'
    HEIGHT = 'height'
    NUM_BANDS = 'NumBands'
    TYPE = 'Type'
    BOUNDARIES = 'Boundaries'
    CRS = 'crs'
    META = 'meta'


class DrbImageSimpleValueNode(DrbLogicalNode):

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str,
                         namespace_uri: str = None) -> None:
        raise NotImplementedError

    def __init__(self, parent: DrbNode, name: str, value: any):
        path = parent.path / name
        DrbLogicalNode.__init__(self, path)
        self._parent = parent
        self._value = value
        self._wrapped_node = None

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'No attribute {name} found')

    @property
    def children(self) -> List[DrbNode]:
        return None
