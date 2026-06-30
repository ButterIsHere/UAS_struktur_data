# ==============================================================================
# MODULE: QUEUE STRUCTURE (FIFO)
# Mengimplementasikan antrean pemrosesan peminjaman & pengembalian buku.
# ==============================================================================

from src.structures.linked_lists import Node

class Queue:
    """Struktur data Antrean berbasis Linked List."""
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if not self.rear:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = self.front.next
        if not self.front:
            self.rear = None
        return temp.data

    def is_empty(self):
        return self.front is None

    def to_list(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result
