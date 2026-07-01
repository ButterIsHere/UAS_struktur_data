# =============================================================================
# MODULE: CONSOLE INTERFACE ENGINE (WITH CLEAR SCREEN & FULL FEATURE EQUIVALENT)
# =============================================================================

import json
import os
from src.structures.linked_lists import SingleLinkedList, DoubleLinkedList
from src.structures.queue import Queue
from src.structures.bst import BinarySearchTree
from src.algorithms.searching import linear_search, binary_search
from src.algorithms.sorting import quick_sort

DATA_PATH = "data/library_data.json"

class LibrarySystem:
    def __init__(self):
        # Inisialisasi Struktur Data Core Backend
        self.inventaris = SingleLinkedList()
        self.antrean_peminjaman = Queue()
        self.riwayat_aktivitas = DoubleLinkedList()
        self.bst_index = BinarySearchTree()
        self.load_state()

    def clear_screen(self):
        """Membersihkan layar terminal (Mendukung Linux/Arch & Windows)."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def load_state(self):
        """Persistence JSON Loader."""
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
        """Persistence JSON Saver."""
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        state = {
            "inventaris": self.inventaris.to_list(),
            "antrean": self.antrean_peminjaman.to_list(),
            "riwayat": self.riwayat_aktivitas.to_list()
        }
        with open(DATA_PATH, 'w') as f:
            json.dump(state, f, indent=4)

    def render_console_tree(self):
        """
        [Ekuivalen Fitur GUI Modul 6]
        Merender visualisasi pohon hirarki 3-Level (Library -> Genre -> Buku)
        secara terstruktur langsung di terminal CLI.
        """
        print("\n" + "="*60)
        print("  [6] LIBRARY HIERARCHY INDEX VISUALIZER (CLI RENDER)  ")
        print("="*60)
        
        master_books = self.inventaris.to_list()
        if not master_books:
            print("    └── [LIBRARY KOSONG]")
            print("="*60)
            return

        # Pengelompokkan Level 1 (Genre) dan Level 2 (Buku)
        genre_map = {}
        no_genre_books = []
        for book in master_books:
            genres = book.get("genres", [])
            if not genres:
                no_genre_books.append(book)
            else:
                for g in genres:
                    if g not in genre_map:
                        genre_map[g] = []
                    genre_map[g].append(book)
        if no_genre_books:
            genre_map["Uncategorized"] = no_genre_books

        # Cetak Root Level 0
        print("└── 🏫 LIBRARY")
        
        genres_list = list(genre_map.keys())
        for i, genre in enumerate(genres_list):
            is_last_genre = (i == len(genres_list) - 1)
            prefix_genre = "    └── " if is_last_genre else "    ├── "
            indent_book  = "        " if is_last_genre else "    │   "
            
            # Cetak Level 1 (Genre)
            print(f"{prefix_genre}📁 {genre.upper()}")
            
            # Cetak Level 2 (Buku di dalam Genre tersebut)
            books = genre_map[genre]
            for j, book in enumerate(books):
                is_last_book = (j == len(books) - 1)
                prefix_book = "└── " if is_last_book else "├── "
                print(f"{indent_book}{prefix_book}📖 [{book['id']}] {book['title']}")
        print("="*60)

    def wait_user(self):
        """Menahan layar sebelum dibersihkan kembali oleh clear screen."""
        input("\nTekan [ENTER] untuk kembali ke Menu Utama...")

    def run(self):
        while True:
            self.clear_screen()  # <--- Bersihkan layar setiap kembali ke menu utama
            print("="*55)
            print("       DIGITAL LIBRARY SYSTEM (CONSOLE ENGINE)      ")
            print("="*55)
            print("[1]  Tambah Buku Baru (Multi-Genre Checkbox Match)")
            print("[2]  Hapus Buku Berdasarkan ID")
            print("[3]  Enqueue Antrean Peminjam (Queue FIFO)")
            print("[4]  Dequeue / Proses Antrean Terdepan")
            print("[5]  Batalkan Antrean Spesifik via Kode Transaksi")
            print("[6]  Algoritma Pemrosesan Searching (Linear / Binary)")
            print("[7]  Algoritma Pemrosesan Sorting (⚡ Quick Sort ID)")
            print("[8]  Render Struktur Hirarki Indeks Tree (3-Level)")
            print("[9]  Tampilkan Laporan Audit Trail Log (DLL)")
            print("[10] Tampilkan Semua Data Inventaris (SLL View)")
            print("[0]  Sinkronisasi Data (JSON) & Keluar Sistem")
            print("-"*55)
            
            pilihan = input("Pilih Opsi Menu (0-10): ").strip()
            
            if pilihan == "1":
                self.clear_screen()
                print("--- TAMBAH BUKU BARU ---")
                id_in = input("Masukkan ID Buku (Kosongkan untuk Auto-Increment): ").strip()
                title = input("Masukkan Judul Buku: ").strip()
                if not title:
                    print("! Judul tidak boleh kosong.")
                    self.wait_user()
                    continue
                
                print("Pilihan Genre Tersedia: Sci-Fi, Comic, Novel, Textbook, History")
                genres_in = input("Masukkan genre (pisahkan dengan koma jika lebih dari satu): ")
                genres = [g.strip() for g in genres_in.split(",") if g.strip()]
                
                b_id = int(id_in) if id_in else (max([b["id"] for b in self.inventaris.to_list()] + [0]) + 1)
                
                if any(book["id"] == b_id for book in self.inventaris.to_list()):
                    print(f"! Error: Buku dengan ID {b_id} sudah terdaftar.")
                    self.wait_user()
                    continue
                    
                book = {"id": b_id, "title": title, "genres": genres}
                self.inventaris.append(book)
                self.bst_index.insert(b_id, book)
                self.riwayat_aktivitas.append(f"Tambah buku: {title} (Genres: {genres}) [ID: {b_id}]")
                print(f"✔ Buku '{title}' berhasil disimpan di RAM & Index.")
                self.save_state()
                self.wait_user()

            elif pilihan == "2":
                self.clear_screen()
                print("--- HAPUS BUKU ---")
                try:
                    b_id = int(input("Masukkan ID Buku yang akan dihapus: ").strip())
                    if self.inventaris.delete(b_id):
                        self.riwayat_aktivitas.append(f"Hapus buku ID: {b_id}")
                        print(f"✔ Buku dengan ID {b_id} sukses dihapus.")
                        self.save_state()
                    else:
                        print("! Buku tidak ditemukan.")
                except ValueError:
                    print("! Input tidak valid. Gunakan angka integer murni.")
                self.wait_user()

            elif pilihan == "3":
                self.clear_screen()
                print("--- ENQUEUE ANTREAN PEMINJAM ---")
                nama = input("Masukkan Nama Peminjam: ").strip()
                try:
                    b_id = int(input("Masukkan Target ID Buku: ").strip())
                    if not nama: raise ValueError()
                    
                    tx_id = max([q["tx_id"] for q in self.antrean_peminjaman.to_list() if "tx_id" in q] + [1000]) + 1
                    self.antrean_peminjaman.enqueue({"tx_id": tx_id, "peminjam": nama, "book_id": b_id})
                    self.riwayat_aktivitas.append(f"Enqueue Antrean #{tx_id}: {nama} -> Buku ID {b_id}")
                    print(f"✔ Berhasil masuk manifest antrean. Kode Transaksi Anda: #{tx_id}")
                    self.save_state()
                except ValueError:
                    print("! Input gagal. Lengkapi data peminjaman dengan benar.")
                self.wait_user()

            elif pilihan == "4":
                self.clear_screen()
                print("--- PROCESS FIFO ANTREAN (DEQUEUE) ---")
                proses = self.antrean_peminjaman.dequeue()
                if proses:
                    self.riwayat_aktivitas.append(f"FIFO memproses transaksi #{proses.get('tx_id')}")
                    print(f"✔ Sukses Memproses Antrean #{proses.get('tx_id')} atas nama {proses['peminjam']}.")
                    self.save_state()
                else:
                    print("! Daftar sirkulasi antrean sedang kosong.")
                self.wait_user()

            elif pilihan == "5":
                self.clear_screen()
                print("--- BATALKAN ANTREAN SPESIFIK VIA ID ---")
                try:
                    target = int(input("Masukkan ID Kode Transaksi yang ingin dibatalkan: ").strip())
                    old_items = self.antrean_peminjaman.to_list()
                    self.antrean_peminjaman = Queue()
                    found = False
                    
                    for item in old_items:
                        if item.get("tx_id") == target:
                            found = True
                            self.riwayat_aktivitas.append(f"Membatalkan Transaksi #{target}")
                            continue
                        self.antrean_peminjaman.enqueue(item)
                        
                    if found:
                        print(f"✔ Transaksi Antrean #{target} berhasil dibatalkan & dihapus.")
                        self.save_state()
                    else:
                        print("! ID Transaksi tidak ditemukan di antrean aktif.")
                        for item in old_items: self.antrean_peminjaman.enqueue(item)
                except ValueError:
                    print("! Masukkan parameter angka integer murni.")
                self.wait_user()

            elif pilihan == "6":
                self.clear_screen()
                print("--- ALGORITMA SEARCHING ENGINE ---")
                print("[1] Linear Search (By Teks Judul)")
                print("[2] Binary Search (By ID Angka - Auto Quick Sort)")
                sub = input("Pilih metode (1-2): ").strip()
                current_list = self.inventaris.to_list()
                
                if sub == "1":
                    q = input("Masukkan Kata Kunci Judul: ").strip()
                    res = linear_search(current_list, q, 'title')
                    print(f"\nHasil Pencarian Linear ({len(res)} ditemukan):")
                    for b in res:
                        print(f"  -> ID: {b['id']} | Judul: {b['title']} | Genres: {b.get('genres', [])}")
                elif sub == "2":
                    try:
                        target = int(input("Masukkan target ID Buku: ").strip())
                        sorted_list = quick_sort(current_list, 'id')
                        res = binary_search(sorted_list, target, 'id')
                        print("\nHasil Pencarian Binary:")
                        if res:
                            print(f"  ✔ Ditemukan -> ID: {res['id']} | Judul: {res['title']} | Genres: {res.get('genres', [])}")
                        else:
                            print("  ! Buku tidak ditemukan.")
                    except ValueError:
                        print("! Parameter input ID wajib berupa angka.")
                self.wait_user()

            elif pilihan == "7":
                self.clear_screen()
                print("--- ALGORITMA SORTING ENGINE (QUICK SORT) ---")
                current_list = self.inventaris.to_list()
                print("Mengurutkan display display buffer tabel visual dengan Quick Sort O(n log n)...")
                sorted_res = quick_sort(current_list, 'id')
                print("\n[DISPLAY BUFFER HASH COMPILATION]:")
                for b in sorted_res:
                    print(f"  ID: {b['id']} | Judul: {b['title']} | Genres: {b.get('genres', [])}")
                self.riwayat_aktivitas.append("Mengurutkan display visual tabel via Quick Sort.")
                self.wait_user()

            elif pilihan == "8":
                self.clear_screen()
                self.render_console_tree()
                self.wait_user()

            elif pilihan == "9":
                self.clear_screen()
                print("=== LAPORAN RIWAYAT AKTIVITAS AUDIT TRAIL (DLL) ===")
                logs = self.riwayat_aktivitas.to_list()
                if not logs:
                    print("  [Belum ada log aktivitas tercatat]")
                for log in logs:
                    print(f"[LOG] {log}")
                self.wait_user()

            elif pilihan == "10":
                self.clear_screen()
                print("--- DATA INVENTARIS SEKARANG (SLL ORIGINAL RAM STATE) ---")
                books = self.inventaris.to_list()
                if not books:
                    print("  [Inventaris kosong]")
                for b in books:
                    print(f"ID: {b['id']} | Judul: {b['title']} | Genres: {b.get('genres', [])}")
                self.wait_user()

            elif pilihan == "0":
                self.save_state()
                print("✔ State data berhasil disinkronisasi ke JSON. Keluar program.")
                break
            else:
                print("! Opsi menu tidak valid.")
                self.wait_user()
