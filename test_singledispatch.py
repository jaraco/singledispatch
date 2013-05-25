#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import decimal
from itertools import permutations
import singledispatch as functools
import unittest


class TestSingleDispatch(unittest.TestCase):
    def test_simple_overloads(self):
        @functools.singledispatch
        def g(obj):
            return "base"
        def g_int(i):
            return "integer"
        g.register(int, g_int)
        self.assertEqual(g("str"), "base")
        self.assertEqual(g(1), "integer")
        self.assertEqual(g([1,2,3]), "base")

    def test_mro(self):
        @functools.singledispatch
        def g(obj):
            return "base"
        class C:
            pass
        class D(C):
            pass
        def g_C(c):
            return "C"
        g.register(C, g_C)
        self.assertEqual(g(C()), "C")
        self.assertEqual(g(D()), "C")

    def test_classic_classes(self):
        @functools.singledispatch
        def g(obj):
            return "base"
        class C:
            pass
        class D(C):
            pass
        def g_C(c):
            return "C"
        g.register(C, g_C)
        self.assertEqual(g(C()), "C")
        self.assertEqual(g(D()), "C")

    def test_register_decorator(self):
        @functools.singledispatch
        def g(obj):
            return "base"
        @g.register(int)
        def g_int(i):
            return "int %s" % (i,)
        self.assertEqual(g(""), "base")
        self.assertEqual(g(12), "int 12")
        self.assertIs(g.dispatch(int), g_int)
        self.assertIs(g.dispatch(object), g.dispatch(str))
        # Note: in the assert above this is not g.
        # @singledispatch returns the wrapper.

    def test_wrapping_attributes(self):
        @functools.singledispatch
        def g(obj):
            "Simple test"
            return "Test"
        self.assertEqual(g.__name__, "g")
        self.assertEqual(g.__doc__, "Simple test")

    @unittest.skipUnless(decimal, 'requires _decimal')
    def test_c_classes(self):
        @functools.singledispatch
        def g(obj):
            return "base"
        @g.register(decimal.DecimalException)
        def _(obj):
            return obj.args
        subn = decimal.Subnormal("Exponent < Emin")
        rnd = decimal.Rounded("Number got rounded")
        self.assertEqual(g(subn), ("Exponent < Emin",))
        self.assertEqual(g(rnd), ("Number got rounded",))
        @g.register(decimal.Subnormal)
        def _(obj):
            return "Too small to care."
        self.assertEqual(g(subn), "Too small to care.")
        self.assertEqual(g(rnd), ("Number got rounded",))

    def test_compose_mro(self):
        c = collections
        mro = functools._compose_mro
        bases = [c.Sequence, c.MutableMapping, c.Mapping, c.Set]
        for haystack in permutations(bases):
            m = mro(dict, haystack)
            self.assertEqual(m, [dict, c.MutableMapping, c.Mapping, object])
        bases = [c.Container, c.Mapping, c.MutableMapping, c.OrderedDict]
        for haystack in permutations(bases):
            m = mro(c.ChainMap, haystack)
            self.assertEqual(m, [c.ChainMap, c.MutableMapping, c.Mapping,
                                 c.Sized, c.Iterable, c.Container, object])
        # Note: The MRO order below depends on haystack ordering.
        m = mro(c.defaultdict, [c.Sized, c.Container, str])
        self.assertEqual(m, [c.defaultdict, dict, c.Container, c.Sized, object])
        m = mro(c.defaultdict, [c.Container, c.Sized, str])
        self.assertEqual(m, [c.defaultdict, dict, c.Sized, c.Container, object])

    def test_register_abc(self):
        c = collections
        d = {"a": "b"}
        l = [1, 2, 3]
        s = {object(), None}
        f = frozenset(s)
        t = (1, 2, 3)
        @functools.singledispatch
        def g(obj):
            return "base"
        self.assertEqual(g(d), "base")
        self.assertEqual(g(l), "base")
        self.assertEqual(g(s), "base")
        self.assertEqual(g(f), "base")
        self.assertEqual(g(t), "base")
        g.register(c.Sized, lambda obj: "sized")
        self.assertEqual(g(d), "sized")
        self.assertEqual(g(l), "sized")
        self.assertEqual(g(s), "sized")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sized")
        g.register(c.MutableMapping, lambda obj: "mutablemapping")
        self.assertEqual(g(d), "mutablemapping")
        self.assertEqual(g(l), "sized")
        self.assertEqual(g(s), "sized")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sized")
        g.register(c.ChainMap, lambda obj: "chainmap")
        self.assertEqual(g(d), "mutablemapping")  # irrelevant ABCs registered
        self.assertEqual(g(l), "sized")
        self.assertEqual(g(s), "sized")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sized")
        g.register(c.MutableSequence, lambda obj: "mutablesequence")
        self.assertEqual(g(d), "mutablemapping")
        self.assertEqual(g(l), "mutablesequence")
        self.assertEqual(g(s), "sized")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sized")
        g.register(c.MutableSet, lambda obj: "mutableset")
        self.assertEqual(g(d), "mutablemapping")
        self.assertEqual(g(l), "mutablesequence")
        self.assertEqual(g(s), "mutableset")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sized")
        g.register(c.Mapping, lambda obj: "mapping")
        self.assertEqual(g(d), "mutablemapping")  # not specific enough
        self.assertEqual(g(l), "mutablesequence")
        self.assertEqual(g(s), "mutableset")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sized")
        g.register(c.Sequence, lambda obj: "sequence")
        self.assertEqual(g(d), "mutablemapping")
        self.assertEqual(g(l), "mutablesequence")
        self.assertEqual(g(s), "mutableset")
        self.assertEqual(g(f), "sized")
        self.assertEqual(g(t), "sequence")
        g.register(c.Set, lambda obj: "set")
        self.assertEqual(g(d), "mutablemapping")
        self.assertEqual(g(l), "mutablesequence")
        self.assertEqual(g(s), "mutableset")
        self.assertEqual(g(f), "set")
        self.assertEqual(g(t), "sequence")
        g.register(dict, lambda obj: "dict")
        self.assertEqual(g(d), "dict")
        self.assertEqual(g(l), "mutablesequence")
        self.assertEqual(g(s), "mutableset")
        self.assertEqual(g(f), "set")
        self.assertEqual(g(t), "sequence")
        g.register(list, lambda obj: "list")
        self.assertEqual(g(d), "dict")
        self.assertEqual(g(l), "list")
        self.assertEqual(g(s), "mutableset")
        self.assertEqual(g(f), "set")
        self.assertEqual(g(t), "sequence")
        g.register(set, lambda obj: "concrete-set")
        self.assertEqual(g(d), "dict")
        self.assertEqual(g(l), "list")
        self.assertEqual(g(s), "concrete-set")
        self.assertEqual(g(f), "set")
        self.assertEqual(g(t), "sequence")
        g.register(frozenset, lambda obj: "frozen-set")
        self.assertEqual(g(d), "dict")
        self.assertEqual(g(l), "list")
        self.assertEqual(g(s), "concrete-set")
        self.assertEqual(g(f), "frozen-set")
        self.assertEqual(g(t), "sequence")
        g.register(tuple, lambda obj: "tuple")
        self.assertEqual(g(d), "dict")
        self.assertEqual(g(l), "list")
        self.assertEqual(g(s), "concrete-set")
        self.assertEqual(g(f), "frozen-set")
        self.assertEqual(g(t), "tuple")

    def test_mro_conflicts(self):
        c = collections

        @functools.singledispatch
        def g(arg):
            return "base"

        class O(c.Sized):
            def __len__(self):
                return 0

        o = O()
        self.assertEqual(g(o), "base")
        g.register(c.Iterable, lambda arg: "iterable")
        g.register(c.Container, lambda arg: "container")
        g.register(c.Sized, lambda arg: "sized")
        g.register(c.Set, lambda arg: "set")
        self.assertEqual(g(o), "sized")
        c.Iterable.register(O)
        self.assertEqual(g(o), "sized")   # because it's explicitly in __mro__
        c.Container.register(O)
        self.assertEqual(g(o), "sized")   # see above: Sized is in __mro__

        class P:
            pass

        p = P()
        self.assertEqual(g(p), "base")
        c.Iterable.register(P)
        self.assertEqual(g(p), "iterable")
        c.Container.register(P)
        with self.assertRaises(RuntimeError) as re:
            g(p)
            self.assertEqual(
                str(re),
                ("Ambiguous dispatch: <class 'collections.abc.Container'> "
                    "or <class 'collections.abc.Iterable'>"),
            )

        class Q(c.Sized):
            def __len__(self):
                return 0

        q = Q()
        self.assertEqual(g(q), "sized")
        c.Iterable.register(Q)
        self.assertEqual(g(q), "sized")   # because it's explicitly in __mro__
        c.Set.register(Q)
        self.assertEqual(g(q), "set")     # because c.Set is a subclass of
                                          # c.Sized which is explicitly in
                                          # __mro__

    def test_cache_invalidation(self):
        from collections import UserDict
        class TracingDict(UserDict):
            def __init__(self, *args, **kwargs):
                super(TracingDict, self).__init__(*args, **kwargs)
                self.set_ops = []
                self.get_ops = []
            def __getitem__(self, key):
                result = self.data[key]
                self.get_ops.append(key)
                return result
            def __setitem__(self, key, value):
                self.set_ops.append(key)
                self.data[key] = value
            def clear(self):
                self.data.clear()
        _orig_wkd = functools.WeakKeyDictionary
        td = TracingDict()
        functools.WeakKeyDictionary = lambda: td
        c = collections
        @functools.singledispatch
        def g(arg):
            return "base"
        d = {}
        l = []
        self.assertEqual(len(td), 0)
        self.assertEqual(g(d), "base")
        self.assertEqual(len(td), 1)
        self.assertEqual(td.get_ops, [])
        self.assertEqual(td.set_ops, [dict])
        self.assertEqual(td.data[dict], g.registry[object])
        self.assertEqual(g(l), "base")
        self.assertEqual(len(td), 2)
        self.assertEqual(td.get_ops, [])
        self.assertEqual(td.set_ops, [dict, list])
        self.assertEqual(td.data[dict], g.registry[object])
        self.assertEqual(td.data[list], g.registry[object])
        self.assertEqual(td.data[dict], td.data[list])
        self.assertEqual(g(l), "base")
        self.assertEqual(g(d), "base")
        self.assertEqual(td.get_ops, [list, dict])
        self.assertEqual(td.set_ops, [dict, list])
        g.register(list, lambda arg: "list")
        self.assertEqual(td.get_ops, [list, dict])
        self.assertEqual(len(td), 0)
        self.assertEqual(g(d), "base")
        self.assertEqual(len(td), 1)
        self.assertEqual(td.get_ops, [list, dict])
        self.assertEqual(td.set_ops, [dict, list, dict])
        self.assertEqual(td.data[dict], g.dispatch(dict))
        self.assertEqual(g(l), "list")
        self.assertEqual(len(td), 2)
        self.assertEqual(td.get_ops, [list, dict])
        self.assertEqual(td.set_ops, [dict, list, dict, list])
        self.assertEqual(td.data[list], g.dispatch(list))
        class X:
            pass
        c.MutableMapping.register(X)   # Will not invalidate the cache,
                                       # not using ABCs yet.
        self.assertEqual(g(d), "base")
        self.assertEqual(g(l), "list")
        self.assertEqual(td.get_ops, [list, dict, dict, list])
        self.assertEqual(td.set_ops, [dict, list, dict, list])
        g.register(c.Sized, lambda arg: "sized")
        self.assertEqual(len(td), 0)
        self.assertEqual(g(d), "sized")
        self.assertEqual(len(td), 1)
        self.assertEqual(td.get_ops, [list, dict, dict, list])
        self.assertEqual(td.set_ops, [dict, list, dict, list, dict])
        self.assertEqual(g(l), "list")
        self.assertEqual(len(td), 2)
        self.assertEqual(td.get_ops, [list, dict, dict, list])
        self.assertEqual(td.set_ops, [dict, list, dict, list, dict, list])
        self.assertEqual(g(l), "list")
        self.assertEqual(g(d), "sized")
        self.assertEqual(td.get_ops, [list, dict, dict, list, list, dict])
        self.assertEqual(td.set_ops, [dict, list, dict, list, dict, list])
        c.MutableSet.register(X)       # Will invalidate the cache.
        self.assertEqual(len(td), 2)   # Stale cache.
        self.assertEqual(g(l), "list")
        self.assertEqual(len(td), 1)
        g.register(c.MutableMapping, lambda arg: "mutablemapping")
        self.assertEqual(len(td), 0)
        self.assertEqual(g(d), "mutablemapping")
        self.assertEqual(len(td), 1)
        self.assertEqual(g(l), "list")
        self.assertEqual(len(td), 2)
        g.register(dict, lambda arg: "dict")
        self.assertEqual(g(d), "dict")
        self.assertEqual(g(l), "list")
        functools.WeakKeyDictionary = _orig_wkd


if __name__ == '__main__':
    unittest.main()
