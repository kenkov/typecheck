#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import unittest
import ast
from expression import V


class ShowExprTest(unittest.TestCase):
    #@classmethod
    #def compile_code(source):
    #    comp = compile(
    #        source,
    #        filename="<string>",
    #        mode="exec",
    #        #mode="eval",
    #        flags=ast.PyCF_ONLY_AST)
    #    return comp

    def compile_eval_code(self, source):
        comp = compile(
            source,
            filename="<string>",
            mode="eval",
            flags=ast.PyCF_ONLY_AST)
        return comp

    def expr(self, source):
        comp = self.compile_eval_code(source)
        v = V()
        return v.visit(comp)

    def check(self, source_list):
        for source in source_list:
            ans = self.expr(source)
            self.assertEqual(ans, source)

    def test_BoolOp(self):
        source = ["True and False or True"]
        self.check(source)

    def test_BinOp(self):
        source_list = ["1 + 2", "1 - 2", "1 * 2", "1 % 2", "2 ** 3", "2 << 3",
                       "2 >> 3", "1 | 2", "1 ^ 2", "1 & 2", "1 // 2"]
        self.check(source_list)

    def test_UnaryOp(self):
        source_list = ["- 1", "+ 3", "~ 2", "not True"]
        self.check(source_list)

    def test_Lambda(self):
        source = ["lambda x: x * x",
                  "lambda x, y: x + y",
                  "lambda x=3: x * x",
                  "lambda w, x=3, y=4: x * x"]
        self.check(source)

    def test_IfExp(self):
        source = ["1 if True else 2",
                  "1 if True and False else 2"]
        self.check(source)

    def test_Dict(self):
        source = ['{1:3, 2:4}']
        self.check(source)

    def test_Set(self):
        source = ['{1, 2, 3, 4}']
        self.check(source)

    def test_List(self):
        source = ['[1, 2, 3, 4]']
        self.check(source)

    def test_Tuple(self):
        source = ['(1, 2, 3, 4)']
        self.check(source)

    def test_ListComp(self):
        source = ['[x for x in [1, 2, 3]]',
                  '[x for x in [1, 2, 3] if x % 2]']
        self.check(source)

    def test_SetComp(self):
        source = ['{x for x in [1, 2, 3]}',
                  '{x for x in [1, 2, 3] if x % 2}']
        self.check(source)

    def test_DictComp(self):
        source = ['{x: x for x in [1, 2, 3]}',
                  '{x: x for x in [1, 2, 3] if x % 2}']
        self.check(source)

    def test_GeneratorComp(self):
        source = ['(x for x in [1, 2, 3])']
        self.check(source)

    # Yield and YieldFrom should be used in function
    #def test_Yield(self):
    #    source = ['yield True',
    #              'yield']
    #    self.check(source)
    #
    #
    #def test_YieldFrom(self):
    #    source = ['yield from [1, 2, 3]']
    #    self.check(source)

    def test_Compare(self):
        source = ['1 < 2',
                  '1 < 2 < 3',
                  # Error raised
                  # '1 < (2 < 3)
                  ]
        self.check(source)

    def test_Call(self):
        source = [
            # The following expressions raise error
            # when running
            'dir(object, x=1)',
            'dir(object, 1, 2, x=1, y=2)'
        ]
        self.check(source)

    def test_Str(self):
        source = [
            "'fuga'",
            # error raised in the following tests
            #'"fuga"',
            #"\"'fuga'\""
        ]
        self.check(source)

    def test_Bytes(self):
        source = [
            "b'hello'",
        ]
        self.check(source)

    def test_Ellipsis(self):
        source = [
            "Ellipsis",
        ]
        self.check(source)

    def test_Attribute(self):
        source = [
            "hoge.fuga",
            "hoge.fuga.hogefuga",
            "hoge.fuga()"]
        self.check(source)

    def test_Subscript(self):
        source = [
            # slice
            "o[1:2:3]",
            "o[1::]",
            "o[:2:]",
            "o[::3]",
            "o[1:2:]",
            "o[:2:3]",
            "o[1::3]",
            "o[::]",
            # index
            "o[1]",
            # extslice
            "o[::, ::]",
            "o[1:2:3, 4:5:6]"
        ]
        self.check(source)

    def test_Starred(self):
        source = [
            #"*[1, 2, 3]"
        ]
        self.check(source)


if __name__ == '__main__':
    unittest.main()
