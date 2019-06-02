#!/usr/bin/env python3

# pylint: disable=missing-docstring
# pylint: disable=wrong-spelling-in-comment

import unittest

from winpathlib import to_posix_path


class TestPathConversion(unittest.TestCase):

    def test_dot(self):
        self.assertEqual(to_posix_path('.'), '.')

    def test_dots(self):
        self.assertEqual(to_posix_path('..'), '..')

    def test_dots_2(self):
        self.assertEqual(to_posix_path('.\\..'), '..')
        self.assertEqual(to_posix_path('..\\..'), '../..')

    def test_simple_paths(self):
        self.assertEqual(to_posix_path('tests'), 'tests')
        self.assertEqual(to_posix_path('TeStS'), 'tests')

    def test_longer_paths_1(self):
        win_path = 'TESTS\\FILES\\CONFS\\ABC\\DEF\\FILE'
        lin_path = 'tests/files/confs/abc/DEF/file'
        self.assertEqual(to_posix_path(win_path), lin_path)

    def test_longer_paths_2(self):
        win_path = 'tests\\files\\case\\dosbox.conf'
        lin_path = 'tests/files/case/DoSbOx.CoNf'
        self.assertEqual(to_posix_path(win_path), lin_path)

    def test_missing_path(self):
        win_path = 'tests\\files\\case\\dosbox.confz'
        self.assertEqual(to_posix_path(win_path), None)

    @unittest.skip("implementation is too slow")
    def test_really_long_path(self):
        path = 'tests/files/somewhat_long_path/'
        file = 'With Much Much Longer Path Inside ' + \
               'AbcDefGhiJklMnoPqrStuVwxYz_0123456789.tXt'
        win_path = (path + file).replace('\\', '/').upper()
        self.assertEqual(to_posix_path(win_path), path + file)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
