# ==============================================================================
# MODULE: LINKED LIST STRUCTURES
# Mengimplementasikan SLL, DLL, CSLL, dan CDLL secara mandiri dari nol.
# ==============================================================================

class Node:
    """Node dasar untuk Single Linked List dan Circular Singly Linked List."""
    def __init__(self, data=None):
        self.data = data
        self.next = None

class BiNode:
    """Node dua arah untuk Double Linked List dan Circular Doubly Linked List."""
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

class SingleLinkedList:
    """Digunakan untuk Manajemen Inventaris Buku."""
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, book_id):
        current = self.head
        if current and current.data['id'] == book_id:
            self.head = current.next
            return True
        prev = None
        while current and current.data['id'] != book_id:
            prev = current
            current = current.next
        if not current:
            return False
        prev.next = current.next
        return True

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class DoubleLinkedList:
    """Digunakan untuk Riwayat Aktivitas (Navigasi Dua Arah)."""
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = BiNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class CircularSinglyLinkedList:
    """Digunakan untuk Fitur Buku Favorit (Siklus Data Tunggal)."""
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return
        current = self.head
        while current.next != self.head:
            current = current.next
        current.next = new_node
        new_node.next = self.head

    def to_list(self):
        if not self.head: return []
        result = []
        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head: break
        return result

class CircularDoublyLinkedList:
    """Digunakan untuk Sistem Rekomendasi (Siklus Ganda Efisiensi Tinggi)."""
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = BiNode(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            new_node.prev = self.head
            return
        tail = self.head.prev
        tail.next = new_node
        new_node.prev = tail
        new_node.next = self.head
        self.head.prev = new_node

    def to_list(self):
        if not self.head: return []
        result = []
        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head: break
        return result
