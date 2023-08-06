import posixpath
import re
from typing import Optional, Any, Union, List, Dict, Tuple

import drb
from typing.io import IO
from xml.etree.ElementTree import parse, Element
from io import BufferedIOBase, RawIOBase

from drb import DrbNode
from drb.exceptions import DrbNotImplementationException, DrbException
from drb.path import Path
from drb.utils.logical_node import DrbLogicalNode


def extract_namespace_name(value: str) -> Tuple[str, str]:
    """
    Extracts namespace and name from a tag of a Element
    :param value: XML element tag
    :type value: str
    :return: a tuple containing the extracted namespace and name
    :rtype: tuple
    """
    ns, name = re.match(r'({.*})?(.*)', value).groups()
    if ns is not None:
        ns = ns[1:-1]
    return ns, name


class XmlNode(DrbNode):
    @property
    def path(self) -> Path:
        if self._path is None:
            self._path = self._parent.path / self._name
        return self._path

    def __init__(self, element: Element, parent: DrbNode = None):
        self._parent = parent
        self._elem: Element = element
        self._namespace, self._name = extract_namespace_name(element.tag)
        self._attrs: Dict[Tuple[str, str], Any] = None
        self._children: List[XmlNode] = None
        self._path = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self._namespace

    @property
    def value(self) -> Optional[Any]:
        if self.has_child():
            return None
        return self._elem.text

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attrs is None:
            self._attrs = {}
            for k, v in self._elem.attrib.items():
                ns, name = extract_namespace_name(k)
                self._attrs[(name, ns)] = v
        return self._attrs

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = [XmlNode(e, self) for e in list(self._elem)]
        return self._children

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        return self.attributes[(name, namespace_uri)]

    def has_child(self) -> bool:
        return len(list(self._elem)) > 0

    def get_named_child(self, name: str, namespace_uri: str = None,
                        occurrence: int = None) -> Union[DrbNode,
                                                         List[DrbNode]]:
        try:
            found = [child for child in self.children
                     if child.name == name
                     and child.namespace_uri == namespace_uri]
            if occurrence is None and len(found) > 0:
                return [node for node in found]
            if occurrence > 0:
                return found[occurrence - 1]
            else:
                raise DrbException(f'Child ({name},{occurrence}) not found')
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child ({name},{occurrence}) not found') \
                from error

    def get_first_child(self) -> Optional[DrbNode]:
        if self.has_child():
            try:
                return XmlNode(self._elem[0], self)
            except (IndexError, TypeError) as error:
                raise DrbException(f'First child not found') from error
        raise DrbException(f'First child not found')

    def get_last_child(self) -> Optional[DrbNode]:
        if self.has_child():
            try:
                return XmlNode(self._elem[-1], self)
            except (IndexError, TypeError) as error:
                raise DrbException(f'Last child not found') from error
        raise DrbException(f'Last child not found')

    def get_child_at(self, index: int) -> DrbNode:
        try:
            return XmlNode(self._elem[index], self)
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    def get_children_count(self) -> int:
        return len(list(self._elem))

    def insert_child(self, node: DrbNode, index: int) -> None:
        raise NotImplementedError

    def append_child(self, node: DrbNode) -> None:
        raise NotImplementedError

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        raise NotImplementedError

    def remove_child(self, index: int) -> None:
        raise NotImplementedError

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        raise NotImplementedError

    def has_impl(self, impl: type) -> bool:
        return impl == str and not self.has_child()

    def get_impl(self, impl: type) -> Any:
        if self.has_impl(impl):
            return self.value
        raise DrbNotImplementationException(
            f"XmlNode doesn't implement {impl}")

    def close(self) -> None:
        pass


class XmlBaseNode(DrbLogicalNode):

    def __init__(self, node: DrbNode,
                 source: Union[BufferedIOBase, RawIOBase, IO]):
        """
        The given source is closed via this class #close() method.
        """
        DrbLogicalNode.__init__(self, source=node)
        self.base_node = node
        self.source = source
        xml_root = parse(source).getroot()
        self.xml_node = XmlNode(xml_root, parent=node)

    @property
    def children(self) -> List[DrbNode]:
        return [self.xml_node]

    def has_child(self) -> bool:
        return True

    def get_named_child(self, name: str, namespace_uri: str = None,
                        occurrence: int = None) -> Union[DrbNode,
                                                         List[DrbNode]]:
        try:
            if self.xml_node.name == name and \
                    self.xml_node.namespace_uri == namespace_uri:
                if occurrence is None:
                    return [self.xml_node]
                elif occurrence == 1:
                    return self.xml_node
            raise DrbException(f'Child ({name},{occurrence}) not found')
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child ({name},{occurrence}) not found') \
                from error

    def get_first_child(self) -> Optional[DrbNode]:
        return self.xml_node

    def get_last_child(self) -> Optional[DrbNode]:
        return self.xml_node

    def get_children_count(self) -> int:
        return 1

    def close(self) -> None:
        if self.source:
            self.source.close()
        # TBC: shall the base node be closes by base node creator (?)
        self.base_node.close()

    def insert_child(self, node: DrbNode, index: int) -> None:
        raise NotImplementedError

    def append_child(self, node: DrbNode) -> None:
        raise NotImplementedError

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        raise NotImplementedError

    def remove_child(self, index: int) -> None:
        raise NotImplementedError

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        raise NotImplementedError

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        raise NotImplementedError
