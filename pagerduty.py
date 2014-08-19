import unittest


class TestSomething(unittest.TestCase):

    def test_please(self):
        retval = something([50,50,50])
        self.assertEquals([(50,50)], retval)

    def test_please_redeux(self):
        retval = something([1,99,99,1])
        self.assertEquals([(1,99), (99,1)], retval)

    def test_please_finalle(self):
        retval = something([1, 2])
        self.assertEquals([], retval)

    def test_please_durp(self):
        retval = something([49, 51])
        self.assertEquals([(49, 51)], retval)

    def test_blah(self):
        retval = something([1])
        self.assertEquals([], retval)

    def test_none_blacker(self):
        retval = something([])
        self.assertEquals([], retval)

    def test_wtfbbq(self):
        import random
        for i in xrange(4):
            numvals = 5000 * (i + 1)
            equalto = 50 * (i + 1)
            vals = [random.randint(0, equalto) for val in xrange(numvals)]
            retval = something(vals, equalto=equalto)
            print "Found %s pairings that equal %s for list of %s values" % (len(retval), equalto, numvals)


def something(l, equalto=100):
    output = []
    while len(l) >= 2:
        val1 = l[0]
        if val1 > equalto:
            l.remove(val1)
            continue
        val2 = None
        for val in l[1:]:
            if val1 + val == equalto:
                val2 = val
                output.append((val1, val2))
                break
        l.remove(val1)
        if val2 is not None:
            l.remove(val2)
    return output    


if __name__ == "__main__":
    unittest.main()
