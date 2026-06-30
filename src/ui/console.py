# ==============================================================================
# MODULE: CONSOLE INTERFACE ENGINE
# Alur kemudi utama aplikasi berbasis CLI interaktif.
# ==============================================================================

import json
import os
from src.structures.linked_lists import SingleLinkedList, DoubleLinkedList, CircularSinglyLinkedList, CircularDoublyLinkedList
from src.structures.queue import Queue
from src.structures.bst import BinarySearchTree
from src.algorithms.searching import linear_search, binary_search
from src.algorithms.sorting import quick_sort, bubble_sort

DATA_PATH = "data/library_data.json"

class LibrarySystem:
    def __init__(self):
        # Inisialisasi 6 Struktur Data Wajib
        self.inventaris = SingleLinkedList()
        self.antrean_peminjaman = Queue()
        self.riwayat_aktivitas = DoubleLinkedList()
        self.buku_favorit = CircularSinglyLinkedList()
        self.sistem_rekomendasi = CircularDoublyLinkedList()
        self.bst_index = BinarySearchTree()
        
        self.load_state()

    def load_state(self):
        """Eksplorasi Tingkat Lanjut: Persistence JSON Loader."""
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, 'r') as f:
                    data = json.load(f)
                    for b in data.get('inventaris', []):
                        self.inventaris.append(b)
                        self.bst_index.insert(b['id'], b)
                    for q in data.get('antrean', []):
                        self.antrean_peminjaman.enqueue(q)
                    for r in data.get('riwayat', []):
                        self.riwayat_aktivitas.append(r)
            except Exception:
                pass

    def save_state(self):
        """Eksplorasi Tingkat Lanjut: Persistence JSON Saver."""
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        state = {
            "inventaris": self.inventaris.to_list(),
            "antrean": self.antrean_peminjaman.to_list(),
            "riwayat": self.riwayat_aktivitas.to_list()
        }
        with open(DATA_PATH, 'w') as f:
            json.dump(state, f, indent=4)

    def run(self):
        while True:
            print("\n=== SISTEM PERPUSTAKAAN DIGITAL ===")
            print("[1] Kelola Buku (Tambah/Lihat)")
            print("[2] Peminjaman (Enqueue Antrean)")
            print("[3] Pengembalian (Dequeue Antrean)")
            print("[4] Searching Engine (Linear & Binary)")
            print("[5] Sorting Engine (Bubble & Quick)")
            print("[6] Operasi Tree (Visualisasi BST)")
            print("[7] Laporan Sistem & Log")
            print("[0] Keluar")
            
            pilihan = input("Masukkan pilihan Anda: ").strip()
            
            if pilihan == "1":
                b_id = int(input("Masukkan ID Buku (Angka): "))
                title = input("Masukkan Judul Buku: ")
                book = {"id": b_id, "title": title}
                self.inventaris.append(book)
                self.bst_index.insert(b_id, book)
                self.riwayat_aktivitas.append(f"Menambahkan buku: {title}")
                print("✓ Buku berhasil ditambahkan ke Inventaris (SLL).")
                self.save_state()
                
            elif pilihan == "2":
                nama = input("Masukkan Nama Peminjam: ")
                b_id = int(input("Masukkan ID Buku yang dipinjam: "))
                self.antrean_peminjaman.enqueue({"peminjam": nama, "book_id": b_id})
                self.riwayat_aktivitas.append(f"{nama} mengantre pinjam ID {b_id}")
                print("✓ Transaksi dimasukkan ke Antrean Pemrosesan (Queue FIFO).")
                self.save_state()
                
            elif pilihan == "3":
                proses = self.antrean_peminjaman.dequeue()
                if proses:
                    print(f"✓ Memproses peminjaman {proses['peminjam']} untuk Buku ID {proses['book_id']}.")
                    self.riwayat_aktivitas.append(f"Selesai memproses peminjaman {proses['peminjam']}")
                    self.save_state()
                else:
                    print("! Antrean kosong.")
                    
            elif pilihan == "4":
                print("[1] Linear Search (Teks Judul)\n[2] Binary Search (ID - Membutuhkan Sorting)")
                sub = input("Pilih metode: ")
                current_list = self.inventaris.to_list()
                if sub == "1":
                    q = input("Masukkan kata kunci judul: ")
                    res = linear_search(current_list, q, 'title')
                    print("Hasil:", res)
                elif sub == "2":
                    target = int(input("Masukkan ID Buku: "))
                    sorted_list = quick_sort(current_list, 'id')
                    res = binary_search(sorted_list, target, 'id')
                    print("Hasil:", res)
                    
            elif pilihan == "5":
                current_list = self.inventaris.to_list()
                print("Mengurutkan data inventaris dengan Quick Sort O(n log n)...")
                sorted_res = quick_sort(current_list, 'id')
                print("Hasil Pengurutan ID:", sorted_res)
                
            elif pilihan == "6":
                self.bst_index.visualize()
                
            elif pilihan == "7":
                print("\n=== LAPORAN RIWAYAT AKTIVITAS (DLL) ===")
                for log in self.riwayat_aktivitas.to_list():
                    print(f"[LOG] {log}")
                    
            elif pilihan == "0":
                self.save_state()
                print("Keluar dari program. Terima kasih.")
                break
            else:
                print("! Opsi tidak valid.")
