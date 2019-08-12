#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test cases for Foma Python bindings.
"""

import unittest
from grammar_fst.Foma.foma import FST


class TestFST(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_fst = FST.load('english.fst')

    def test_load_fst(self):
        print(self.test_fst)
        assert isinstance(self.test_fst, FST)

    def test_apply_fst(self):
        result = self.test_fst.apply_up('tries')
        self.assertEqual(list(result), ['try+V+3P+Sg', 'try+N+Pl'])

    def test_apply_down(self):
        result = self.test_fst.apply_down('try+N+Pl')
        self.assertEqual(list(result), ['tries'])


if __name__ == '__main__':
    unittest.main()
