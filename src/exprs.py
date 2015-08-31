#!/usr/bin/env python3
# exprs.py ---
#
# Filename: exprs.py
# Author: Abhishek Udupa
# Created: Wed Aug 19 15:47:31 2015 (-0400)
#
#
# Copyright (c) 2015, Abhishek Udupa, University of Pennsylvania
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by The University of Pennsylvania
# 4. Neither the name of the University of Pennsylvania nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#

# Code:

"""Implements an expression type, along with a manager to create
expressions as needed
"""

import utils
import sys
import collections
from enum import IntEnum
import exprtypes

if __name__ == '__main__':
    utils.print_module_misuse_and_exit()

def ExpressionKinds(IntEnum):
    """Expression Kinds
    variable_expression: An expression representing a typed variable.
    constant_expression: An expression representing a typed constant.
    function_expression: An expression representing a function application.
    """
    variable_expression = 1
    constant_expression = 2
    function_expression = 3


_VariableExpression =
collections.namedtuple('VariableExpression', ['expr_kind', 'variable_info'])

_ConstantExpression =
collections.namedtuple('ConstantExpression', ['expr_kind', 'value_object'])

_FunctionExpression =
collections.namedtuple('FunctionExpression', ['expr_kind', 'function_info', 'children'])

_Value = collections.namedtuple('Value', ['value_object', 'value_type'])

def Value(value_object, value_type):
    return _Value(value_object, value_type)

def value_to_string(the_value):
    if (the_value.value_type.type_code == exprtypes.TypeCodes.boolean_type):
        if (the_value.value_object == True):
            return 'true'
        else:
            return 'false'
    elif (the_value.value_type.type_code == exprtypes.TypeCodes.integer_type):
        return str(the_value.value_object)
    elif (the_value.value_type.type_code == exprtypes.TypeCodes.bit_vector_type):
        return utils.bitvector_to_string(the_value.value_object, the_value.value_type.size)


class VariableInfo(object):
    __slots__ = ['variable_type', 'variable_eval_offset', 'variable_name']
    _undefined_offset = 1000000000

    def __init__(self, variable_type, variable_name):
        self.variable_name = variable_name
        self.variable_type = variable_type
        self.variable_eval_offset = _undefined_offset


def ExprManager(object):
    """A class for managing expression objects.
    Note that the expression types themselves are private.
    The only way to create expressions is thus intended to
    be through an instance of this class.
    Args:
    function_instantiator: an object that instantiates operators based on
    the name of the operator and types of the arguments provided to the operator.
    """

    def __init__(self, *function_instantiators):
        self.function_instantiators = function_instantiators
        self.variables_map = {}
        self.next_var_id = 1

    def make_variable_expr(self, var_type, var_name):
        """Makes a variable expression of the given name and type."""

        assert(isinstance(var_type, exprtypes.TypeBase))

        interned_var = sys.intern(var_name)
        var_id = self.variables_map.get(interned_var)
        if (var_id == None):
            self.variables_map[interned_var] = self.next_var_id
            var_id = self.next_var_id
            self.next_var_id += 1
        return _VariableExpression(ExpressionKinds.variable_expression, var_type, var_id)

    def make_constant_expr(self, const_type, const_value):
        """Makes a typed constant expression with the given value."""

        assert(isinstance(const_type, exprtypes.TypeBase))

        return _ConstantExpression(ExpressionKinds.constant_expression, const_type, const_value)

    def make_function_expr(self, function_name, *child_exps):
        "Makes a typed function expression applied to the given child expressions."""
        function_info = None
        for instantiator in self.function_instantiators:
            function_info = instantiator.instantiate_function(function_name, child_exps)
            if (function_info != None):
                break

        if (function_info == None):
            raise ArgumentError('Could not instantiate function named "' + function_name +
                                '" with argument types: (' +
                                ', '.join([str(x.expr_type) for x in child_exps]) + ')')

        return _FunctionExpression(ExpressionKinds.function_expression, function_info,
                                   tuple(child_exps))

    def make_true_expr(self):
        """Makes an expression representing the Boolean constant TRUE."""
        return _ConstantExpression(ExpressionKinds.constant_expression,
                                   exprtypes.BoolType(), True)

    def make_false_expr(self):
        """Makes an expression representing the boolean constant FALSE."""
        return _ConstantExpression(ExpressionKinds.constant_expression,
                                   exprtypes.BoolType(), True)

def _constant_to_string(constant_type, constant_value):
    if (constant_type == exprtypes.BoolType() or
        constant_type == exprtypes.IntType()):
        return str(constant_value)
    else:
        return utils.bitvector_to_string(constant_value, constant_type.size)


def expression_to_string(expr):
    """Returns a string representation of an expression"""

    if (expr.expr_kind == ExpressionKinds.variable_expression):
        return expr.var_name
    elif (expr.expr_kind == ExpressionKinds.constant_expression):
        return _constant_to_string(expr.expr_type, expr.const_value)
    else:
        retval = '(' + expr.function_info.function_name + ' '
        for child in expr.children:
            retval += expression_to_string(child)
            retval += ' '
        retval += ')'
        return retval


def get_expression_type(expr):
    """Returns the type of the expression."""

    if (expr.expr_kind == ExpressionKinds.variable_expression):
        return expr.variable_info.variable_type
    elif (expr.expr_kind == ExpressionKinds.constant_expression):
        return expr.value_object.value_type
    elif (expr.expr_kind == ExpressionKinds.function_expression):
        return expr.function_info.range_type
    else:
        raise basetypes.UnhandledCaseError('Odd expression kind: %s' % expr.expr_kind)

#
# exprs.py ends here
