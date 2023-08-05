# Relational
# Copyright (C) 2008-2020  Salvo "LtWorf" Tomaselli
#
# Relational is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>
#
# This module optimizes relational expressions into ones that require less time to be executed.
#
# expression: In all the functions expression can be either an UTF-8 encoded string, containing a valid
# relational query, or it can be a parse tree for a relational expression (ie: class parser.node).
# The functions will always return a string with the optimized query, but if a parse tree was provided,
# the parse tree itself will be modified accordingly.
from typing import Union, Optional, Dict, Any, Tuple

from relation import Relation
import optimizations
from parser import Node, Variable, Unary, Binary, op_functions, tokenize, tree
import querysplit
from maintenance import UserInterface


def optimize_program(code: str, rels: Dict[str, Relation]) -> str:
    '''
    Optimize an entire program, composed by multiple expressions
    and assignments.
    '''
    lines = code.split('\n')
    context: Dict[str, Node] = {}

    last_res = None
    for line in lines:
        # skip comments or empty lines
        line = line.strip()
        if line.startswith(';') or not line:
            continue


        res, query = UserInterface.split_query(line)
        last_res = res
        parsed = tree(query)
        _replace_leaves(parsed, context)
        context[res] = parsed

    if last_res is None:
        return ''
    node = optimize_all(context[last_res], rels, tostr=False)
    return querysplit.split(node, rels)


def _replace_leaves(node: Node, context: Dict[str, Node]) -> None:
    '''
    If a name appearing in node appears
    also in context, the parse tree is
    modified to replace the node with the
    subtree found in context.
    '''
    if isinstance(node, Unary):
        _replace_leaves(node.child, context)

        if isinstance(node.child, Variable) and node.child.name in context:
            node.child = context[node.child.name]
    elif isinstance(node, Binary):
        _replace_leaves(node.left, context)
        _replace_leaves(node.right, context)
        if isinstance(node.left, Variable) and node.left.name in context:
            node.left = context[node.left.name]
        if isinstance(node.right, Variable) and node.right.name in context:
            node.right = context[node.right.name]


def optimize_all(expression: Union[str, Node], rels: Dict[str, Relation], specific: bool = True, general: bool = True, debug: Optional[list] = None, tostr: bool = True) -> Union[str, Node]:
    '''This function performs all the available optimizations.

    expression : see documentation of this module
    rels: dic with relation name as key, and relation istance as value
    specific: True if it has to perform specific optimizations
    general: True if it has to perform general optimizations
    debug: if a list is provided here, after the end of the function, it
        will contain the query repeated many times to show the performed
        steps.

    Return value: this will return an optimized version of the expression'''
    if isinstance(expression, str):
        n = tree(expression)  # Gets the tree
    elif isinstance(expression, Node):
        n = expression
    else:
        raise TypeError('expression must be a string or a node')

    total = 1
    while total != 0:
        total = 0
        if specific:
            for i in optimizations.specific_optimizations:
                n, c = _recursive_scan(i, n, rels)
                if c != 0 and isinstance(debug, list):
                    debug.append(str(n))
                total += c
        if general:
            for j in optimizations.general_optimizations:
                n, c = _recursive_scan(j, n, None)
                if c != 0 and isinstance(debug, list):
                    debug.append(str(n))
                total += c
    if tostr:
        return str(n)
    else:
        return n


def _recursive_scan(function, node: Node, rels: Optional[Dict[str, Any]]) -> Tuple[Node, int]:
    '''Does a recursive optimization on the tree.

    This function will recursively execute the function given
    as "function" parameter starting from node to all the tree.
    if rels is provided it will be passed as argument to the function.
    Otherwise the function will be called just on the node.

    Result value: function is supposed to return the amount of changes
    it has performed on the tree.
    The various result will be added up and this final value will be the
    returned value.'''

    args = []
    if rels is not None:
        args.append(rels)

    changes = 0
    node, c = function(node, *args)
    changes += c

    if isinstance(node, Unary):
        node.child, c = _recursive_scan(function, node.child, rels)
        changes += c
    elif isinstance(node, Binary):
        node.left, c = _recursive_scan(function, node.left, rels)
        changes += c
        node.right, c = _recursive_scan(function, node.right, rels)
        changes += c
    return node, changes
