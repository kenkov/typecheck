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

    def show_ListComp(self, node):
        return "[{} {}]".format(
            self.show(node.elt),
            " ".join(map(self.show, node.generators)))

    def show_SetComp(self, node):
        return "{{{} {}}}".format(
            self.show(node.elt),
            " ".join(map(self.show, node.generators)))

    def show_DictComp(self, node):
        return "{{{} {}}}".format(
            ": ".join([self.show(node.key), self.show(node.value)]),
            " ".join(map(self.show, node.generators)))

    def show_GeneratorExp(self, node):
        return "({} {})".format(
            self.show(node.elt),
            " ".join(map(self.show, node.generators)))

    def show_Num(self, node):
        return str(node.n)

    def show_Name(self, node):
        return node.id

    def show_List(self, node):
        return "[{}]".format(
            ", ".join(map(self.show, node.elts)))

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

    # comprehension = (expr target, expr iter, expr* ifs)
    def show_comprehension(self, node):
        ifs = node.ifs
        if ifs:
            return "for {} in {} {}".format(
                self.show(node.target),
                self.show(node.iter),
                " ".join(["if {}".format(item)
                          for item in map(self.show, ifs)]))
        else:
            return "for {} in {}".format(
                self.show(node.target),
                self.show(node.iter))

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


if __name__ == "__main__":
    pass
