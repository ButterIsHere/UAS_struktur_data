# ==============================================================================
# MODULE: BINARY SEARCH TREE & VISUALIZER
# Mengelola hierarki data non-linear dan pencetakan pohon secara grafis.
# ==============================================================================

class TreeNode:
    def __init__(self, key, value):
        self.key = key      # ID Buku atau Judul sebagai Key indeks
        self.value = value  # Metadata Buku
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if not node:
            return TreeNode(key, value)
        if key < node.key:
            node.left = self._insert_recursive(node.left, key, value)
        elif key > node.key:
            node.right = self._insert_recursive(node.right, key, value)
        return node

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def visualize(self):
        """Eksplorasi Tingkat Lanjut: Tree Visualizer di Layar."""
        print("\n--- Visualisasi Struktur Binary Search Tree ---")
        self._print_tree(self.root, "", True)

    def _print_tree(self, node, indent, last):
        if node:
            print(indent, end="")
            if last:
                print("└── ", end="")
                indent += "    "
            else:
                print("├── ", end="")
                indent += "│   "
            print(f"[{node.key}: {node.value.get('title', '')}]")
            self._print_tree(node.left, indent, False)
            self._print_tree(node.right, indent, True)
