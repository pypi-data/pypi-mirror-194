from unittest import TestCase

from utils import Directory, File


class TestDirectory(TestCase):
    def test_init(self):
        dir_tests = Directory('src/utils')
        self.assertEqual(dir_tests.path, 'src/utils')
        self.assertEqual(dir_tests.name, 'utils')
        self.assertEqual(dir_tests.children[0], File('src/utils/Browser.py'))

        self.assertEqual(dir_tests, Directory('src/utils'))
