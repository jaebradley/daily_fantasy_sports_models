from unittest import TestCase

from daily_fantasy_sports_models.core.sets import is_disjoint


class TestSets(TestCase):
    def test_disjoint_sets(self):
        for (first, second) in [
            (
                    set(), set()
            ),
            (
                    {1}, {2},
            ),
            (
                    {1, 2}, {4, 3}
            )
        ]:
            self.assertTrue(is_disjoint(first=first, second=second))
            self.assertTrue(is_disjoint(first=second, second=first))

    def test_non_disjoint_sets(self):
        for (first, second) in [
            (
                    {1}, {1},
            ),
            (
                    {1, 2}, {1, 2}
            ),
            (
                    {1, 2}, {1, 3}
            )
        ]:
            self.assertFalse(is_disjoint(first=first, second=second))
            self.assertFalse(is_disjoint(first=second, second=first))
