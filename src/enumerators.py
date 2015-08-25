#!/usr/bin/env python3
# enumerators.py ---
#
# Filename: enumerators.py
# Author: Abhishek Udupa
# Created: Tue Aug 25 11:44:38 2015 (-0400)
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

import utils
import basetypes
import copy
import itertools

# if __name__ == '__main__':
#     utils.print_module_misuse_and_exit()

def _cartesian_product_of_generators(*generators):
    """A generator that produces the cartesian product of the input
    "sub-generators."""
    tuple_size = len(generators)
    if (tuple_size == 1):
        for elem in generators[0].generate():
            yield (elem, )

    else:
        for sub_tuple in _cartesian_product_of_generators(*generators[1:]):
            for elem in generators[0].generate():
                yield (elem, ) + sub_tuple

class _DefaultObjectValidator(object):
    def __init__(self):
        pass

    def validate(self, object):
        return True

class GeneratorBase(object):
    object_counter = 0

    def __init__(self, object_validator = None, name = None):

        if (object_validator != None):
            self.object_validator = object_validator
        else:
            self.object_validator = _DefaultObjectValidator()

        if (name != None or name != ''):
            self.name = name
        else:
            self.name = 'AnonymousGenerator_%d' % self.object_counter
        self.object_counter += 1

    def generate(self):
        raise basetypes.AbstractMethodError('GeneratorBase.generate()')

    def set_size(self, new_size):
        raise basetypes.AbstractMethodError('GeneratorBase.set_size()')

    def clone(self):
        raise basetypes.AbstractMethodError('GeneratorBase.clone()')


class LeafGenerator(GeneratorBase):
    """A generator for leaf objects.
    Variables, constants and the likes."""

    def __init__(self, leaf_objects, object_validator = None, name = None):
        super().__init__(object_validator, name)
        self.leaf_objects = list(leaf_objects)
        self.iterable_size = len(self.leaf_objects)
        self.allowed_size = 0

    def generate(self):
        current_position = 0
        if (self.allowed_size != 1):
            return

        while (current_position < self.iterable_size):
            retval = self.leaf_objects[current_position]
            current_position += 1
            if (self.object_validator.validate(retval)):
                yield retval

    def set_size(self, new_size):
        self.allowed_size = new_size

    def clone(self):
        return LeafGenerator(self.leaf_objects, self.object_validator, self.name)


class FunctionalGenerator(GeneratorBase):
    """A generator for function objects.
    Accepts a function symbol and a list of "sub-generators"
    and builds expressions rooted with the function symbol, where
    the arguments to the function are the expressions generated by
    the "sub-generators".
    The "sub-generators and function symbol can be changed after construction,
    this is useful in the case of recursive generators."""

    def __init__(self, function_descriptor, sub_generators,
                 object_validator = None, name = None):
        assert (len(sub_generators) >= 1)

        super().__init__(object_validator, name)
        self.function_descriptor = function_descriptor
        self.sub_generators = [x.clone() for x in sub_generators]
        self.arity = len(self.sub_generators)
        self.allowed_size = 0

    def set_size(self, new_size):
        self.allowed_size = new_size

    def _set_sub_generator_sizes(self, partition):
        assert (len(partition) == self.arity)

        for i in range(self.arity):
            self.sub_generators[i].set_size(partition[i])
        return

    def generate(self):
        if (self.allowed_size - 1 < self.arity):
            return

        # self.allowed_size - 1 >= self.arity
        for partition in utils.partitions(self.allowed_size - 1, self.arity):
            self._set_sub_generator_sizes(partition)
            for product_tuple in _cartesian_product_of_generators(*self.sub_generators):
                retval = (self.function_descriptor, ) + product_tuple
                if (self.object_validator.validate(retval)):
                    yield retval

    def clone(self):
        return FunctionalGenerator(self.function_descriptor,
                                   [x.clone() for x in self.sub_generators],
                                   self.object_validator, self.name)


class AlternativesGenerator(GeneratorBase):
    """A generator that accepts multiple "sub-generators" and
    generates a sequence that is equivalent to the concatenation of
    the sequences generated by the sub-generators."""
    def __init__(self, sub_generators, object_validator = None, name = None):
        assert (len(sub_generators) > 1)
        super().__init__(object_validator, name)
        self.sub_generators = [x.clone() for x in sub_generators]

    def set_size(self, new_size):
        self.allowed_size = new_size

        for sub_generator in self.sub_generators:
            sub_generator.set_size(new_size)

    def generate(self):
        for sub_generator in self.sub_generators:
            yield from sub_generator.generate()

    def clone(self):
        return AlternativesGenerator([x.clone() for x in self.sub_generators],
                                     self.object_validator, self.name)


class _RecursiveGeneratorPlaceholder(GeneratorBase):
    """A type for placeholders for recursive generators.
    Really just a wrapper around a string."""

    def __init__(self, factory, identifier):
        self.identifier = identifier
        self.factory = factory

    def __eq__(self, other):
        return (self.identifier == other.identifier)

    def __ne__(self, other):
        return (not self.__eq__(other))

    def set_size(self, new_size):
        if (new_size > 0):
            self.actual_generator = self.factory._instantiate_placeholder(self)
            self.actual_generator.set_size(new_size)
        else:
            self.actual_generator = None

    def generate(self):
        if (self.actual_generator == None):
            return
        else:
            yield from self.actual_generator.generate()

    def clone(self):
        return _RecursiveGeneratorPlaceholder(self.factory, self.identifier)


class RecursiveGeneratorFactory(object):
    """A factory for creating recursive generators
    (possibly mutually recursive as well). We associate names with
    generator objects, and also allow these names to be used as placeholders.
    In the end, we actually create the generator object, when :set_size(): is called
    on the returned generator objects."""

    def __init__(self):
        self.generator_map = {}
        self.generator_factories = {}

    def make_placeholder(self, identifier):
        if (identifier in self.generator_map):
            raise basetypes.ArgumentError('Identifier already used as placeholder!')
        retval = _RecursiveGeneratorPlaceholder(self, identifier)
        self.generator_map[identifier] = retval
        return retval

    def make_generator(self, generator_name, generator_factory,
                       arg_tuple_to_factory):
        self.generator_factories[generator_name] = (generator_factory, arg_tuple_to_factory)
        return self.generator_map[generator_name]

    def _instantiate_placeholder(self, placeholder):
        assert (placeholder.factory is self)
        (factory, arg_tuple) = self.generator_factories[placeholder.identifier]
        return factory(*arg_tuple)


############################################################
# TEST CASES
############################################################
def test_generators():
    var_generator = LeafGenerator(['varA', 'varB', 'varC'], None, 'Variable Generator')
    const_generator = LeafGenerator([0, 1], None, 'Constant Generator')
    leaf_generator = AlternativesGenerator([var_generator, const_generator], None,
                                           'Leaf Term Generator')
    generator_factory = RecursiveGeneratorFactory()
    start_generator_ph = generator_factory.make_placeholder('Start')
    start_bool_generator_ph = generator_factory.make_placeholder('StartBool')

    start_generator = \
    generator_factory.make_generator('Start',
                                     AlternativesGenerator,
                                     ([leaf_generator] +
                                      [FunctionalGenerator('+',
                                                           [start_generator_ph,
                                                            start_generator_ph]),
                                       FunctionalGenerator('-',
                                                           [start_generator_ph,
                                                            start_generator_ph]),
                                       FunctionalGenerator('ite',
                                                           [start_bool_generator_ph,
                                                            start_generator_ph,
                                                            start_generator_ph])], None, None))

    start_bool_generator = \
    generator_factory.make_generator('StartBool',
                                     AlternativesGenerator,
                                     ([FunctionalGenerator('and',
                                                           [start_bool_generator_ph,
                                                            start_bool_generator_ph]),
                                       FunctionalGenerator('or',
                                                           [start_bool_generator_ph,
                                                            start_bool_generator_ph]),
                                       FunctionalGenerator('not',
                                                           [start_bool_generator_ph]),
                                       FunctionalGenerator('<=',
                                                           [start_generator_ph,
                                                            start_generator_ph]),
                                       FunctionalGenerator('=',
                                                           [start_generator_ph,
                                                            start_generator_ph]),
                                       FunctionalGenerator('>=',
                                                           [start_generator_ph,
                                                            start_generator_ph])], None, None))

    start_generator.set_size(6)
    for exp in start_generator.generate():
        print(exp)

if __name__ == '__main__':
    test_generators()

#
# enumerators.py ends here
