import sys
import unittest
import os

from drb.factory import DrbFactoryResolver
from drb.node import DrbNode
from drb.factory.factory import DrbFactory, DrbFactoryCategory
from tests.utils import DrbTestNode


class DrbFactoryContainer(DrbFactory):
    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.CONTAINER

    def valid(self, uri: str) -> bool:
        return uri.endswith('.ext')

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNode(f'Container_{node.name}')


class DrbFactoryFormat(DrbFactory):
    @property
    def category(self) -> DrbFactoryCategory:
        return DrbFactoryCategory.FORMATTING

    def valid(self, uri: str) -> bool:
        return 'format' in uri

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbTestNode(f'Format_{node.name}')


class TestDrbFactoryResolverCategory(unittest.TestCase):
    system_path = os.path.join(os.getcwd(), 'resources', 'packages')

    def setUp(self) -> None:
        sys.path.append(TestDrbFactoryResolverCategory.system_path)

    def tearDown(self) -> None:
        sys.path.remove(TestDrbFactoryResolverCategory.system_path)

    def test_drb_factory_resolve_all_factories_category(self):
        resolver = DrbFactoryResolver()

        uri = "/path/to/my_file/toto.ext"
        families = {'cont': DrbFactoryContainer(),
                    'format': DrbFactoryFormat()}

        self.assertTrue(families['cont'].valid(uri=uri))

        factories = resolver._resolve_all_factories(uri, families)
        self.assertTrue(factories[0].create(uri).name.startswith("Container_"))

        uri = "/path/to/my_file/toto_format.ext"

        # check that the format category is prior to container category"
        self.assertTrue(families['cont'].valid(uri=uri))
        self.assertTrue(families['format'].valid(uri=uri))

        factories = resolver._resolve_all_factories(uri, families)
        self.assertTrue(factories[0].create(uri).name.startswith("Container_"))
        self.assertTrue(factories[1].create(uri).name.startswith("Format_"))

        # Check that the order of families have not influence
        families = {'format': DrbFactoryFormat(),
                    'cont': DrbFactoryContainer()}

        factories = resolver._resolve_all_factories(uri, families)
        self.assertTrue(factories[0].create(uri).name.startswith("Container_"))
        self.assertTrue(factories[1].create(uri).name.startswith("Format_"))

        # Check that the order of families have not influence
        families = {'format': DrbFactoryFormat()}

        factories = resolver._resolve_all_factories(uri, families)
        self.assertTrue(factories[0].create(uri).name.startswith("Format"))

        uri = "/path/to/my_file/toto_bad.no"
        factories = resolver._resolve_all_factories(uri, families)
        self.assertEqual(len(factories), 0)
