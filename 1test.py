class Node:
    def __init__(self, x):
        self.x = x
        self.left = None
        self.right = None

    def insert(self, x):
        if self.x:

            if x > self.x:
                if self.left is None:
                    self.left = Node(x)
                else:
                    self.left.insert(x)
            elif x < self.x:
                if self.right is None:
                    self.right = Node(x)
                else:
                    self.right.insert(x)
        else:
            self.x = x

    def __str__(self):
        return f"<Node: {self.x}>"


root = Node(5)
root.insert(10)
root.insert(2)
root.insert(15)

print(root.left)


