#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''Contains utilities for performing complex searches in nested Python 
    iterables based on both keys/indices and values.
    This has been tested (using gorp.test.test_jsonpath) on Python 3.6-3.9.
    It might work on 3.5, but no warranty is made except for 3.6-3.9.
The most immediately comparable project in terms of scope is jsonpath_ng, 
    which is fully JsonPath standard-compliant, but which appears to me to 
    lack some of this module's power, such as regex matching on keys.
Some things that you can do with this module:
    - Use regular expressions to match keys as well as values in dicts.
    - Filter layers of JSON based on comparisons of multiple values (e.g., 
        get indices 1:10 of an array only if arr[1] > str(arr[2]))
    - Mutate JSON at the nodes found by a search.
    - Filter pandas DataFrames using the same query language, while still 
        getting their incredibly fast performance.
    - If you prefer not to use a query parser, build layers of filters by an 
        object-oriented approach. See the Filter, GlobalConstraint, Mutator, 
        and JsonPath classes. Thanks to jsonpath_ng for pioneering this 
        approach!
    - Build arithmetic expressions of the values and keys in an iterable 
        without using eval(). See math_eval, and its workhorse function, 
        compute(eqn).
The searching of nested iterables (which we'll call JSON for short) in this 
    module works using a "filter path" that contains ordered "filter layers" 
    that may look  something like this::
    [
    '..', # flag that turns on recursive search (descend til you find a match).
        [ # layer 1
        Filter(keys_in = ['key', number], # key must match one of these
               vals_in = ['a regex'], # corresponding value must match this
               fuzzy_keys = True), # keys_in can have regexes or functions
        GlobalConstraint(keys_in = ['blah'], # this key must be in the iterable
                         vals_in = [lambda x: x['a']>x['b']], 
                         # constraint on the iterable as a whole
                         action = 'down')
        ], 
        # if the iterable matched both filters, descend to iterable['blah']
    '!!', # another type of flag (the below constraints should NOT be matched).
        [ # layer 2
        Filter(keys_in = ['baz'], # key that must be in the iterable 
               vals_in = [lambda x: (x<3) and (x>0)], 
               # constraint on the value associated with that key
               action = 'up2', 
               # if the iterable satisfied this filter, we'll go up to the
               # grandparent of this iterable
               fuzzy_keys = False) 
               # keys must match a string/number in keys_in exactly
        ],
    <optional Mutator object for updating JSON>
    ]

In this example, we see that our filter path can contain:
    
    1. flags ('..' and '!!') that change how filters are used
    
    2. sublists of filters that all operate on the same level of the JSON (so 
        layer 1 operates on the root level of the JSON,
        layer 2 operates on the second level of key-value pairs, and so on)
        - Even if you only have one filter in a layer, it has to be contained 
            in a list.
    
    3. An optional Mutator object that comes after all the sublists of filters.

Note that the user of this module doesn't need to explicitly build a list of 
filter layers like the one shown above; the parse_json_path and related 
functions take care of translating query strings into layers of filters, 
so a query string like::
    ..~~@zzfo{2};;nn1:vv^[a-z]+$~~ggblahvvnnx[`a`]>x[`b`]~~@!!zzbazvvnnx<3&x>0~~^^

would translate directly into one possible list of filter layers that 
would match the example above.

I have not attempted to comply with the JsonPath "standard" established by 
Stefan Goessner (https://goessner.net/articles/JsonPath/), which in turn 
was inspired by the syntax of the much-better-known XPath for XML.

I apologize for the lack of compliance with this standard, and I apologize 
still more for the rather long query strings caused by my profuse use of 
special double-characters,
but I would also like to explain the philosophy that motivates this choice:
    
    * Regular expressions have many special characters, including '.' and '*'.
    In any application like this where regular expressions are used, 
    it is inconvenient for '.' and '*' have any other special meanings.
    
    * A special double-character is easily compatible with regular 
    expressions because any double-character can be expressed as 
    "character{2}" in regex.
    
    * A more talented programmer than I could undoubtedly create a parser 
    that can handle the overloading of special characters, but I can't.
'''
import re
import math_eval
from math_eval import compute, IntRange, ComputeError, has_pattern, ufunctions, binops, safe_ufunctions, safe_binops
from .gprint import bad_json, gprint, compressed_obj_repr
from .utils import is_iterable
__version__ = '0.1.0'
function = type(is_iterable)

class JsonPathError(Exception): pass


def _convert_to_filterfunc(x, fuzzy):
    '''Used by the Filter class to convert user-supplied arguments into functions that
    compare keys and values to those arguments. fuzzy is the fuzzy_keys 
    parameter of Filters.'''
    if not fuzzy and (not isinstance(x, (IntRange, int, str))):
        raise JsonPathError("When not in fuzzy_keys mode, only IntRange slicers and ints are allowed as key tests.")
    if isinstance(x, (list, tuple)):
        # a list or tuple within the keys_in/vals_in tuple; bundles conditions together.
        funclist = [_convert_to_filterfunc(elt, fuzzy) for elt in x]
        return lambda val: all(func(val) for func in funclist)
    elif isinstance(x, function):
        return x
    elif isinstance(x, (int, float, IntRange, complex)):
        return lambda val: val == x
    elif isinstance(x, str):
        if fuzzy: # x is a regex; the appropriate function tests if val contains that
                  # regex
            return lambda val: has_pattern(val, x)
        else: # x is a non-regex; the appropriate function tests equality with x
            return lambda val: val == x
    raise TypeError("Expected inputs to _convert_to_filterfunc to be list, tuple, function, number, IntRange, or string, got {}".format(type(x)))

def _filter_layer_repr(filter_layer):
    '''Functions returned by math_eval.compute() have docstrings that 
    indicate what the function does. 
This recursively searches the keys_in and vals_in attributes of Filter and 
    GlobalConstraint objects and make it so that the string representation
    of those compute() functions looks like "compute('x**2 + 3')" instead of
    '<function compute.<locals>.outfunc at 0x000002EEE5AAC160>'.'''
    out = []
    for k in filter_layer:
        if isinstance(k, list):
            out.append(_filter_layer_repr(k))
            continue
        try:
            if 'compute.<locals>.outfunc' in repr(k):
                doc = k.__doc__.split('\n')[0]
                out.append('compute("{}")'.format(doc))
            else:
                out.append(k)
        except:
            out.append(k)
    return out


class Filter:
    '''Used to check keys, array indices, and values in nested Python objects.
    Note that in this context "keys" means both dict keys and array indices.

**Arguments**:

*keys_in*: Function that performs a comparison, IntRange, number, string, or 
tuple that contains any number of nums, strings, comparison funcs, 
:class:`math_eval.IntRange`, or tuples.
If this is a tuple, a key that matches *anything* in the tuple is a match.
Any tuple within the tuple represents a set of conditions that are 
bundled and must be simultaneously satisfied.
If this is empty, all keys are matched.

*vals_in*: Same as keys_in, but tests values in a key-value pair.

*key_or_val*: Bool, default False. If true, any key-value pair where the key 
    matches keys_in OR vals_in is considered a match.

*action*: str: {'check', 'down', 'stay', 'up'+str(integer)} 
This determines how json_extract treats key-value pairs that are matched 
by this filter.
    * If the action is 'check', there must be another filter in the filter 
    layer. This filter only makes assertions.
    * If the action is 'down', json_extract will search downwards (to the
    children) of any keys that are matched by this filter.
    * If the action is 'stay', json_extract will return the container holding 
    the keys that match this filter.
    * If the action is 'up'+str(integer), json_extract will search the 
    integer^th ancestor (e.g., 1 = parent, 3 = great-grandparent) of the 
    key matched by this filter.

*fuzzy_keys*: bool. If False, IntRanges match array indices but not dict keys
and numbers and strings in keys_in must match keys and indices exactly.
If this is True, keys can be tested "fuzzily" by comparison functions and 
IntRanges, and all strings are treated as regular expressions.
Value testing is "fuzzy" regardless of the value of fuzzy_keys.

**Other attributes**:
    
*keyfuncs*: List of functions that perform key matching based on keys_in.
*valfuncs*: List of functions that perform value matching based on vals_in.

**Methods**:
    
*in*: The test "(k, v) in filt" will return True if the key-value 
pair k,v matches the filter "filt".

*callable*: "filt(k, v)" returns the same thing as "(k, v) in filt".
    '''
    def __init__(self, 
                 keys_in = tuple(), 
                 vals_in = tuple(), 
                 key_or_val = False,
                 action = 'down',
                 fuzzy_keys = False):
        if not is_iterable(keys_in) and not isinstance(keys_in, IntRange):
            self.keys_in = [keys_in]
        else:
            self.keys_in = keys_in
        
        if not is_iterable(vals_in) and not isinstance(vals_in, IntRange):
            self.vals_in = [vals_in]
        else:
            self.vals_in = vals_in
        
        self.keyfuncs = [_convert_to_filterfunc(k, fuzzy = fuzzy_keys) for k in self.keys_in]
        self.valfuncs = [_convert_to_filterfunc(v, True) for v in self.vals_in]
        self.key_or_val = key_or_val
        self.action = action
        self.fuzzy_keys = fuzzy_keys
    
    def filter(self, arr, reverse_selectivity = False):
        '''arr: a dict or array.
reverse_selectivity: If True, return only those key-value pairs that do NOT 
    satisfy the value filters of this Filter, and also NOT the key filters, 
    unless this Filter has fuzzy_keys = False, in which case the keys must 
    still be matched.
Returns a dict mapping the paths to all key-value pairs that satisfy this 
    Filter's keyfuncs and valfuncs (or keyfuncs OR valfuncs if self.key_or_val)
        '''
        out = {}
        if self.fuzzy_keys:
            if isinstance(arr, dict):
                iterator = arr.items()
            else:
                iterator = enumerate(arr)
            for k, v in iterator:
                if ((k, v) in self) ^ reverse_selectivity:
                    out[k] = v
        else: # non-fuzzy matching
            # reverse_selectivity cannot be implemented for non-fuzzy matching, because
            # reverse_selectivity would require linear-time exhaustive search of arr,
            # and that's not what fuzzy_keys is about.
            if isinstance(arr, dict):
                keys = arr
            else:
                keys = range(len(arr))
            if self.keys_in:
                keysin = self.keys_in
            else:
                if not self.valfuncs: 
                    # no keyfuncs or valfuncs; filtering will return the original itbl
                    if isinstance(arr, dict):
                        return arr
                    else:
                        # Other functions in this module need to work with dicts
                        # rather than arrays, so map e.g. [1, 2, 3] to {0:1, 1:2, 2:3}
                        return dict(enumerate(arr))
                keysin = keys
            for k in keysin:
                if isinstance(k, IntRange):
                    if isinstance(arr, dict):
                        continue
                        # IntRanges cannot be used to search for keys in dicts in 
                        # non-fuzzy mode, 
                        # because the IntRange could contain a huge number of 
                        # elements and that would make an exhaustive search prohibitive
                    else:
                        for ii in k.indices_from(arr):
                            if self.key_or_val:
                                out[ii] = arr[ii]
                            valmatch = len(self.vals_in) == 0
                            for valopt in self.valfuncs:
                                try:
                                    valmatch |= valopt(arr[ii])
                                except:
                                    pass
                            if valmatch ^ reverse_selectivity:
                                # TODO: maybe more intuitive for reverse_selectivity to
                                # be COMPLETELY disabled when fuzzy_keys is off than
                                # for it to reverse selectivity on values but not keys.
                                # I may decide to comment out the "^reverse_selectivity"
                                out[ii] = arr[ii]
                else:
                    if k in keys:
                        if self.key_or_val:
                            out[k] = arr[k]
                        valmatch = len(self.vals_in) == 0
                        for valopt in self.valfuncs:
                            try:
                                valmatch |= valopt(arr[k])
                            except:
                                pass
                        if valmatch ^ reverse_selectivity:
                            out[k] = arr[k]
        return out
    
    def filter_dataframe(self, df, reverse_selectivity = False):
        '''df: a pandas.DataFrame.
reverse_selectivity: Return all columns and rows that DON'T satisfy 
    constraints instead.
**Returns:** (
    boolean pandas.Series (True for each row satisfying vals_in constraints),
    list(names of columns satisfying keys_in constraints)
)'''
        import pandas as pd
        if self.valfuncs:
            rows = pd.Series([False]*df.shape[0])
        else:
            rows = pd.Series([True]*df.shape[0])
        if self.keyfuncs:
            cols = pd.Series([False]*df.shape[1])
            for keyfunc in self.keyfuncs:
                # each keyfunc applies an elementwise regex match to column names, or an
                # exact string match if not self.fuzzy_keys, returning a boolean array
                # of same length as columns
                new_cols = keyfunc(df.columns) ^ reverse_selectivity
                cols |= new_cols
                for col in df.columns[new_cols]:
                    for valfunc in self.valfuncs:
                        try:
                            new_rows = (valfunc(df[col]) ^ reverse_selectivity)
                            rows |= new_rows
                        except Exception as ex: 
                            # probably the valfunc was trying an invalid operation
                            # for that column's dtype 
                            pass
        else:
            cols = pd.Series([True]*df.shape[1])
            for col in df.columns:
                for valfunc in self.valfuncs:
                    try:
                        rows |= (valfunc(df[col]) ^ reverse_selectivity)
                    except:
                        pass
        return rows, list(df.columns[cols])
                
    
    def __contains__(self, key_val):
        k, v = key_val
        keymatch = len(self.keys_in) == 0
        valmatch = len(self.vals_in) == 0
        if not keymatch:
            for keyopt in self.keyfuncs:
                try:
                    keymatch |= keyopt(k)
                except:
                    pass
        if keymatch and self.key_or_val:
            return True
        if not valmatch:
            for valopt in self.valfuncs:
                try:
                    valmatch |= valopt(v)
                except:
                    pass
        if (self.key_or_val and valmatch) or (valmatch and keymatch):
            return True
        return False
    
    def __call__(self, key, val):
        return (key, val) in self
            
    def __repr__(self):
        keysin = _filter_layer_repr(self.keys_in)
        valsin = _filter_layer_repr(self.vals_in)
        return "Filter(keys_in = {}, vals_in = {}, key_or_val = {}, action = '{}', fuzzy_keys = {})".format(keysin, valsin, bool(self.key_or_val), self.action, bool(self.fuzzy_keys))
    __str__ = __repr__



class GlobalConstraint:
    '''Whereas the :class:`Filter` class checks individual key-value pairs in an array or
dict, the GlobalConstraint is for applying constraints to the whole iterable.

keys_in: a list/tuple of strings, numbers, or IntRanges.
    As with a Filter object with fuzzy_keys = False, each string/num in 
    keys_in must exactly match at least one key or index in the iterable; no 
    regular expressions!

vals_in: a list of functions that each take a single iterable as an argument. 
    These can be generated by the compute() function (which supports array 
    and dict slicing and indexing) or they can just be normal Python functions.
    Unlike the keyfuncs and valfuncs of a Filter object, constraints can 
    operate on multiple key-value pairs in a single iterable, like 
    "itbl['b']>=itbl['a']" or "sum(itbl)>0".

action: See the description of the "action" argument for Filter objects.
    '''
    def __init__(self, 
                 keys_in = tuple(),
                 vals_in = tuple(),
                 action = 'down'):
        if not is_iterable(keys_in):
            self.keys_in = [keys_in]
        else:
            self.keys_in = keys_in
        if not is_iterable(vals_in):
            self.vals_in = [vals_in]
        else:
            self.vals_in = vals_in
        for ii, val in enumerate(self.vals_in):
            if isinstance(val, str):
                # most likely due to val coming from a query string without an "nn"
                # after the "vv" delimiter.
                self.vals_in[ii] = compute(val)
        if any(hasattr(k, '__call__') for k in self.keys_in):
            raise JsonPathError("GlobalConstraint keys_in arguments cannot be functions. They should be things like numbers and other normal dict keys/array indices.")
        self.action = action
        
    def filter(self, itbl, reverse_selectivity = False):
        out = {}
        if self.satisfied_by(itbl) ^ reverse_selectivity:
            if not self.keys_in:
                if isinstance(itbl, dict):
                    out.update(itbl)
                else:
                    out.update(enumerate(itbl))
            for k in self.keys_in:
                if not isinstance(k, IntRange):
                    try:
                        out[k] = itbl[k]
                    except:
                        pass
                elif not isinstance(itbl, dict):
                    out[k] = itbl[k.slice]
        return out
    
    def filter_dataframe(self, df, reverse_selectivity = False):
        '''df: a pandas.DataFrame.
reverse_selectivity: Return all columns and rows that DON'T satisfy 
    constraints instead.
**Returns:** (
    boolean pandas.Series (True for each row satisfying vals_in constraints),
    list(names of columns in self.keys_in)
)'''
        import pandas as pd
        if self.keys_in:
            if reverse_selectivity:
                cols = [x for x in df.columns if x not in set(self.keys_in)]
            else:
                cols = self.keys_in.copy()
        else:
            cols = df.columns
        rows = pd.Series([False]*len(df))
        if self.vals_in:
            for valfunc in self.vals_in:
                rows |= (valfunc(df) ^ reverse_selectivity)
        return rows, cols
    
    def satisfied_by(self, itbl):
        '''itbl: any iterable (array, dict, pandas DataFrame) that this
    GlobalConstraint can filter.
**Returns:** bool, True if itbl satisfies all constraints, else False.'''
        out = True
        for constraint in self.vals_in:
            try:
                out &= constraint(itbl)
            except:
                return False
        return out
    
    def __str__(self):
        return "GlobalConstraint(keys_in = {k}, vals_in = {valsin}, action = '{a}')".format(k=self.keys_in, valsin = _filter_layer_repr(self.vals_in), a=self.action)
    __repr__ = __str__



class Mutator:
    '''Intended as the last "layer" in a filter path. These are used by JsonPath
    objects' sub method and also by json_extract to mutate json at the paths 
    found by the other filters in the path.
If "fun" is the replacement_func of Mutator "mut", mut.mutate(json, paths) 
    will replace the values {v1, ..., vn} that are json's children of every 
    path in paths with {fun(v1), ..., fun(vn)}.'''
    def __init__(self, replacement_func):
        '''replacement_func: a function of one variable,
OR a string that math_eval.compute() can parse as a function of one variable.'''
        if isinstance(replacement_func, str):
            self.replacement_funcname = "compute({})".format(replacement_func)
            self.replacement_func = compute(replacement_func)
        else:
            self.replacement_funcname = replacement_func.__name__
            self.replacement_func = replacement_func
        
    def __repr__(self):
        return "Mutator(replacement_func = '{}')".format(self.replacement_funcname)
    __str__ = __repr__
        
    def mutate(self, json, paths, ask_permission = False):
        mutate_json_repeatedly(json, paths, self.replacement_func, ask_permission)



def follow_abspath(json, abspath):
    '''json: an arbitrarily nested python object, where each layer 
    is a list, dict, or tuple.
abspath: a list of keys or array indices to be followed.
**Returns:** the child of json[abspath[0]][abspath[1]]...[abspath[-1]]'''
    out = json
    for elt in abspath:
        out = out[elt]
    return out


def json_find_matches(json,
                      graph,
                      filter_path, 
                      curpath = tuple(), 
                      get_full_path_also=False,
                      reverse_selectivity = False, 
                      recursive = False):
    '''See :func:`json_extract` for a description of how this works.
Recursively searches the nested iterable graph,
    using a pre-generated filter_path (which must be a list of filters and 
    not a query string).
Called by json_extract and other similar functions.
Returns a generator expression that yields the appropriate results.'''
    paths_to_action_filter = []
    new_filter_path = filter_path.copy()
    while isinstance(new_filter_path[0], str):
        if new_filter_path[0] == '..':
            recursive = True
            new_filter_path = new_filter_path[1:]
        if new_filter_path[0] == '!!':
            reverse_selectivity = not reverse_selectivity
            new_filter_path = new_filter_path[1:]
    
    current_filter = new_filter_path[0]
    if len(new_filter_path) == 1 \
        and len(current_filter) == 1 \
        and (current_filter[0].keys_in == [''] or (not current_filter[0].keys_in)) \
        and not current_filter[0].vals_in:
        # this is a filter with no specification for keys or values, which could
        # have been produced by terminating a parsed path with a path-separating 
        #pipe; just return the entire graph.
        if get_full_path_also:
            yield curpath, graph
        else:
            yield graph
        return
    satisfied = [False for elt in current_filter]
    paths_to_action_filter = []
    action = [filt.action for filt in current_filter if filt.action!='check'][0]
    if action[:2] == 'up':
        # "up" actions are of the form "up1", "up2", etc.
        if len(action) > 2:
            num_levels_up = int(action[2:])
        else:
            num_levels_up = 1 # if action is "up", assumed number is 1
        paths_to_action_filter = [curpath[:-num_levels_up]]
    elif action == 'stay':
        paths_to_action_filter = [curpath]
    
    for ii, filt in enumerate(current_filter):
        results = filt.filter(graph, reverse_selectivity)
        if results:
            satisfied[ii] = True
        if filt.action == 'down': # 'up' and 'stay' possibilites already covered
            paths_to_action_filter = set()
            for k in results:
                if isinstance(k, IntRange):
                    for k_ind in k.indices_from(graph):
                        paths_to_action_filter.add(curpath + (k_ind,))
                else:
                    paths_to_action_filter.add(curpath + (k,))
    
    if recursive:
        if type(graph)==dict:
            iterator = graph.items()
        else:
            iterator = enumerate(graph)
        for curnode, newgraph in iterator:
            if is_iterable(newgraph) and (curpath+(curnode,) not in paths_to_action_filter): 
                # we haven't matched all the filters yet, but we can descend
                # If we didn't match this node in the path, we don't
                # want to continue recursively searching this node's children
                # UNLESS we're in recursive mode.
                # i.e., if we have path = 
                # [[Filter(keys_in = '^a$')],[Filter(keys_in = (1,2)]], we want
                # paths like ['a',1,'b',3] or ['a',2], but not paths like
                # ['a', 3, 'b', 1].
                # If we're in recursive mode, paths like ['a',3,'b',1] are fine.
                yield from json_find_matches(json,
                        newgraph, 
                        new_filter_path, 
                        curpath + (curnode,),
                        get_full_path_also,
                        reverse_selectivity = reverse_selectivity,
                        recursive = recursive)
    if all(satisfied):
        # we matched all the filters on this layer, move forward in the path.
        for path_to_action_filter in sorted(paths_to_action_filter):
            nextgraph = follow_abspath(json, path_to_action_filter)
            if len(new_filter_path)==1:
                # print("Adding nextgraph: ", end = '')
                # gprint(nextgraph)
                if get_full_path_also:
                    yield (path_to_action_filter, nextgraph)
                else:
                    yield nextgraph
                continue
            elif is_iterable(nextgraph):
                # if we're in recursive mode, we already searched.
                # continue searching, this time for any paths that match
                # the rest of the path (not including the current node in the path,
                # which we already found).
                # print("(De/Asc)ending from path {} to path_to_action_filter {}".format(curpath, path_to_action_filter))
                yield from json_find_matches(json,
                        nextgraph, 
                        new_filter_path[1:], 
                        path_to_action_filter,
                        get_full_path_also,
                        reverse_selectivity = reverse_selectivity,
                        recursive = False) # Finding a match disables recursive mode
    return


def json_find_matches_dataframe(df, filter_path, reverse_selectivity = False):
    '''Iteratively filters a pandas.DataFrame df using the same sort of 
    filter_path used by json_extract.
Because of the tabular nature of pandas DataFrames, filters are treated as 
    being either 'down' or 'check'; a filter either refines both the rows and 
    columns returned (essentially a 'down' action) or refines only the rows 
    returned (essentially a 'check' action).'''
    import pandas as pd
    for layer in filter_path:
        if isinstance(layer, str):
            if layer == '!!':
                reverse_selectivity = not reverse_selectivity
            continue
        rows = pd.Series([True]*df.shape[0])
        for filt in layer:
            new_rows, new_cols = filt.filter_dataframe(df)
            rows &= new_rows
            if filt.action != 'check':
                cols = new_cols
            else:
                cols = df.columns
        df = df.loc[rows, cols]
    return df


def json_extract(filter_path, 
                 json,
                 get_full_path_also = False,
                 reverse_selectivity = False,
                 recursive = False,
                 fuzzy_keys = False,
                 sub_func = None,
                 ask_permission = True):
    '''*json*: an arbitrarily nested Python object, where each layer 
    is a tuple, list, dict, or subclass of dict.

*filter_path*: list of :class:`Filter` steps, or single string or number.
    The preferred form of filter_path is a query string that can be
    parsed into a list of Filter layers by parse_json_path.

*get_full_path_also*: bool, see "Returns".

*reverse_selectivity*: bool, see "Returns".

*recursive*: bool, see "Returns".

*fuzzy_keys*: If True, you can test keys with regular expressions and many 
kinds of mathematical tests.
The drawback of using fuzzy_keys is that arrays and dicts have to be searched
exhaustively in linear time, rather than just going straight to an exact 
index or key in constant time.
fuzzy_keys can be toggled by 'zz' in a filter_path query string.

*sub_func*: Function of one variable. 
If this is not None, after the JSON is extracted, the sub_func is applied to 
the terminal nodes by mutate_json.
You can also turn on "sub mode" in a query string by terminating the query 
string with "~~ss", followed by a string representing the sub_func
that can be parsed by math_eval.compute(). 

*ask_permission*: only relevant if sub_func is not None. When in "sub mode", if
ask_permission is True, create an interactive prompt.

**Returns:** a list of the children that can be found by paths matched by this 
function.

Notes on optional parameters:
    * If reverse_selectivity is True at a given filter layer, the matching
    changes as follows:
        * If fuzzy_keys is False, only the matching on values is reversed. 
        * If fuzzy_keys is True, the matching on both values and keys is 
        reversed.
    * If get_full_path_also is True, return instead a dict mapping 
    complete paths (tuples of keys and indices) to the children of those paths.
    * If recursive is True, we keep descending until we find a match, even if
    the match fails on the first level it's applied to.

**EXAMPLES**
___________

>>> bad_json = {'b': 3,
   '6': 7,
   'jub': {'uy': [1, 2, 3],
           'yu': [6, {'y': 'b', 'M8': 9, 1: (3,0)}]}}
>>> json_extract(json = bad_json,
    filter_path = '^\d+$') 
    # this is a regex match on keys; it doesn't work by default 
ALERT: It looks like you may have tried to match keys with regular expressions
['\\\\d'] while not in fuzzy_keys mode. Did you intend this?
[]
>>> json_extract(json = bad_json,
    filter_path = '^\d+$', fuzzy_keys=True) 
    # regexes on keys work with fuzzy_keys=True.
[7]
>>> json_extract(json = bad_json,
    filter_path = 'jub~~@yu~~uy') 
    # look for the children of key 'uy' that's a child of 
    # root-level 'jub', but only if 'jub' also has the child 'yu'.
    # This is non-fuzzy matching, but it works since 'jub', 'yu'
    # and 'uy' all match keys in json exactly.
[[1, 2, 3]]
>>> json_extract(json = bad_json,
    filter_path = '..~~@zz^[a-z]{2}$~~@zznn0') 
    # 'zz' toggles fuzzy_keys; the first use turned it on 
    # and the second turned it off
[1, 6]
>>> json_extract(json = bad_json,
    fuzzy_keys = True,
    filter_path = '[a-z]{2}~~@nn0') 
    # Matches 'jub', but then tries to find index 0 in graph['jub'] and can't
[]
>>> json_extract(json = bad_json,
    filter_path = '..~~@zz[5-8];;nn5:9', 
    get_full_path_also = True) 
    # recursively ('..') looks for keys with a substring in {'5','6','7','8'}
    # OR (';;') that have the numeric value in range(5,9) ('nn5:9')
{('jub', 'yu', 1, 'M8'): 9, ('6',): 7}
>>> json_extract(json = bad_json,
    filter_path = '[5-8];;nn5:9')
    # careful! you're trying to match an IntRange and a regex to keys when not 
    # fuzzy_keys. When fuzzy_keys = False, IntRanges only match array indices.
[]
>>> json_extract(json = bad_json,
    filter_path = '..~~@nnint(k)*2<4vvnnstr(v)>`8`', 
    get_full_path_also = True) 
    # If fuzzy_keys is False, we can't use functions like "int(k)*2 < 4"
    # to constrain keys. As a result, we get this error:
Traceback (most recent call last):
...
JsonPathError: When not in fuzzy_keys mode, only IntRange slicers and ints are allowed as key tests.
>>> small_json = [[1, 2, 3, 4, 5], {0: 'a', 1: 'b'},
        {2: 'c'}, [6, 7], {3: 'd'}]
>>> json_extract(json = small_json,
        filter_path = 'nn:3~~@..~~@ggnn1vvx[0]<x[1]', 
        get_full_path_also = True)
        # The 'gg' string before the third layer means that we create a 
        # GlobalConstraint that matches the key/index 1,
        # if itbl[0] < itbl[1].
{(0, 1): 2, (1, 1): 'b'}
>>> json_extract(json = small_json,  
        filter_path = 'nn:3~~@..~~@ggnn1:3vvnnx[0]<x[1]',
        get_full_path_also = True)
        # GlobalConstraints only match IntRanges to array indices.
        # IntRanges do not match numeric dict keys in a GlobalConstraint.
{(0, 1): 2, (0, 2): 3}
>>> json_extract(json = bad_json,
    filter_path = '..~~@zz(?i)^[M-Y]||vvnn1:10:2',
    get_full_path_also = True) 
    # The '||' means that at least one key-value pair must match the key
    # constraint OR the value constraint. It doesn't have to match both.
{('jub', 'uy'): [1, 2, 3],
 ('jub', 'yu'): [6, {'y': 'b', 'M8': 9, 1: (3, 0)}],
 ('6',): 7,
 ('b',): 3}
>>> json_extract(json = bad_json,
    filter_path = 'zz!!\d~~@!!yu',
    get_full_path_also = True) 
    # in this case, '!!' toggles reverse_selectivity on and then off again.
{('jub', 'yu'): [6, {'y': 'b', 'M8': 9, 1: (3, 0)}]}
>>> json_extract(json = bad_json,
    fuzzy_keys = True,
    filter_path = '..~~@(?i)[a-z]+\d~~^^', 
    get_full_path_also = True)
    # '~~^^' means "find the grandparents of the current container".
    # You could also get the parents with '~~^' or the great-grandparents 
    # with '~~^^^', and so on.
{('jub',): {'uy': [1, 2, 3], 'yu': [6, {'y': 'b', 'M8': 9, 1: (3, 0)}]}}
>>> json_extract(json = {'a':17, 'b':2, 'c': 4, 'd': 31}, 
    filter_path = 'zz^[a-z]vvnnx>3&&str(x)<`3`', 
    get_full_path_also=True)
    # Each value must satisfy BOTH constraints separated by the '&&'.
    # So the key has to start with a lowercase ASCII letter,
    # and the value has to have a numeric value greater than 3 ("x>3") AND
    # a string value less than '3' ("str(x)<`3`).
{('a',): 17}
>>> json_extract(json = bad_json,
    filter_path = "ggvvnnstr(x[`b`]) =~ `^\d`~~zz\dvvnnx<4")
    # The "=~" operator allows regex matching within a compute expression.
[2]
    '''
    if isinstance(filter_path, str):
        filter_path = parse_json_path(filter_path, fuzzy_keys = fuzzy_keys)
    elif not isinstance(filter_path, (tuple, list)):
        filter_path = [Filter(keys_in = filter_path)]
    if len(filter_path)==0:
        return []
    mutator = False
    if isinstance(filter_path[-1], Mutator):
        filter_path, mutator = filter_path[:-1], filter_path[-1]
    # gprint(filter_path)
    
    if type(json).__name__ != 'DataFrame':
        if get_full_path_also or mutator:
            # map paths to termini of those paths
            out =  dict(json_find_matches(json,
                                          json,
                                          filter_path = filter_path,
                                          get_full_path_also = True, 
                                          reverse_selectivity = reverse_selectivity, 
                                          recursive = recursive))
        else:
            # show only termini of good paths
            out =  list(json_find_matches(json,
                                          json,
                                          filter_path = filter_path,
                                          get_full_path_also = False, 
                                          reverse_selectivity = reverse_selectivity, 
                                          recursive = recursive))
        if mutator:
            mutator.mutate(json, out, ask_permission)
        else:
            return out
    else:
        df = json_find_matches_dataframe(json, filter_path, reverse_selectivity)
        if df.shape != (0, 0) and mutator:
            return mutator.replacement_func(df)
        return df




def parse_json_path_tuple(node, 
                          fuzzy_keys,
                          ask_about_ambiguity, 
                          possible_uncomputed_eqns, 
                          possible_nonfuzzy_regexes = None,
                          numer_mode = False, 
                          recursions = 0):
    '''Parses the key part or the value part of a json_path step.'''
    out = []
    if recursions:
        splitter = '&&'
    else:
        splitter = ';;' # separates a condition that does not have to be satisfied
                        # at the same time as any other conditions
    for elt in node.split(splitter):
        # print('    '*recursions + "in parse_json_path_tuple, elt = "+repr(elt))
        if elt[:2] == 'nn':
            numer_mode = not numer_mode
            elt = elt[2:]
        if '&&' in elt: # a tuple of bundled conditions within a tuple!
            out.append(parse_json_path_tuple(elt,
                                             fuzzy_keys,
                                             ask_about_ambiguity,
                                             possible_uncomputed_eqns,
                                             possible_nonfuzzy_regexes,
                                             numer_mode, 
                                             recursions + 1))
            continue
        if numer_mode:
            compute_result = compute(elt)
            out.append(compute_result)
        else:
            if (possible_nonfuzzy_regexes is not None) and (not fuzzy_keys):
                maybe_nonfuzzy_regex = re.findall("\\\\[ds]", elt)
                # "\s" and "\d" are probably the most 
                # distinctive features of regular expressions.
                possible_nonfuzzy_regexes.extend(maybe_nonfuzzy_regex)
            maybe_uncomputed_eqn = re.findall("(?:\d+|:|[`a-zA-Z]+)?[<>=!]=?(?:\d+|:|[`a-zA-Z]+)", elt)
            if maybe_uncomputed_eqn:
                possible_uncomputed_eqns.extend(maybe_uncomputed_eqn)
            out.append(elt)
    # print('    '*recursions+"In parse_json_path_tuple, out = "+repr(out))
    return out


def parse_json_path_step(elt, 
                         filters, 
                         layer, 
                         action, 
                         fuzzy_keys,
                         ask_about_ambiguity, 
                         possible_uncomputed_eqns,
                         possible_nonfuzzy_regexes):
    '''Parses a string representing a single substep in a json path layer as 
    described in parse_json_path.__doc__.'''
    global_constraint = False
    if elt == '..':
        filters[layer] = '..'
        return layer + 1, fuzzy_keys
    while elt[:2] in {'!!', 'zz', 'gg'}:
        if elt[:2] == 'gg':
            global_constraint = True
            elt = elt[2:]
            continue
        elif elt[:2] == 'zz':
            fuzzy_keys = not fuzzy_keys
            elt = elt[2:]
            continue
        elif filters.get(layer) is not None:
            raise JsonPathError("The reverse_selectivity-toggling '!!' token must be declared at the beginning of a filter layer. If you have one or more 'check' filters and then a non-check filter, the '!!' token must be before the first consecutive 'check' filter.")
        if elt[:2] == '!!':
            filters[layer] = '!!'
            layer += 1
            elt = elt[2:]
        
    key_or_val = False
    try:
        filters.setdefault(layer, [])
        val_part = elt.index('vv')
        e = [elt[:val_part], elt[val_part+2:]] #e[0] will be keys_in, e[1] vals_in
        # print(e)
        if e[0] == '':
            keys_in = tuple()
        else:
            if e[0][-2:] == '||':
                e[0] = e[0][:-2]
                key_or_val = True
            keys_in = parse_json_path_tuple(e[0],
                                            (fuzzy_keys and not global_constraint),
                                            ask_about_ambiguity, 
                                            possible_uncomputed_eqns,
                                            possible_nonfuzzy_regexes)
        vals_in = parse_json_path_tuple(e[1], 
                                        True, #fuzzy_keys only applies to keys.
                                        ask_about_ambiguity, 
                                        possible_uncomputed_eqns,
                                        None)
    except Exception as ex: # this is likely because there is no 'vv' in elt,
                            # causing a "ValueError: substring not found"
                            # at "val_part = elt.index('vv')". We assume this means
                            # that the user didn't intend to add any vals_in
                            # constraints
        if isinstance(ex, (JsonPathError, ComputeError)):
            raise JsonPathError(ex)
        keys_in = parse_json_path_tuple(elt, 
                                        (fuzzy_keys and not global_constraint),
                                        ask_about_ambiguity, 
                                        possible_uncomputed_eqns,
                                        possible_nonfuzzy_regexes)
        vals_in = tuple()
    if global_constraint:
        filters[layer].append(GlobalConstraint(keys_in = keys_in,
                                               vals_in = vals_in,
                                               action = action))
    else:
        filters[layer].append(Filter(keys_in, 
                                     vals_in, 
                                     key_or_val, 
                                     action, 
                                     fuzzy_keys))
    updown_count = sum(filt.action != 'check' for filt in filters[layer])
    if updown_count > 1:
        raise JsonPathError("Error at filter layer {}: Cannot have more than one filter with an action other than 'check'".format(layer))
    if action == 'check':
        return layer, fuzzy_keys
    return layer+1, fuzzy_keys


def parse_json_path(x, 
                    fuzzy_keys = False, 
                    ask_about_ambiguity = True):
    """*x*: a string.

*fuzzy_keys*: See the same argument of json_extract.__doc__.

*ask_about_ambiguity*: Print possibly helpful messages when x appears to have a
    malformed pipe, a missing 'nn' for declaring "compute mode",
    or a missing 'zz' for declaring fuzzy_keys mode when using regexes.

RULES FOR PARSING AN ENTIRE JSON PATH ('x'):
    
    * x is split into path layers or substeps by one of the delimiters 
    {'~~', '~~@', '~~^+'), '~~}'}.
        
        * '~~' means that the preceding path substep serves as a "check"; 
        (de/a)scent to a child or parent cannot proceed unless all checks 
        at a path layer are satisfied.
        There can be any number of checks at a path layer.
        
        * '~~@' comes at the end of a path layer; it means that once all the 
        checks are satisfied at the current path layer, you begin searching 
        the CHILDREN of all nodes that satisfied the preceding check.
        
        * '~~^+' also comes at the end of a path layer; it means that
        once all the checks are satisfied at the current path layer, you 
        begin searching the n^th ancestor of the current level of json, 
        where n is the number of '^' characters.
        
        * '~~}' can be supplied as the last three characters of a path.
        It means that if the all the checks in the current layer of json were
        satisfied, you return the CURRENT LAYER, not children or ancestors.
        
        * Descent-type-search (as specified by '~~@') is the default, so the 
        final path layer will always return the children of all matched nodes
        unless the path is terminated with '~~}' or '~~^+'.
    
    * '..' switches json_extract into recursive search mode.
    Recursive search mode is off by default.
    
    * '!!' as its own path layer or at the beginning of another path layer 
    is treated as a special indicator that toggles reverse_selectivity mode.
    
    * 'zz' at the beginninng of another path layer toggles fuzzy_keys, which 
    changes the fuzzy_keys parameter of the Filters created by this function.
    
    * 'gg' at any point in a path layer (including on a "check" filter in a
    multi-substep path layer) creates a GlobalConstraint rather than a Filter.
    
    * '~~ss<func of one variable>' as the FINAL ELEMENT IN A PATH
    (even after '~~}')
    ends the path with a :class:`Mutator` object that can be used to perform in-place
    transformations on the JSON after paths have been found by 
    json_extract() or JsonPath.extract().


RULES FOR PARSING A SINGLE PATH SUBSTEP (performed by parse_json_path_step):
    
    * 'nn' at any point in a path substep toggles "compute mode".
    While the parser is in "compute mode", it interprets everything as a
    mathematical expression, and passes it into :func:`math_eval.compute`.
    Thus, it is easier to include string filters at the beginning of a tuple
    path substep and numeric filters at the end of a tuple path substep.
    
    * ';;' separates two elements within the path substep.
    
    * '&&' separates two elements within the path substep, and every 
    consecutive element joined by '&&' is bundled together; 
    so 'cond1;;cond2&&cond3;;cond4' 
    would filter on cond1 OR (cond2 AND cond3) OR cond4.
    
    * 'vv' is a delimiter. 
    everything after 'vv' in the path substep is a filter on VALUES and 
    everything before 'vv' is a filter on KEYS.
        * Note that 'vv' resets the 'nn' flag.
        This means that you need to use 'nn' to turn on compute mode 
        separately for values and keys.
        * Note also that for a GlobalConstraint, everything after the 'vv' 
        flag is a filter on the iterable as a whole.
    
    * By default, a path substep must match at least one key filter AND at 
    least one value filter, assuming both key and value filters are supplied.
    
    * '||' is an optional indicator that can be used with 'vv'.
    When '||' is supplied, the filter at that path substep only requires that
    a key filter OR a value filter is matched.
    
        * The '||' flag does not do anything when used on a GlobalConstraint.
    
    * When not in compute mode, all strings (including numeric strings) are 
    treated as regular expressions if fuzzy_keys = True and not inside a 
    :class:`GlobalConstraint`.
    Otherwise, they are treated as plain strings.

EXAMPLES: 
________

>>> parse_json_path("nn5:8vv77")
[[Filter(keys_in = [IntRange(5, 8, 1)], vals_in = ['77'], key_or_val = False, action = 'down', fuzzy_keys = False)]]
>>> parse_json_path("\\d\\n~~}") # don't forget to turn on fuzzy_keys if you want regex!
ALERT: It looks like you may have tried to match keys with regular expressions
['\\d'] while not in fuzzy_keys mode. Did you intend this?
[[Filter(keys_in = ['\\d\\n'], vals_in = [], key_or_val = False, action = 'stay', fuzzy_keys = False)]]
>>> parse_json_path("zzx*3<=4**3")
ALERT: It looks like you may have forgotten to use the 'nn' token to indicate that the equation(s)
['3<=4'] should be treated as math expressions. Did you intend this?
[[Filter(keys_in = ['x*3<=4**3'], vals_in = [], key_or_val = False, action = 'down', fuzzy_keys = True)]]
>>> parse_json_path("^[a-z]{2}$||vvnnx<3&&x>2;;nn^[23]", fuzzy_keys = True)
    # the "nnx<3&&x>2" means that the conditions "x<3" and "x>2" must BOTH be satisfied.
    # The other condition, "^[23]", wants the value to be a string starting with '2' or 
    # '3'. 
    # So long as BOTH of the first two conditions OR the third condition is/are satisfied,
    # this vals_in requirement is met.
[[Filter(keys_in = ["^[a-z]{2}$"], vals_in = [[compute('x<3'), compute('x>2')], "^[23]"], key_or_val = True, action = 'down', fuzzy_keys = True)]]
>>> parse_json_path("3~~ggnn1:4:2vvnnx[0]>1")
[[Filter(keys_in = ['3'], vals_in = [], key_or_val = False, action = 'check', fuzzy_keys = False), GlobalConstraint(keys_in = [IntRange(1, 4, 2)], vals_in = [compute('x[0]>1')], action = 'down')]] 
>>> parse_json_path('..~~@yu~~zzvvuy~~^^')
['..', [Filter(keys_in = ['yu'], vals_in = [], key_or_val = False, action = 'check', fuzzy_keys = False)], [Filter(keys_in = [], vals_in = ['uy'], key_or_val = False, action = 'up2', fuzzy_keys = True)], [Filter(keys_in = [''], vals_in = [], key_or_val = False, action = 'down', fuzzy_keys = True)]]
>>> parse_json_path('a~~@nn1:~~}~~ss str(x)')
[[Filter(keys_in = ['a'], vals_in = [], key_or_val = False, action = 'down', fuzzy_keys = False)], [Filter(keys_in = [IntRange(1, inf, 1)], vals_in = [], key_or_val = False, action = 'stay', fuzzy_keys = False)], Mutator(replacement_func = 'compute( str(x))')]
    """
    mutator = False
    if '~~ss' in x:
        x, replacement_funcname = x.split('~~ss')
        mutator = Mutator(replacement_funcname)
    arr = re.split('(~~(?:\^+|[@\}])?)', x)
    possible_uncomputed_eqns = []
    possible_nonfuzzy_regexes = []
    if ask_about_ambiguity:
        possible_malformed_pipes = re.findall("(?<!~)~[@\^\}]", x)
        if possible_malformed_pipes:
            pass
            print("ALERT: It looks like you included path-splitting pipe(s) with only one '~': {}.\nIs this what you intended?".format(possible_malformed_pipes))
    filters = {}
    layer = 0
    for ii, elt in enumerate(arr):
        if ii == len(arr)-1:
            action = 'down'
        elif arr[ii+1] == '~~':
            action = 'check'
        elif re.search("~~\^+", arr[ii+1]):
            action = 'up'+str(arr[ii+1].count("^"))
        elif arr[ii+1] == '~~@':
            action = 'down'
        elif arr[ii+1] == '~~}':
            action = 'stay'
        if elt[:2] == '~~':
            if len(elt)==3 and elt == '~~}':
                break
            continue
        layer, fuzzy_keys = parse_json_path_step(elt, 
                                     filters,
                                     layer, 
                                     action,
                                     fuzzy_keys,
                                     ask_about_ambiguity, 
                                     possible_uncomputed_eqns,
                                     possible_nonfuzzy_regexes)
    if ask_about_ambiguity and possible_uncomputed_eqns:
        pass
        print("ALERT: It looks like you may have forgotten to use the 'nn' token to indicate that the equation(s)\n{} should be treated as math expressions. Did you intend this?".format(possible_uncomputed_eqns))
    if ask_about_ambiguity and possible_nonfuzzy_regexes:
        pass
        print("ALERT: It looks like you may have tried to match keys with regular expressions\n{} while not in fuzzy_keys mode. Did you intend this?".format(possible_nonfuzzy_regexes))
    if mutator:
        return [filt for lay, filt in sorted(filters.items(), key = lambda x: x[0])] \
               + [mutator]
    return [filt for lay, filt in sorted(filters.items(), key = lambda x: x[0])]


def mutate_json(obj, path, func, ask_permission = False, **kwargs):
    '''Mutates a nested iterable object in-place by applying func to obj[path].

*obj*: an object containing arbitrarily nested iterables.

*path*: a tuple of keys or indices to follow through the object.

*func*: a function to apply to the child found at the end of the path, OR a 
non-function that everything should be replaced by, regardless of its value.

*ask_permission*: if True, ask before changing the node. Useful when this is 
called repeatedly by other functions.

**Returns:** None.'''
    level = kwargs.get('level', 0)
    if level == len(path):
        if not hasattr(func, '__call__'):
            out = func
        else:
            out = func(obj)
        if ask_permission:
            print("At path {p},\n{obj_short}\n    would be replaced by\n{out_short}.".format(p=path, obj_short=compressed_obj_repr(obj), out_short=compressed_obj_repr(out)))
            decision = input("Do you want to do this? (y/n) ")
            if decision == 'y':
                return out
            else:
                next_decision = input("Do you want to quit? (y/n) ")
                if next_decision == 'y':
                    raise JsonPathError("mutate_json halted at user request.")
                return obj
        return out
    obj[path[level]] = mutate_json(obj[path[level]], 
                                   path, 
                                   func, 
                                   ask_permission,
                                   level = level+1)
    if (level != 0):
        return obj


def mutate_json_repeatedly(obj, paths, func, ask_permission = False):
    '''See mutate_json. This applies the func to obj[path] for each path in paths.'''
    for ii, p in enumerate(paths):
        if not is_iterable(p):
            p = (p,)
        try:
            mutate_json(obj, p, func, ask_permission)
        except Exception as ex:
            if 'halted at user request' in repr(ex):
                return
            raise JsonPathError(ex)
        if ask_permission and ii < len(paths)-1:
            ask_permission = (input("There are {numpaths} nodes remaining that may be replaced. Do you still want to be asked permission? (y/n) ".format(numpaths= len(paths)-ii-1)) == 'y')


class JsonPath:
    '''Class for manipulating and traversing filter paths.

**Initialization args:**

*filters_or_query*: a list of layers of Filters and GlobalConstraints; or a 
query that can be parsed by parse_json_path and translated into such a list.

*json*: a nested Python object. This can be added later by add_json().

*fuzzy_keys*: See the documentation for the :class:`Filter` class and :func:`json_extract`.

**Attributes:**

*filters*: A list of layers of Filters and GlobalConstraints, along with '..' 
and '!!' flags.

*mutator*: The final item in the "filters" list passed in when initialized.
This is a Mutator object that mutates the JSON passed in to this func.

*curLayer*: Tracks what index of the filters the JsonPath will start 
traversing from. This can be manipulated with :func:`JsonPath.descend` to see how the 
resultset changes.

**Methods:**
    *'+'*: Two JsonPaths can be added together to concatenate their filters; 
    the JsonPath produced by (a+b) has a's JSON.
    You can also add a JsonPath to a list of filters, or vice versa.

    *copy()*: Returns a new JsonPath with no associated json.

    *descend()*: Allows examination of how each filter layer changes the 
    resultset.

    *extract()*: Like json_extract().

    *sub()*: Finds all the paths from extract(), then applies a function to 
    each child node found. This is an in-place transformation.

**Other notes:**

You can access slices and individual filter layers in a JsonPath with the 
[a:b] or [a] array-slicing notation.
    '''
    def __init__(self, 
                 filters_or_query,
                 json = None,
                 fuzzy_keys = False):
        self.json = json
        self.resultset = None
        self.mutator = None
        self.curLayer = 0
        self._initial_fuzzy_keys = fuzzy_keys # handy because fuzzy_keys can change
        self.fuzzy_keys = fuzzy_keys
        if isinstance(filters_or_query, str):
            self.query = filters_or_query
            self.filters = parse_json_path(filters_or_query, fuzzy_keys)
            for layer in self.filters:
                if isinstance(layer, list):
                    for filt in layer:
                        if hasattr(filt, 'fuzzy_keys'):
                            self.fuzzy_keys = filt.fuzzy_keys
        else:
            self.query = None
            self.filters = filters_or_query
        if isinstance(self.filters[-1], Mutator):
            self.filters, self.mutator = self.filters[:-1], self.filters[-1]
            
    def add_filters(self, filters_or_query):
        '''filters_or_query: a query parsed by parse_json_path that returns a list of
    filter layers, or a list of filter layers.
Adds new filters to the end of the this JsonPath's 'filters' attribute.'''
        if len(self.filters[-1]) == 1 \
        and (self.filters[-1][0].keys_in == [''] or (not self.filters[-1][0].keys_in)) \
        and not self.filters[-1][0].vals_in:
            # this is a filter with no specification for keys or values, which could
            # have been made by terminating a parsed path with a path-separating pipe
            self.filters.pop()
        if isinstance(filters_or_query, str):
            self.filters.extend(parse_json_path(filters_or_query, 
                                                fuzzy_keys = self.fuzzy_keys))
        else:
            self.filters.extend(filters_or_query)
            
    def __getitem__(self, slice_or_ind):
        return JsonPath(self.filters[slice_or_ind], self.json, self._initial_fuzzy_keys)
        
    def __setitem__(self, slice_or_ind, new_filters):
        if isinstance(new_filters, JsonPath):
            if isinstance(slice_or_ind, int):
                if slice_or_ind < 0:
                    slice_or_ind = len(self) + slice_or_ind
                # need to make sure that we don't put a filter layer inside of an
                # existing filter layer
                self.filters[slice_or_ind:slice_or_ind+1] = new_filters.filters
            else:
                self.filters[slice_or_ind] = new_filters.filters
        else:
            self.filters[slice_or_ind] = new_filters
            
    def __delitem__(self, slice_or_ind):
        del self.filters[slice_or_ind]
        
    def __add__(self, other_JsonPath):
        if isinstance(other_JsonPath, JsonPath):
            return JsonPath(self.filters + other_JsonPath.filters, 
                            self.json, 
                            self._initial_fuzzy_keys)
        elif isinstance(other_JsonPath, list):
            # add a list of filters to this JsonPath.
            return JsonPath(self.filters + other_JsonPath, 
                            self.json,
                            self._initial_fuzzy_keys)
        raise TypeError("Can only add lists of filters and other JsonPaths to JsonPaths.")
        
    def __radd__(self, other_JsonPath):
        if isinstance(other_JsonPath, JsonPath):
            # (a + b) keeps a's JSON; (b + a) keeps b's JSON. 
            return JsonPath(other_JsonPath.filters + self.filters, 
                            other_JsonPath.json,
                            other_JsonPath._initial_fuzzy_keys)
        elif isinstance(other_JsonPath, list):
            return JsonPath(other_JsonPath + self.filters, 
                            self.json,
                            self._initial_fuzzy_keys)
        raise TypeError("Can only add lists of filters and other JsonPaths to JsonPaths.")
            
    def copy(self):
        '''Return a new JsonPath with the same filters but no associated JSON.'''
        return JsonPath(self.filters.copy())
            
    def __str__(self):
        return "JsonPath(filters_or_query = {},\nfuzzy_keys = {},\njson = {})".format(gprint(self.filters, str), self.fuzzy_keys, compressed_obj_repr(self.json))
    __repr__ = __str__
    
    def __len__(self):
        return len(self.filters)
        
    def add_json(self, json):
        '''Set this JsonPath's 'json' attribute to json. Resets resultset and 
    curLayer.''' 
        self.curLayer = 0
        self.json = json
        self.resultset = None
    
    def follow_path(self, layers = None):
        '''See the documentation for JsonPath.descend().

This is mainly useful as a helper function for JsonPath.descend(), which is 
in turn a helper function for JsonPath.extract().

EXAMPLES:
________
>>> list(JsonPath('a~~@nn1:', json={'a':[1,2,3],'b':2}).follow_path(1))
    # only applies the first filter, which finds key 'a' and then descends
[(('a',), [1, 2, 3])]
>>> dict(JsonPath('a~~@nn1:', json={'a':[1,2,3],'b':2}).follow_path())
    # no path was specified, so it applies both filters and descends to json['a']
    # and then json['a'][1:]
{('a', 1): 2, ('a', 2): 3}
>>> jpath_ex = JsonPath('a~~@nn1:', json={'a':[1,2,3],'b':2})
>>> dict(jpath_ex.follow_path(1)) 
    # note that calling follow_path(1) increases its curLayer from 0 to 1
{('a',): [1, 2, 3]}
>>> dict(jpath_ex.follow_path(1)) 
    # now calling follow_path(1) increases its curLayer from 1 to 2,
    # but the first call didn't update the resultset so we get nothing.
    # use descend() to update the resultset.
{}
        '''
        if self.curLayer == len(self):
            raise StopIteration("Traversal of this JsonPath is complete.")
        if layers is None:
            path_continued = self.filters[self.curLayer:]
            self.curLayer = len(self)
        else:
            path_continued = []
            ii = 0
            # print({"ii":ii, "curLayer": self.curLayer, "filters[curLayer+ii]":self.filters[self.curLayer+ii], 'path_continued': path_continued})
            while ii < layers:
                path_continued.append(self.filters[self.curLayer+ii])
                if isinstance(self.filters[self.curLayer+ii], str):
                    # it's a '..' indicating the switch to recursive mode
                    # or a '!!' indicating the switch to "reverse_selectivity" mode.
                    layers += 1
                ii += 1
            self.curLayer += layers
        
        if self.resultset is not None:
            for curpath, subgraph in self.resultset.items():
                yield from json_find_matches(self.json,
                                        subgraph,
                                        path_continued, 
                                        curpath = curpath, 
                                        get_full_path_also=True)
        else:
            yield from json_find_matches(self.json,
                                        self.json,
                                        path_continued, 
                                        curpath = tuple(), 
                                        get_full_path_also=True)
        
    def descend(self, layers = None):
        '''layers: The number of layers of this JsonPath's filters to traverse.

If layers is None, just use all of the Filters and GlobalConstraints in this
JsonPath.

Returns None, but updates the JsonPath's resultset so that repeated calls to 
descend() followed by peeks at its resultset show you how its resultset 
evolves as the filters are successively applied.

Note that the traversal starts at self.curLayer, which may not be the first 
layer.

EXAMPLES:
________
>>> jpath_ex = JsonPath('a~~@nn1:', json={'a':[1,2,3],'b':2})
>>> jpath_ex.resultset
>>> jpath_ex.curLayer
0
>>> jpath_ex.descend(1) 
    # applies the filter(s) in layer 0, and descends to layer 1.
>>> jpath_ex.resultset
{('a',): [1, 2, 3]}
>>> jpath_ex.descend(1) # applies the filters in layer 1, which is the last layer
>>> jpath_ex.resultset
{('a', 1): 2, ('a', 2): 3}
        '''
        new_resultset = {}
        for newpath, newgraph in self.follow_path(layers):
            new_resultset[newpath] = newgraph
        self.resultset = new_resultset
        
    def extract(self, layers = None):
        '''With no arguments, this is equivalent to json_extract(self.json).
If layers is an int, it's equivalent to 
:func:`json_extract`(self.json, self.filters[:layers]),
unless one or more layers is '..' or '!!', because '..' and '!!' don't count
as their own filter layers.'''
        if re.search('DataFrame', str(type(self.json))):
            # the json is a DataFrame, which is extracted differently
            return json_find_matches_dataframe(self.json,
                                               self.filters[:layers])
        self.curLayer = 0
        self.descend(layers)
        self.curLayer = 0
        out = self.resultset
        self.resultset = None
        return out
        
    def sub(self, func = None, ask_permission = False, layers = None):
        '''Applies func to the terminal nodes of all the paths found by
    self.extract(layers).
    If func is None, uses this JsonPath's mutator to alter the JSON.
See the documentation for :func:`mutate_json` and :func:`JsonPath.extract`.
WARNING: This is an IN-PLACE transformation.
If you're concerned about making unintended changes, use ask_permission=True.

PERFORMANCE NOTE: If you intend to use the results from extract() and then 
use sub(), the below will save time by not calling extract() twice::
    
    >>> results = jp.extract() # jp is a JsonPath
    >>> mutate_json_repeatedly(jp.json, results.keys(), jp.mutator.replacement_func)

EXAMPLES:
________
>>> jpath_ex = JsonPath('a~~@nn1:', json={'a':[1,2,3],'b':2})
>>> jpath_ex.sub(lambda x: (x+1)*2, False)
>>> jpath_ex.json
{'a':[1,6,8], 'b':2}
>>> jpath_ex.sub(lambda x: (x+1)*2, True)
At path ('a', 1),
6
    would be replaced by
14.
Do you want to do this? (y/n) y
There are 1 nodes remaining that may be replaced. Do you still want to be asked permission? (y/n) y
At path ('a', 2),
8
    would be replaced by
18.
Do you want to do this? (y/n) n
Do you want to quit? (y/n) y
>>> JsonPath('b~~@nn1:', json = jpath_ex.json).sub(lambda x: x*3, False, 1)
    # note that we supplied layers = 1, so this will only traverse the first filter
    # layer before trying to make replacements.
>>> jpath_ex.json
{'a':[1, 14, 8], 'b':6}
>>> JsonPath('a~~@nn1:~~ss str(x)', json = jpath_ex.json).sub(ask_permission=False, 
                                                             layers = 2)
    # Here we are using the syntax of parse_json_path that allows us to add a Mutator
    # to a JsonPath by terminating the JsonPath string with "~~ss<func of 1 variable>"
>>> jpath_ex.json
{'a':[1, '14', '8'], 'b':6}
        '''
        if func is None:
            func = self.mutator.replacement_func
        if re.search('DataFrame', str(type(self.json))):
            # the json is a DataFrame, which is extracted differently
            results = self.extract(layers)
            rows, cols = list(results.index), list(results.columns)
            decision = 'y'
            replacement = func(self.json.loc[rows, cols])
            if ask_permission:
                print(self.json.loc[rows, cols])
                print("would be replaced by")
                print(replacement)
                decision = input("Is this OK? ")
            if decision == 'y':
                self.json.loc[rows, cols] = replacement
            return
        paths = list(self.extract(layers).keys())
        mutate_json_repeatedly(self.json, paths, func, ask_permission)
