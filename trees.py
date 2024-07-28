# Satchel Hamilton
# Project 3 - Griefer List
# Command line args supported: "avl"

from math import floor, log, ceil
from sys import argv, exit, stdin
import time 

class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.banCount = 1
        self.banTime = self.key[2]

class AVLTree(object):
    def insert(self, root, key):
        if not root:
            return Node(key)
            
        if key[0] == root.key[0]:
            if root.banTime < key[2]:
                root.banTime = key[2]
            root.banCount += 1
            return root
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)


        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if key < root.left.key:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if key > root.right.key:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def search(self, root, key):
        nd = root
        while nd != None:
            if nd.key[0] > key:
                nd = nd.left
            elif nd.key[0] < key:
                nd = nd.right
            else:
                return nd;
        return None

    def getGriefers(self):
        for player in stdin:
            player = player.strip()
            if self.search(root, player) != None:
                griefer = self.search(root, player)
                print(str(griefer.key[0]) + " was banned from " + str(griefer.banCount) + \
                " servers. most recently on: " + str(griefer.banTime))
            else:
                print(str(player) + " is not currently banned from any servers.")

class ScapeGoatTree(object):
    def __init__(self):
        self.alpha = 0.8
        self.size = 0
        self.max_size = 0
        self.root = None

    def insert(self, key):
        a = self.root
        b = None
        c = Node(key)
        depth = 0
        ancestors = []

        while a != None:
            ancestors.insert(0,a)
            b = a
            if a.banTime < a.key[2]:
                a.banTime = a.key[2]
            if a.key[0] == c.key[0]:
                if a.banTime < c.key[2]:
                    a.banTime = c.key[2]
                a.banCount += 1
                return a
            if c.key < a.key:
                a = a.left
            else:
                a = a.right
            depth += 1

        if b == None:
            self.root = c
        elif c.key < b.key:
            b.left = c
        else:
            b.right = c

        self.size += 1
        self.max_size = max(self.size, self.max_size)
        
        if self.getDepth(depth):
            sg = None
            ancestors.insert(0,c)
            sgSize = [0]*len(ancestors)
            temp = 0

            for i in range(1, len(ancestors)):
                sgSize[i] = sgSize[i-1] + self.getCount(self.isSibling \
                (ancestors[i-1], ancestors[i]))+1
                if not self.isBalanced(ancestors[i], sgSize[i]+1):
                    sg = ancestors[i]
                    temp = i
            
            tmp = self.rebuildTree(sg, sgSize[temp]+1)
            sg.left = tmp.left
            sg.right = tmp.right
            sg.key = tmp.key
            sg.banCount = tmp.banCount
            sg.banTime = tmp.banTime

    def isBalanced(self, n, sizeOfN):
        x = self.getCount(n.left) <= (self.alpha * sizeOfN)
        y = self.getCount(n.right) <= (self.alpha * sizeOfN)
        return x and y
        
    def getCount(self, x):
        if x == None:
            return 0
        return 1 + self.getCount(x.left) + self.getCount(x.right)

    def isSibling(self, node, parent):
        if parent.left != None and parent.left.key == node.key:
            return parent.right
        return parent.left

    def getDepth(self, depth):
        return depth > floor(log(self.size, 1 / self.alpha))

    def rebuildTree(self, root, length):
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        def listToTree(nodes, start, end):
            if start > end:
                return None
            mid = int(ceil(start + (end - start) / 2))
            n = Node(nodes[mid].key)
            n.left = listToTree(nodes, start, mid-1)
            n.right = listToTree(nodes, mid+1, end)
            n.banTime = nodes[mid].banTime
            n.banCount = nodes[mid].banCount
            return n

        nodes = []
        flatten(root, nodes)
        return listToTree(nodes, 0, length-1)

    def search(self, key):
        nd = self.root
        while nd != None:
            if nd.key[0] > key:
                nd = nd.left
            elif nd.key[0] < key:
                nd = nd.right
            else:
                return nd;
        return None

    def getGriefers(self):
        for player in stdin:
            player = player.strip()
            if self.search(player) != None:
                griefer = self.search(player)
                print(str(griefer.key[0]) + " was banned from " + str(griefer.banCount) + \
                " servers. most recently on: " + str(griefer.banTime))
            else:
                print(str(player) + " is not currently banned from any servers.")

if __name__ == '__main__':
    start_time = time.time_ns()
    if len(argv) > 2:
        treeType = argv[1]
        filename = argv[2]
    else:
        print("Usage ./program <treeType> <inputFile>")
        exit()

    with open(filename, 'r') as f:
        tmp = f.readlines()
        griefer_data = [line.strip().split(" ", 2) for line in tmp]

    if treeType == "scapegoat":
        sg = ScapeGoatTree()
        list = [sg.insert(list) for list in griefer_data]
        sg.getGriefers()
        time_taken_in_microseconds = ( time.time_ns()- start_time ) / 1000.0 
        print("".join(["total time in microseconds: ", str(time_taken_in_microseconds)]))
        
    if treeType == "avl":
        avl, root = AVLTree(), None
        for list in griefer_data:
            root = avl.insert(root, list)
        avl.getGriefers()
        time_taken_in_microseconds = ( time.time_ns()- start_time ) / 1000.0
        print("".join(["total time in microseconds: ", str(time_taken_in_microseconds)]))
