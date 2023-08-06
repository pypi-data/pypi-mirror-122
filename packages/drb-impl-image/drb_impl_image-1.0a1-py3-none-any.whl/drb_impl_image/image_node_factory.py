import os
from typing import Any, Optional, List

from drb import DrbNode
from drb.factory import DrbFactory
from drb.factory.factory import DrbFactoryCategory
from drb.utils.logical_node import DrbLogicalNode

from drb_impl_image.image_node import DrbImageNode


class DrbImageBaseNode(DrbLogicalNode):

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        raise NotImplementedError

    def __init__(self, base_node: DrbNode):
        DrbLogicalNode.__init__(self, source=base_node)
        self.base_node = base_node
        self._children = [DrbImageNode(self)]

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    def close(self):
        if self._children is not None:
            self._children[0].close()
        self.base_node.close()

    def has_impl(self, impl: type) -> bool:
        return self._wrapped_node.has_impl(impl)

    def get_impl(self, impl: type) -> Any:
        return self._wrapped_node.get_impl(impl)


class DrbImageFactory(DrbFactory):

    supported_ext = {
        '.tif',
        '.image',
        '.jp2',
        '.png'
    }

    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.CONTAINER

    def valid(self, uri: str) -> bool:
        filename, file_extension = os.path.splitext(uri)
        return file_extension and file_extension.lower() in self.supported_ext

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbImageBaseNode(base_node=node)
