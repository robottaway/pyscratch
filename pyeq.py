"""We define a class which overrides the __eq__ and 
__hash__ methods so that we can better define the
business sense of identity.

In this case we have binary tree structure where we 
test if one tree is equal to another.

In our case the subclass, while possibly having the same
values throughout the tree is never equal to parent class
instances.
"""

class Node(object):
    left = None
    right = None
    val = None

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __hash__(self):
        return hash(self.val) ^ hash(self.left) ^ hash(self.right)

    def __eq__(self, other):
        if other is None:
            return False
        if id(self) == id(other):
            return True
        if type(self) != type(other):
            return False
        return self.val == other.val  \
                 and self.left == other.left \
                 and self.right == other.right

    def __ne__(self, other):
        return not self.__eq__(other)


class SuperNode(Node):

    def __init__(self, val, left=None, right=None):
        super(SuperNode, self).__init__(val, left, right)


def main():
    n1 = Node("hey")
    print "Node not equal to None: %s" % (n1 != None)
    n2 = Node("you")
    print "Not equal nodes are not equal: %s" % (n1 != n2)
    n3 = Node("guy", n1, n2)
    n4 = Node ("guy", n1, n2)
    n5 = Node("guy", n2, n1)
    print "Equal nodes are equal: %s" % (n3 == n4)
    print "Not equal nodes are not equal: %s" % (n3 != n5)
    n6 = SuperNode("guy", n1, n2)
    print "Subclass node not equal to like Node: %s" % (n3 != n6)
    n7 = SuperNode("guy", n1, n2)
    print "Equal SuperNodes are equal: %s" % (n6 == n7)
    s = set([n1, n2, n3, n4, n5, n6, n7])
    print "Set should only have 5: %s" % (len(s) == 5)
    print "Node n1 should be in set: %s" % (n1 in s)


if __name__ == "__main__":
    main()

