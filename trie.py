import unittest


class Trie(object):
    """Allow indexing a set of strings

    Very useful in many algorithm implementations
    """
    
    def __init__(self):
        self.root = TrieNode(None)

    def add_string(self, string, metadata=None):
        """Add a string to the Trie"""

        if len(string) <= 0:
            return
        curr_node = self.root
        for c in string:
            if curr_node.has_child_char(c):
                curr_node = curr_node.get_child_node(c)
            else:
                curr_node = curr_node.add_child(c, metadata)
        curr_node.terminal = True

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
        self.terminal = False
        self.metadata = []

    def get_child_node(self, char):
        return self.children.get(char, None)

    def has_child_char(self, char):
        return char in self.children.keys()

    def add_child(self, char, metadata=None):
        if not self.has_child_char(char):
            self.children[char] = TrieNode(char)
        if metadata:
            self.add_metadata(metadata)
        return self.children[char]

    def add_terminal(self):
        self.terminal = True

    def add_metadata(self, metadata):
        self.metadata.append(metadata)


class SuffixTree(object):
    """Data structure that can be used to index all suffixes of given words"""

    def __init__(self):
        self.trie = Trie()

    def index_string(self, string):
        """Index the string's suffixes"""

        for i in range(len(string)):
            self.trie.add_string(string[i:], string)


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
