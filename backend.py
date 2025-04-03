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
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

    class Scope:
        def __init__(self):
            self.size = 100
            self.table = [None] * self.size

        def _hash(self, key):
            return hash(key) % self.size

        def insert(self, key, value, update_existing=False):
            index = self._hash(key)
            current = self.table[index]
            while current:
                if current.key == key:
                    if update_existing:
                        current.value = value
                    return True  # key found and updated/skipped
                current = current.next
            if not update_existing:
                new_node = HashTable.Node(key, value)
                new_node.next = self.table[index]
                self.table[index] = new_node
                return True
            return False  # key not found and update was requested

        def search(self, key):
            index = self._hash(key)
            current = self.table[index]
            while current:
                if current.key == key:
                    return current
                current = current.next
            return None

    def __init__(self):
        self.scopes = [self.Scope()]
        self.current_scope_index = 0

    def insert(self, key, value, update_existing=False):
        # Try to update existing key in any visible scope
        for i in range(self.current_scope_index, -1, -1):
            if update_existing:
                updated = self.scopes[i].insert(key, value, update_existing=True)
                if updated:
                    return True
        # If not found and not updating, insert into current scope
        if not update_existing:
            return self.scopes[self.current_scope_index].insert(key, value)
        return False  # tried to update non-existent key

    def search_value(self, key):
        for i in range(self.current_scope_index, -1, -1):
            node = self.scopes[i].search(key)
            if node:
                return node.value
        return -1

    def key_exists(self, key):
        for i in range(self.current_scope_index, -1, -1):
            if self.scopes[i].search(key):
                return True
        return False

    def start_scope(self):
        self.scopes.append(self.Scope())
        self.current_scope_index += 1

    def finish_scope(self):
        if self.current_scope_index > 0:
            self.scopes.pop()
            self.current_scope_index -= 1
