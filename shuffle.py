import unittest
import random
import logging

logger = logging.getLogger(__name__)


def shuffle(l):
    """Simple implementation of Fischer-Yates/Knuth shuffle"""

    for i in reversed(xrange(len(l))):
        j = random.randint(0, i)
        jval = l[j]
        l[j] = l[i]
        l[i] = jval


class TestShuffle(unittest.TestCase):
    
    def test_shuffle(self):
        l = range(1000)
        shuffle(l)
        self.assertNotEqual(l, range(1000))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    unittest.main()
