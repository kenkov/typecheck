#! /usr/bin/env python
# coding:utf-8

from __future__ import division
import ast
from pprint import pprint


def node_name(node: ast.AST) -> str:
    if hasattr(node, "id"):
        return node.id
    elif hasattr(node, "name"):
        return node.name
    else:
        return ""


def node_type(node: ast.AST) -> str:
    return node.__class__.__name__


class ShowExpr:
    def __init__(self):
        pass

    def show(self, node: ast.expr) -> str:
        try:
            fun = getattr(self, "{}_{}".format("show", node_type(node)))
            return fun(node)
        except AttributeError:
            raise

    # expr = BoolOp(boolop op, expr* values)
    #          | BinOp(expr left, operator op, expr right)
    #          | UnaryOp(unaryop op, expr operand)
    #          | Lambda(arguments args, expr body)
    #          | IfExp(expr test, expr body, expr orelse)
    #          | Dict(expr* keys, expr* values)
    #          | Set(expr* elts)
    #          | ListComp(expr elt, comprehension* generators)
    #          | SetComp(expr elt, comprehension* generators)
    #          | DictComp(expr key, expr value, comprehension* generators)
    #          | GeneratorExp(expr elt, comprehension* generators)
    #          -- the grammar constrains where yield expressions can occur
    #          | Yield(expr? value)
    #          | YieldFrom(expr value)
    #          -- need sequences for compare to distinguish between
    #          -- x < 4 < 3 and (x < 4) < 3
    #          | Compare(expr left, cmpop* ops, expr* comparators)
    #          | Call(expr func, expr* args, keyword* keywords,
    #              expr? starargs, expr? kwargs)
    #          | Num(object n) -- a number as a PyObject.
    #          | Str(string s) -- need to specify raw, unicode, etc?
    #          | Bytes(bytes s)
    #          | Ellipsis
    #          -- other literals? bools?
    def show_BoolOp(self, node):
        boolop = self.show(node.op)
        return "".join([" ", boolop, " "]).join(
            self.show(value) for value in node.values)

    def show_BinOp(self, node):
        return "{} {} {}".format(
            self.show(node.left),
            self.show(node.op),
            self.show(node.right))

    def show_UnaryOp(self, node):
        return "{} {}".format(
            self.show(node.op),
            self.show(node.operand))

    def show_Lambda(self, node):
        return "lambda {}: {}".format(
            self.show(node.args),
            self.show(node.body))

    def show_IfExp(self, node):
        return "{} if {} else {}".format(
            self.show(node.body),
            self.show(node.test),
            self.show(node.orelse))

    def show_Dict(self, node):
        st = ", ".join(
            map(":".join,
                zip(map(self.show, node.keys),
                    map(self.show, node.values))))
        return "{{{}}}".format(st)

    def show_Set(self, node):
        return "{{{}}}".format(
            ", ".join(map(self.show, node.elts)))

    def show_Num(self, node):
        return str(node.n)

    def show_Name(self, node):
        return node.id

    # boolop = And | Or
    def show_Or(self, node):
        return "or"

    def show_And(self, node):
        return "and"

    # operator = Add | Sub | Mult | Div | Mod | Pow | LShift
    #                | RShift | BitOr | BitXor | BitAnd | FloorDiv
    def show_Add(self, node):
        return "+"

    def show_Sub(self, node):
        return "-"

    def show_Mult(self, node):
        return "*"

    def show_Mod(self, node):
        return "%"

    def show_Pow(self, node):
        return "**"

    def show_LShift(self, node):
        return "<<"

    def show_RShift(self, node):
        return ">>"

    def show_BitOr(self, node):
        return "|"

    def show_BitXor(self, node):
        return "^"

    def show_BitAnd(self, node):
        return "&"

    def show_FloorDiv(self, node):
        return "//"

    # unaryop = Invert | Not | UAdd | USub
    def show_Invert(self, node):
        return "~"

    def show_Not(self, node):
        return "not"

    def show_UAdd(self, node):
        return "+"

    def show_USub(self, node):
        return "-"

    # arguments = (arg* args, identifier? vararg, expr? varargannotation,
    #              arg* kwonlyargs, identifier? kwarg,
    #              expr? kwargannotation, expr* defaults,
    #              expr* kw_defaults)
    def show_arguments(self, node):
        # MUST implement keyword-only-argument ...
        args = list(map(self.show, node.args))
        defaults = list(map(self.show, node.defaults))

        sep = len(args) - len(defaults)
        lst = args[:sep] + \
            list(map("=".join, list(zip(args[sep:],
                                        defaults))))
        return ", ".join(lst)

    def show_arg(self, node):
        if node.annotation:
            return "{}: {}".format(
                node.arg,
                self.show(node.annotation))
        else:
            return node.arg


class V(ast.NodeVisitor):
    def __init__(self):
        self.funcs = {}
        self.class_funcs = {}
        self.scope = []
        self.expr = ShowExpr()

    def visit_Expression(self, node):
        return self.expr.show(node.body)

    #def visit_Module(self, node):
    #    self.generic_visit(node)

    #def visit_Interactive(self, node):
    #    pass

    #def visit_Expression(self, node):
    #    pass

    def visit_Load(self, node):
        pass

    def generic_visit(self, node):
        #pprint("{}: {}".format(node.__class__.__name__,
        #                       node.__dict__))
        self.scope.append(node_type(node))
        pprint(self.scope)
        pprint(node.__dict__)
        #pprint("---")
        ast.NodeVisitor.generic_visit(self, node)
        self.scope.pop()


def compile_code(source):
    comp = compile(
        source,
        filename="<string>",
        mode="exec",
        #mode="eval",
        flags=ast.PyCF_ONLY_AST)
    return comp


def compile_eval_code(source):
    comp = compile(
        source,
        filename="<string>",
        mode="eval",
        flags=ast.PyCF_ONLY_AST)
    return comp


def test_expr(source):
    comp = compile_eval_code(source)
    v = V()
    return v.visit(comp)


def test(source_list):
    for source in source_list:
        ans = test_expr(source)
        assert ans == source, "'{}' and '{}' is not equal".format(ans, source)


def test_BoolOp():
    source = ["True and False or True"]
    test(source)


def test_BinOp():
    source_list = ["1 + 2", "1 - 2", "1 * 2", "1 % 2", "2 ** 3", "2 << 3",
                   "2 >> 3", "1 | 2", "1 ^ 2", "1 & 2", "1 // 2"]
    test(source_list)


def test_UnaryOp():
    source_list = ["- 1", "+ 3", "~ 2", "not True"]
    test(source_list)


def test_Lambda():
    source = ["lambda x: x * x",
              "lambda x, y: x + y",
              "lambda x=3: x * x",
              "lambda w, x=3, y=4: x * x"]
    test(source)


def test_IfExp():
    source = ["1 if True else 2",
              "1 if True and False else 2"]
    test(source)


def test_Dict():
    source = ['{1:3, 2:4}']
    test(source)


def test_Set():
    source = ['{1, 2, 3, 4}']
    test(source)


if __name__ == "__main__":

    test_BoolOp()
    test_BinOp()
    test_UnaryOp()
    test_Lambda()
    test_IfExp()
    test_Dict()
    test_Set()
