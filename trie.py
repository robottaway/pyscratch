import unittest


class Trie(object):
    """Allow indexing a set of strings

    Very useful in many algorithm implementations
    """
    
    def __init__(self):
        self.root = TrieNode(None)

    def add_string(self, string, metadata=None, idx=0):
        """Add a string to the Trie"""

        if len(string) <= 0:
            return
        curr_node = self.root
        for c in string:
            if curr_node.has_child_char(c):
                curr_node = curr_node.get_child_node(c)
            else:
                curr_node = curr_node.add_child(c)
            if metadata is not None:
                curr_node.add_metadata(metadata)

    def contains_path(self, string):
        """See if sequence of characters given by value has a path in the Trie"""

        if len(string) <= 0:
            return
        curr_node = self.root
        for c in string:
            if curr_node.has_child_char(c):
                curr_node = curr_node.get_child_node(c)
            else:
                return False, None
        return True, curr_node.metadata



class TrieNode(object):
    """Contains a character, can be terminal if a string terminates at this node"""
    
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.metadata = set()

    def __str__(self):
        return "<(%s) char: %s>" % (self.__class__, self.char)

    def get_child_node(self, char):
        return self.children.get(char, None)

    def has_child_char(self, char):
        return char in self.children.keys()

    def add_child(self, char):
        if not self.has_child_char(char):
            self.children[char] = TrieNode(char)
        return self.children[char]

    def depth_first(self, acc=None):
        if acc:
            accp = acc.compute(self.char)
        else:
            accp = None

        yield self, accp
        for child in self.children.values():
            for child, cacc in child.depth_first(accp):
                yield child, cacc

    def add_metadata(self, metadata):
        self.metadata.add(metadata)


class Accumulator(object):

    def __init__(self, seen=[]):
        self.seen = seen

    def __str__(self):
        return "<%s, seen: %s>" % (self.__class__, self.seen)

    def compute(self, char):
        if char:
            return Accumulator(self.seen+[char])
        else:
            return self


class SuffixTree(object):
    """Data structure that can be used to index all suffixes of given words"""

    def __init__(self):
        self.trie = Trie()

    def index_string(self, string):
        """Index the string's suffixes"""

        for i in range(len(string)):
            self.trie.add_string(string[i:], string, i)


import logging
logging.basicConfig(level=logging.INFO)
test_logger = logging.getLogger('test')
test_logger.setLevel(logging.INFO)


class TestTrie(unittest.TestCase):
    """Run some tests to be sure the Trie is working"""

    def test_trie(self):
        trie = Trie()
        trie.add_string("blahblahblah")
        trie.add_string("blahblibbityblah", "some metadata")
        self.assertTrue(trie.contains_path('blahbla')[0])
        self.assertTrue(trie.contains_path('blahbli')[0])
        self.assertFalse(trie.contains_path('lahb')[0])


class TestSuffixTree(unittest.TestCase):
    """Run some tests to be sure the SuffixTree is working"""

    def test_suffix_tree(self):
        suffix_trie = SuffixTree()
        suffix_trie.index_string("blahblahblah")
        suffix_trie.index_string("blahblibbityblah")
        self.assertTrue(suffix_trie.trie.contains_path('blahbla')[0])
        self.assertTrue(suffix_trie.trie.contains_path('blahbli')[0])
        self.assertTrue(suffix_trie.trie.contains_path('lahbla')[0])
        self.assertTrue(suffix_trie.trie.contains_path('lahbli')[0])


class TestLargeFile(unittest.TestCase):

    def test_substrings(self):
        """Using a large set of dictionary words, create Suffix
        Tree and look for works with a given substring.
        """
        substrs = ['ith', 'orn', 'iev', 'ass', 'net', 'ary', 'car', 'le']
        st = SuffixTree()
        with open('wordlist.csv', 'r') as fd:
            for word in fd:
                    st.index_string(word.split(',')[0].strip().lower()) 

        for substr in substrs:
            test_logger.info("looking for words with '%s' in them", substr)
            found, metadata = st.trie.contains_path(substr)
            if found:
                for item in metadata:
                    test_logger.info(">>> %s", item)

    def test_palindromes(self):
        """Given a word find the longest palindrome within"""

        test_strings = ["baroness", "laval", "analisa", "zabba"]

        for s in test_strings:
            suffixes = []
            st = SuffixTree()
            sr = s[::-1]
            st.index_string(s)
            st.index_string(sr)
            longest = None
            for val, acc in st.trie.root.depth_first(Accumulator()):
                seen = ''.join(acc.seen)
                if len(seen) < 3:
                    continue
                if s in val.metadata and sr in val.metadata:
                    if not longest:
                        longest = seen
                    if len(longest) < len(seen):
                        longest = seen
            if longest:
                print "Longest for %s is %s" % (s, longest)
            else:
                print "No palindrome for %s" % (s)
