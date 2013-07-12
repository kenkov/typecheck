#! /usr/bin/env python
# coding:utf-8

import ast
from pprint import pprint


def node_type(node: ast.AST) -> str:
    return node.__class__.__name__


def node_name(node: ast.AST) -> str:
    typ = node_type(node)
    if typ == "Name":
        return node.id
    elif typ == "Attribute":
        return attr_node_name(node)
    elif hasattr(node, "name"):
        return node.name
    else:
        return ""


def attr_node_name(node):
    typ = node.attr
    name = node_name(node.value)
    return ".".join([name, typ])


class Types(object):
    def __init__(self, tree):
        self.tree = tree
        self.scope_stack = [node_type(tree)]
        self.bindings = {}

    def check(self):
        self.check_node(self.tree)

    def check_node(self, node):
        if node_type(node) == "FunctionDef":
            info = self.function_def_info(node)
            self.bindings.update({
                ".".join(self.scope_stack): info})

        for item in ast.iter_child_nodes(node):
            self.scope_stack.append(node_name(item))
            self.check_node(item)
            self.scope_stack.pop()

    def function_def_info(self, node):
        func_binding = {}
        func_binding["args"] = []
        # args
        for arg in node.args.args:
            #typ = arg.annotation.id if arg.annotation else "undefined"
            #if arg.annotation:
            #    pprint(node_type(arg.annotation))
            #    pprint(arg.annotation.__dict__)
            #    if hasattr(arg.annotation, "value"):
            #        pprint(arg.annotation.value.__dict__)
            typ = node_name(arg.annotation)
            if typ == "":
                typ = "undefined"
            func_binding["args"].append(
                {"symbol": arg.arg, "type": typ})
        # returns
        ret = node.returns.id if node.returns else "undefined"
        func_binding["return"] = ret
        return func_binding


def compile_code(source):
    comp = compile(
        source,
        filename="<string>",
        mode="exec",
        flags=ast.PyCF_ONLY_AST)
    return comp


def test(source, ans):
    comp = compile_code(source)
    t = Types(comp)
    t.check()
    assert ans == t.bindings


def test_classfunc():
    source = """
class Hoge(object):
    def fuga(self, x: int, y) -> int:
        return x
"""
    ans = {
        'Module.Hoge.fuga': {'args': [{'symbol': 'self', 'type': 'undefined'},
                                      {'symbol': 'x', 'type': 'int'},
                                      {'symbol': 'y', 'type': 'undefined'}],
                             'return': 'int'}
        }
    test(source, ans)


def test_func():
    source = """
def fuga(self, x: int, y: str) -> int:
    return x
"""
    ans = {
        'Module.fuga': {'args': [{'symbol': 'self', 'type': 'undefined'},
                                 {'symbol': 'x', 'type': 'int'},
                                 {'symbol': 'y', 'type': 'str'}],
                        'return': 'int'}
    }
    test(source, ans)


def test_both():
    source = """
class Hoge(object):
    def fuga(self, x: int, y) -> int:
        return x
def hoge(self, x: int, y: str) -> int:
    return x
"""
    ans = {
        'Module.Hoge.fuga': {'args': [{'symbol': 'self', 'type': 'undefined'},
                                      {'symbol': 'x', 'type': 'int'},
                                      {'symbol': 'y', 'type': 'undefined'}],
                             'return': 'int'},
        'Module.hoge': {'args': [{'symbol': 'self', 'type': 'undefined'},
                                 {'symbol': 'x', 'type': 'int'},
                                 {'symbol': 'y', 'type': 'str'}],
                        'return': 'int'}
    }
    test(source, ans)


if __name__ == "__main__":
    # test
    test_classfunc()
    test_func()
    test_both()

    import sys

    filename = sys.argv[1]
    with open(filename, "r") as f:
        source = f.read()
        comp = compile_code(source)
        t = Types(comp)
        t.check()
        pprint(t.bindings)
