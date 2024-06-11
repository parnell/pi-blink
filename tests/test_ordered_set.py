import pytest

from pi_blink.ordered_set import OrderedSet


@pytest.fixture
def ordered_set() -> OrderedSet:
    return OrderedSet([1, 2, 3])


def test_add(ordered_set: OrderedSet):
    ordered_set.add(4)
    assert 4 in ordered_set
    assert list(ordered_set) == [1, 2, 3, 4]


def test_discard(ordered_set: OrderedSet):
    ordered_set.discard(2)
    assert 2 not in ordered_set
    assert list(ordered_set) == [1, 3]


def test_contains(ordered_set: OrderedSet):
    assert 1 in ordered_set
    assert 4 not in ordered_set


def test_len(ordered_set: OrderedSet):
    assert len(ordered_set) == 3
    ordered_set.add(4)
    assert len(ordered_set) == 4


def test_iter(ordered_set: OrderedSet):
    assert list(iter(ordered_set)) == [1, 2, 3]


def test_repr(ordered_set: OrderedSet):
    assert repr(ordered_set) == "PartialSet([1, 2, 3])"


def test_eq(ordered_set: OrderedSet):
    other_set = OrderedSet([1, 2, 3])
    assert ordered_set == other_set
    other_set.add(4)
    assert ordered_set != other_set


def test_clear(ordered_set: OrderedSet):
    ordered_set.clear()
    assert len(ordered_set) == 0
    assert list(ordered_set) == []


def test_pop(ordered_set: OrderedSet):
    popped = ordered_set.pop()
    assert popped == 1
    assert list(ordered_set) == [2, 3]
    ordered_set.pop()
    ordered_set.pop()
    with pytest.raises(KeyError):
        ordered_set.pop()


def test_update(ordered_set: OrderedSet):
    a = [4, 5]
    ordered_set.update(a)
    assert list(ordered_set) == [1, 2, 3, 4, 5]


def test_getitem(ordered_set: OrderedSet):
    assert ordered_set[0] == 1
    assert ordered_set[1] == 2


def test_reversed(ordered_set: OrderedSet):
    assert list(reversed(ordered_set)) == [3, 2, 1]


def test_isinstance():
    os = OrderedSet()
    assert isinstance(os, set)
    assert isinstance(os, OrderedSet)


def test_copy(ordered_set):
    copied_set = ordered_set.copy()
    assert copied_set == ordered_set
    assert copied_set is not ordered_set
    copied_set.add(4)
    assert copied_set != ordered_set


def test_copy_returns_int(ordered_set):
    copied_set = ordered_set.copy()
    for i in copied_set:
        assert isinstance(i, int)


def test_iteration_returns_keys2(ordered_set):
    for i in ordered_set:
        assert isinstance(i, int)


def test_iteration_returns_keys(ordered_set):
    keys = list(ordered_set)
    assert keys == [1, 2, 3]


if __name__ == "__main__":
    pytest.main([__file__])
