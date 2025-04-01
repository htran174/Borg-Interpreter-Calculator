TABLESIZE = 10

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class Scope:
    def __init__(self):
        self.table = [None for _ in range(TABLESIZE)]

    def insert(self, variable_name, value):
        index = self.hash_function(variable_name)
        new_node = Node(variable_name, value)
        new_node.next = self.table[index]
        self.table[index] = new_node

    def hash_function(self, variable_name):
        return sum(ord(variable_name[i]) * (i + 1) for i in range(len(variable_name))) % TABLESIZE

    def find(self, variable_name):
        index = self.hash_function(variable_name)
        current = self.table[index]
        while current:
            if current.key == variable_name:
                return current
            current = current.next
        return None

class HashTable:
    def __init__(self):
        self.scopes = [Scope() for _ in range(TABLESIZE)]
        self.current_scope_index = 0

    def insert(self, variable_name, value):
        self.scopes[self.current_scope_index].insert(variable_name, value)

    def search_value(self, variable_name):
        for i in range(self.current_scope_index, -1, -1):
            node = self.scopes[i].find(variable_name)
            if node:
                return node.value
        return -1

    def search_node(self, variable_name):
        for i in range(self.current_scope_index, -1, -1):
            node = self.scopes[i].find(variable_name)
            if node:
                return node
        return None

    def replace(self, variable_name, value):
        node = self.search_node(variable_name)
        if node:
            node.value = value

    def increment(self, variable_name):
        node = self.search_node(variable_name)
        if node:
            node.value += 1

    def decrement(self, variable_name):
        node = self.search_node(variable_name)
        if node:
            node.value -= 1

    def start_scope(self):
        self.current_scope_index += 1

    def finish_scope(self):
        if self.current_scope_index > 0:
            self.current_scope_index -= 1
