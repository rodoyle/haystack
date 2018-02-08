#!/usr/bin/python
"""Collection Objects

Every object follows the standard collection interface and maps some key to an item
The user should select the appropriate key when passing items or use zip, map, and a key_getter

The key will be interpreted as a byte array and split on char unless configured otherwise.

This Python module is set up to follow Rust-like conventions to allow for benchmarking.
All members follow the "Arena" allocation pattern. Incidentally this is also how Python
collections generally operate.

The items in the collection may be over-ridden to support a pair of vectors of Nodes and Edges for a graph structure

Each collection member has different get behavior. The "art" of this module is comparing different collection types
with different sort of "get" queries. Beyond the basic "get" queries, high-level actors can operate on each collection
to support more sophisticated search strategies. Each member is intended to be constructable from an iterator of (key, value) pairs.
Alternative constructors may be desired with better batch construction performance.

SuffixArrayMagp: A generalized suffix array which returns all items with keys matching a pattern

The RadixTreeMap: return a the item with the key with the longest matching prefix

Other collection methods like set operations, serialization, iteration, etc. may be implemented.


"""

import pytest
import operator
from bisect import insort_left

class SuffixArrayNode(object):

    def __init__(self, item_id, token, key_offset=0):
        # array of structs works best here as we don't want to fully materialize everything 
        self.item_id = item_id
        self.key_offset = key_offset
        self.token = token # The suffix in this case
    
    def cmp(self, other, op):
       return op(self.token,  other.token)
    def __lt__(self, other):
        return cmp(self, other, operator.lt)
    def __le__(self, other):
        return cmp(self, other, operator.le)
    def __eq__(self, other):
        return cmp(self, other, operator.eq)
    def __ge__(self, other):
        return cmp(self, other, operator.ge)
    def __gt__(self, other):
        return cmp(self, other, operator.gt)
    def startswith(self, prefix):
        return self.token.startswith(prefix)
        
class SuffixArrayMap(object):
    def __init__(self):
        self.items = list()
        self.keys = list()
        self.index = list()

    def insert(self, key, item):
        # key should be split or otherwise iterable
        item_id = len(self.items)  # id of new item to be inserted
        self.items.append(item)
        self.keys.append(key)
        for i in range(len(key)):
            suffix = key[i:]  + "$" + str(item_id)  # our "token"
            node = SuffixArrayNode(item_id, suffix, i)
            insort_left(self.index, node)

    def get(self, prefix):
        # use of startswith should be deprecated to allow fuzzy search
        # binary search time!
        low = 0
        high = len(self.index) - 1
        if high <= low:
            return None
        while (low < high):
            mid = (high + low)/2
            node = self.index[mid]
            if node.startswith(prefix):
                break
            elif node.token < prefix:  # start is too high
                low = mid + 1
            elif node.token > prefix: # start is too low
                high = mid
        mid = (high+low) /2  # update mid
        if self.items[mid].startswith(prefix):
            h = mid - 1
            while(low < h):
                m = (h+low)/2
                node = self.items[m]
                if prefix > node:
                    low = m + 1
                else:
                    h = m
            if not self.items[low].startswith(prefix):
                low = mid

            l = mid + 1
            while (l<high):
                m = (l + high + 1) /2
                if self.items[m].startswith(prefix):
                    l = m
                else:
                    high = m - 1
            if not self.items[high].startswith(prefix):
                high = mid
            return self.items[low:high + 1]
        else:
            return None

class RadixTreeNode(object):

    def __init__(self, token, item_id=None, key_offset=None):
        """
        token (string): The subset of the key used to id this node and do comparisons
        item_id Option<usize>: Id of the item IF this is a terminal node
        key_offset Option<usize>: The token's position in the key
        """
        self.token = token
        self.item_id = None
        self.children = dict()

class RadixTreeMap(object):

    def __init__(self):
        self.items = list()
        self.keys = list()
        self.index = RadixTreeNode('')

    def insert(self, key, item):
        current = self.index
        # This split is optional could just use bytes
        for key_offset, token in key.split('/').enumerate():
            if token in current.children:
                # it exists, no need to linearly scan with hashtables
                node = current.children[token]
            else:
                node = RadixTreeNode(token)
                current.children[token] = node
        # Either way we've inserted the nodes into the tree
        # Now insert a terminal node with our value.
        # Check if the item is already set.
        # Python rules are this should replace the item
        if node.item_id:
            item_id = node.item_id
            self.items[item_id] = item
            self.keys[item_id] = key
        elif node.item_id is None:
            item_id = len(self.items)
            self.items.append(item)
            self.keys.append(key)
            node.item_id = item_id
            node.key_offset = key_offset

    def get(self, prefix):
        """return item with the longest matching prefix"""
        node = self.index
        best_match = None
        for token in prefix.split("/"):
            if token in node.children:
                best_match = node
                node = node.children[token]
            else:
                break
        # current value of best_match is the longest matching node
        if best_match is None:
            return None # or a default or raise KeyError
        return self.items[best_match.item_id]



if __name__ == '__main__':
    with open('trie_input03.txt', 'r') as infh:
        n = int(infh.next().strip())
        for a0 in range(n):
            op, contact = infh.next().strip().split(' ')
            if op == 'add':
                #add(tree, contact)
                insort_left(SA, contact)
            if op == 'find':
                result = sa_find(SA, contact)
                print(result)
