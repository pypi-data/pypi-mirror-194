import cnest

from collections import namedtuple, OrderedDict
import unittest
import time

NTuple = namedtuple('NTuple', ['a', 'b'])  # default value will be None


def _generate_deep_nest(depth=10, keys=['a', 'b']):
    if depth == 1:
        return dict(zip(keys, range(len(keys))))
    x = _generate_deep_nest(depth - 1, keys)
    return dict(zip(keys, [x] * len(keys)))


def _time(func, msg, *args):
    t0 = time.time()
    ret = func(*args)
    print("%s: %s" % (msg, time.time() - t0))
    return ret


def is_namedtuple(value):
    """Whether the value is a namedtuple instance.
    Args:
        value (Object):
    Returns:
        ``True`` if the value is a namedtuple instance.
    """

    return isinstance(value, tuple) and hasattr(value, '_fields')


def is_unnamedtuple(value):
    """Whether the value is an unnamedtuple instance."""
    return isinstance(value, tuple) and not is_namedtuple(value)


def assert_same_length(seq1, seq2):
    assert len(seq1) == len(seq2), \
        "Different lengths! {} <-> {}".format(len(seq1), len(seq2))


def assert_same_type(value1, value2):
    assert (type(value1) == type(value2)
            or (isinstance(value1, dict) and isinstance(value2, dict))), (
                "Different types! {} <-> {}".format(
                    type(value1), type(value2)))


def is_nested(value):
    """Returns true if the input is one of: ``list``, ``unnamedtuple``, ``dict``,
    or ``namedtuple``. Note that this definition is different from tf's is_nested
    where all types that are ``collections.abc.Sequence`` are defined to be nested.
    """
    return isinstance(value, (list, tuple, dict))


def py_flatten(nest):
    """Returns a flat list from a given nested structure."""
    if not is_nested(nest):
        # any other data type will be returned as it is
        return [nest]
    flattened = []
    if isinstance(nest, list) or is_unnamedtuple(nest):
        for value in nest:
            flattened.extend(py_flatten(value))
    else:
        for _, value in extract_fields_from_nest(nest):
            flattened.extend(py_flatten(value))
    return flattened


def py_assert_same_structure(nest1, nest2):
    """Asserts that two structures are nested in the same way."""
    # When neither is nested, the assertion won't fail
    if is_nested(nest1) or is_nested(nest2):
        try:
            assert_same_type(nest1, nest2)
            assert_same_length(nest1, nest2)
        except AssertionError as e:
            logging.error(str(e))
            raise AssertionError(
                "assert_same_structure() fails between {} and {}".format(
                    nest1, nest2))

        if isinstance(nest1, list) or is_unnamedtuple(nest1):
            for value1, value2 in zip(nest1, nest2):
                py_assert_same_structure(value1, value2)
        else:
            for fv1, fv2 in zip(
                    extract_fields_from_nest(nest1),
                    extract_fields_from_nest(nest2)):
                assert fv1[0] == fv2[0], \
                    "Keys are different !{} <-> {}".format(fv1[0], fv2[0])
                py_assert_same_structure(fv1[1], fv2[1])


def py_map_structure(func, *nests):
    """Applies func to each entry in structure and returns a new structure."""
    assert nests, "There should be at least one input nest!"
    for nest in nests[1:]:
        py_assert_same_structure(nests[0], nest)

    def _map(*nests):
        if not is_nested(nests[0]):
            return func(*nests)
        if isinstance(nests[0], list) or is_unnamedtuple(nests[0]):
            ret = type(nests[0])([_map(*values) for values in zip(*nests)])
        else:
            ret = {}
            for fields_and_values in zip(
                    *[extract_fields_from_nest(nest) for nest in nests]):
                field = fields_and_values[0][0]
                values = map(lambda fv: fv[1], fields_and_values)
                ret[field] = _map(*values)
            ret = type(nests[0])(**ret)
        return ret

    return _map(*nests)


def py_pack_sequence_as(nest, flat_seq):
    """Returns a given flattened sequence packed into a given structure."""
    assert_same_length(py_flatten(nest), flat_seq)
    counter = [0]

    def _pack(nest, flat_seq):
        if not is_nested(nest):
            ret = flat_seq[counter[0]]
            counter[0] += 1
            return ret

        if isinstance(nest, list) or is_unnamedtuple(nest):
            ret = type(nest)([_pack(value, flat_seq) for value in nest])
        else:
            ret = {}
            for field, value in extract_fields_from_nest(nest):
                ret[field] = _pack(value, flat_seq)
            ret = type(nest)(**ret)
        return ret

    return _pack(nest, list(flat_seq))


def extract_fields_from_nest(nest):
    """Extract fields and the corresponding values from a nest if it's either
    a ``namedtuple`` or ``dict``.
    Args:
        nest (nest): a nested structure
    Returns:
        Iterable: an iterator that generates ``(field, value)`` pairs. The fields
        are sorted before being returned.
    Raises:
        AssertionError: if the nest is neither ``namedtuple`` nor ``dict``.
    """
    assert is_namedtuple(nest) or isinstance(nest, dict), \
        "Nest {} must be a dict or namedtuple!".format(nest)
    fields = nest.keys() if isinstance(nest, dict) else nest._fields
    for field in sorted(fields):
        value = nest[field] if isinstance(nest, dict) else getattr(nest, field)
        yield field, value


class TestIsNamedtuple(unittest.TestCase):
    def test_is_namedtupe(self):
        x = dict(a=1)
        y = NTuple(a=1, b='x')
        z = (1, 2, '3')

        self.assertFalse(cnest._is_namedtuple(x))
        self.assertFalse(cnest._is_namedtuple(z))
        self.assertTrue(cnest._is_namedtuple(y))


class TestIsUnnamedtuple(unittest.TestCase):
    def test_is_unnamedtupe(self):
        x = dict(a=1)
        y = NTuple(a=1, b='x')
        z = (1, 2, '3')

        self.assertFalse(cnest._is_unnamedtuple(x))
        self.assertFalse(cnest._is_unnamedtuple(y))
        self.assertTrue(cnest._is_unnamedtuple(z))


class TestAssertSameType(unittest.TestCase):
    def test_assert_same_type(self):
        x = NTuple(a=1, b=2)
        y = NTuple(a=1, b=1)
        a = [1, 2]
        b = [3]
        c = (1, 2)
        cnest._assert_same_type(x, y)
        cnest._assert_same_type(a, b)
        self.assertRaises(RuntimeError, cnest._assert_same_type, a, c)

        a = dict(x=1)
        b = OrderedDict([('x', 1), ('y', 2)])
        cnest._assert_same_type(a, b)

        self.assertRaises(RuntimeError, cnest._assert_same_type, x, a)

        z = (1, 2)
        self.assertRaises(RuntimeError, cnest._assert_same_type, x, z)


class TestAssertSameLength(unittest.TestCase):
    def test_assert_same_length(self):
        x = NTuple(a=1, b=2)
        a = [1, 2]
        c = dict(x=3, y=dict(x=1, y=2))

        cnest._assert_same_length(x, a)
        cnest._assert_same_length(a, c)

        self.assertRaises(RuntimeError, cnest._assert_same_length, a, 1)


class TestExtractFieldsFromNest(unittest.TestCase):
    def test_extract_fields(self):
        x = NTuple(a=dict(x=1), b=1)
        y = dict(aa=1, bb=2)
        z = (1, 2)
        a = {1: 'x', 2: 'y'}

        self.assertTrue(isinstance(cnest._extract_fields_from_nest(x), list))
        self.assertEqual(
            cnest._extract_fields_from_nest(y), [('aa', 1), ('bb', 2)])
        self.assertRaises(RuntimeError, cnest._extract_fields_from_nest, z)
        # only support string keys
        self.assertRaises(RuntimeError, cnest._extract_fields_from_nest, a)


class TestFlatten(unittest.TestCase):
    def test_flatten_time(self):
        nested = _generate_deep_nest(depth=6, keys=list(map(str, range(10))))
        flat1 = _time(cnest.flatten, "cnest flatten", nested)
        flat2 = _time(py_flatten, "nest flatten", nested)
        self.assertEqual(flat1, flat2)


class TestAssertSameStructure(unittest.TestCase):
    def test_assert_same_structure_time(self):
        nested = _generate_deep_nest(depth=6, keys=list(map(str, range(10))))
        _time(cnest.assert_same_structure, "cnest assert_same_structure",
              nested, nested)
        _time(py_assert_same_structure, "nest assert_same_structure",
              nested, nested)


class TestMapStructure(unittest.TestCase):
    def test_map_structure_time(self):
        nested = _generate_deep_nest(depth=6, keys=list(map(str, range(10))))

        ret1 = _time(cnest.map_structure,
                     "cnest map_structure", lambda x, y: x + y, nested, nested)
        ret2 = _time(py_map_structure,
                     "nest map_structure", lambda x, y: x + y, nested, nested)
        self.assertEqual(cnest.flatten(ret1), cnest.flatten(ret2))


class TestPackSequenceAs(unittest.TestCase):
    def test_pack_sequence_as_time(self):
        nested = _generate_deep_nest(depth=5, keys=list(map(str, range(10))))
        flat = cnest.flatten(nested)

        nest1 = _time(cnest.pack_sequence_as, "cnest pack_sequence_as", nested,
                      flat)
        nest2 = _time(py_pack_sequence_as, "nest pack_sequence_as",
                      nested, flat)
        cnest.assert_same_structure(nest1, nest2)


if __name__ == '__main__':
    unittest.main()
