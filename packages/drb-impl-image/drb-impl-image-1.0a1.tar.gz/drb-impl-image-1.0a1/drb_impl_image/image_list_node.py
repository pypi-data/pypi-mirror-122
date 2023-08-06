from typing import Any, List, Dict, Optional, Tuple

from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
from drb.utils.logical_node import DrbLogicalNode


class DrbImageListNode(DrbLogicalNode):

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        raise NotImplementedError

    def __init__(self, parent: DrbNode, name: str):
        path = parent.path / name
        DrbLogicalNode.__init__(self, path)
        self._parent: DrbNode = parent
        self._children: List[DrbNode] = []

    def append_child(self, node: DrbNode) -> None:
        self.children.append(node)

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    def value(self) -> Any:
        return None

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        raise DrbNotImplementationException(f'no {impl} implementation found')
