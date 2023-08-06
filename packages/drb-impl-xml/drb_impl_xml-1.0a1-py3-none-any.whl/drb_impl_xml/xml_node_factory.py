from io import BufferedIOBase

from drb import DrbNode
from .xml_node import XmlBaseNode
from drb.factory.factory import DrbFactory, DrbFactoryCategory


class XmlNodeFactory(DrbFactory):

    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.CONTAINER

    def valid(self, uri: str) -> bool:
        return uri.lower().endswith('.xml')

    def _create(self, node: DrbNode) -> DrbNode:
        return XmlBaseNode(node, node.get_impl(BufferedIOBase))
