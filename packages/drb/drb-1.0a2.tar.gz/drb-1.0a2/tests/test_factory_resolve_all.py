import sys
import unittest
import os
from pathlib import PurePath
from typing import Optional, Any, List, Union

from drb.node import DrbNode
from drb.factory.factory import DrbFactory, DrbFactoryCategory
from drb.factory.factory_resolver import DrbFactoryResolver
from drb.path import Path
from drb.utils.logical_node import DrbLogicalNode


class DrbFactoryContainer(DrbFactory):
    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.CONTAINER

    def valid(self, uri: str) -> bool:
        return uri.endswith('.ext')

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNodeNamed(f'Container_{node.name}', node)


class DrbFactoryFormat(DrbFactory):
    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.FORMATTING

    def valid(self, uri: str) -> bool:
        return 'format' in uri

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNodeNamed(f'Format_{node.name}', node)


class DrbTestNodeWithChildren(DrbLogicalNode):
    def __init__(self, source: Union[DrbNode, str, Path, PurePath]):
        DrbLogicalNode.__init__(self, source=source)
        self._children = [DrbTestNodeNamed('Child1.ext', self),
                          DrbTestNodeNamed('Child2.no', self),
                          DrbTestNodeNamed('Child3_format.ext', self)]

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        pass

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        pass

    @property
    def children(self) -> List[DrbNode]:
        return self._children


class DrbTestNodeNamed(DrbLogicalNode):
    def __init__(self, name: str, source: Union[DrbNode, str, Path, PurePath]):
        DrbLogicalNode.__init__(self, source=source)
        self._children = []
        self._name = name

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        pass

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        pass

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    @property
    def name(self) -> str:
        return self._name


class ProtoFactory(DrbFactory):
    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.PROTOCOL

    def valid(self, uri: str) -> bool:
        return True

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNodeWithChildren(node.path.path)


class DrbFactoryResolverTest(DrbFactoryResolver):
    families = {'cont': DrbFactoryContainer(),
                'format': DrbFactoryFormat(),
                'proto': ProtoFactory()}

    @classmethod
    def resolve(cls, uri: str, cat: DrbFactoryCategory = None) -> DrbFactory:
        factories = cls._resolve_all_factories(uri, cls.families, cat)
        if len(factories) > 0:
            return factories[0]
        return None

    @classmethod
    def resolve_all_factories(cls, uri: str, cat: DrbFactoryCategory = None) \
            -> List[DrbFactory]:
        return cls._resolve_all_factories(uri, cls.families, cat)


class TestDrbFactoryResolverCategory(unittest.TestCase):
    system_path = os.path.join(os.getcwd(), 'resources', 'packages')

    @classmethod
    def setUp(cls) -> None:
        sys.path.append(TestDrbFactoryResolverCategory.system_path)

    @classmethod
    def tearDown(cls) -> None:
        sys.path.remove(TestDrbFactoryResolverCategory.system_path)

    @unittest.skip("Skip due to pb of compatibility with others tests")
    def test_drb_factory_resolve_protocol_with_children(self):
        resolver = DrbFactoryResolverTest()

        uri = "/path/to/my_file/toto"

        node = resolver.resolve_all(uri)

        print(node.__class__)
        print(node.get_children_count())

        node_child1 = node.get_named_child('Container_Child1.ext',
                                           occurrence=1)
        self.assertIsNotNone(node_child1)
        self.assertFalse(node_child1.has_child())

        node_child2 = node.get_named_child('Child2.no', occurrence=1)
        self.assertIsNotNone(node_child2)
        self.assertFalse(node_child2.has_child())

        node_child3 = node.get_named_child(
            'Format_Container_Child3_format.ext', occurrence=1)
        self.assertIsNotNone(node_child3)
