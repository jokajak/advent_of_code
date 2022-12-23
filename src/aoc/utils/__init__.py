"""Utilities for aoc"""

# From https://realpython.com/linked-lists-python/


class MyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    def __str__(self):
        return str(self.data)

    def __add__(self, anotherObj):
        # TODO: Handle None
        if type(anotherObj) == int:
            node = self
            if anotherObj > 0:
                for i in range(anotherObj):
                    node = node.next
                return node
            elif anotherObj < 0:
                for i in range(abs(anotherObj)):
                    node = node.previous
                return node
            elif anotherObj == 0:
                return self
            else:
                raise ValueError

    def __sub__(self, anotherObj):
        # TODO: Handle None
        if type(anotherObj) == int:
            node = self
            if anotherObj > 0:
                for i in range(anotherObj):
                    node = node.next
                return node
            elif anotherObj < 0:
                for i in range(abs(anotherObj) + 1):
                    node = node.previous
                return node
            elif anotherObj == 0:
                return self
            else:
                raise ValueError


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        ret = []
        for node in self.traverse():
            ret.append(str(node))
        return f"[{', '.join(ret)}]"

    def traverse(self, starting_point=None):
        if starting_point is None:
            starting_point = self.head
        node = starting_point
        while node is not None and (node.next != starting_point):
            yield node
            node = node.next
        yield node

    def print_list(self, starting_point=None):
        nodes = []
        for node in self.traverse(starting_point):
            nodes.append(str(node))
        print(" -> ".join(nodes))

    def __iter__(self):
        node = starting_point = self.head
        while node is not None and (node.next != starting_point):
            yield node
            node = node.next
        yield node
