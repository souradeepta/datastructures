import pytest
from python.basic.stack import ListStack


class TestStack:
    def test_push_and_pop(self):
        s = ListStack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_peek(self):
        s = ListStack()
        s.push(42)
        assert s.peek() == 42
        assert s.size() == 1

    def test_is_empty(self):
        s = ListStack()
        assert s.is_empty()
        s.push(1)
        assert not s.is_empty()

    def test_pop_empty_raises(self):
        s = ListStack()
        with pytest.raises(IndexError):
            s.pop()

    def test_size(self):
        s = ListStack()
        for i in range(5):
            s.push(i)
        assert s.size() == 5
