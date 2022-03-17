from unittest import TestCase

from repository.iterabledatastructure import IterableStructure


class TestIterableStructure(TestCase):
    def setUp(self):
        self.iterable1 = IterableStructure()
        self.iterable1.append(2)
        self.iterable1.append(5)
        self.iterable1.append(4)
        self.iterable1.append(3)
        self.iterable1.append(1)
        self.iterable2 = IterableStructure()
        self.iterable2.append("q")
        self.iterable2.append("b")
        self.iterable2.append("w")
        self.iterable2.append("a")
        self.iterable2.append("r")

    def test_data(self):
        self.assertEqual(self.iterable1.data, [2, 5, 4, 3, 1])
        self.assertEqual(self.iterable2.data, ["q", "b", "w", "a", "r"])

    def test_setitem(self):
        self.iterable1[0] = 6
        self.assertEqual(self.iterable1.data, [6, 5, 4, 3, 1])
        self.iterable2[0] = "a"
        self.assertEqual(self.iterable2.data, ["a", "b", "w", "a", "r"])

    def test_getitem(self):
        self.assertEqual(self.iterable1[0], 2)
        self.assertEqual(self.iterable2[0], "q")

    def test_delitem(self):
        del self.iterable1[0]
        self.assertEqual(self.iterable1.data, [5, 4, 3, 1])
        del self.iterable2[0:2]
        self.assertEqual(self.iterable2.data, ["w", "a", "r"])

    def test_len(self):
        self.assertEqual(5, len(self.iterable1.data))
        self.assertEqual(5, len(self.iterable2.data))

    def test_append(self):
        self.iterable1.append("B")
        self.assertEqual(self.iterable1.data, [2, 5, 4, 3, 1, "B"])

    def test_sort(self):
        IterableStructure.sort(self.iterable1, lambda x, y: x < y)
        self.assertEqual(self.iterable1.data, [1, 2, 3, 4, 5])
        IterableStructure.sort(self.iterable2, lambda x, y: x < y)
        self.assertEqual(self.iterable2.data, ["a", "b", "q", "r", "w"])

    def test_filter(self):
        filtered_iterable1 = IterableStructure.filter(self.iterable1, lambda x: x < 3)
        self.assertEqual(filtered_iterable1, [2, 1])
        filtered_iterable2 = IterableStructure.filter(self.iterable2, lambda x: x == "c")
        self.assertEqual(filtered_iterable2, [])
