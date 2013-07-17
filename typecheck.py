#! /usr/bin/env python
# coding:utf-8

import ast
import expression as expr


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


def stack(func):
    def ret(self, node):
        self.scope.append(node_type(node))
        #print(self.scope)
        func(self, node)
        self.scope.pop()
    return ret


class ShowTypes(ast.NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.scope = []
        self.bindings = {}
        self.show_expr = expr.ShowExpr()
        self.show_stmt = expr.ShowStmt()

    def check(self):
        self.visit(self.tree)

    @stack
    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    @stack
    def visit_FunctionDef(self, node):
        print(self.show_stmt.show(node))

    @stack
    def visit_ClassDef(self, node):
        for nd in ast.iter_child_nodes(node):
            if node_type(nd) == "FunctionDef":
                print("{}.{}".format(
                    node.name,
                    self.show_stmt.show(nd)))


def compile_code(source):
    comp = compile(
        source,
        filename="<string>",
        mode="exec",
        flags=ast.PyCF_ONLY_AST)
    return comp


if __name__ == "__main__":

    import sys

    filename = sys.argv[1]
    with open(filename, "r") as f:
        source = f.read()
        comp = compile_code(source)
        t = ShowTypes(comp)
        t.check()
