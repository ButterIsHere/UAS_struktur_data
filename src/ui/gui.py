# ==============================================================================
# MODULE: GUI INTERFACE UPGRADE (HIGH-CONTRAST LIGHT MODE & REAL-TIME SORT DISPLAY)
# Implementasi antarmuka berbasis Light Mode dengan tingkat kontras tinggi.
# Dilengkapi fitur pembaruan urutan tabel secara real-time saat sorting dieksekusi.
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from src.algorithms.searching import linear_search, binary_search
from src.algorithms.sorting import quick_sort

class LibraryGUI:
    def __init__(self, system_backend):
        self.sys = system_backend

        # Root Window Setup
        self.root = tk.Tk()
        self.root.title("Digital Library Ecosystem - High Contrast Light Mode")
        self.root.geometry("1020x680")

        # ----------------------------------------------------------------------
        # PALET WARNA: HIGH-CONTRAST LIGHT MODE
        # ----------------------------------------------------------------------
        self.COLOR_BG = "#ffffff"          # Putih murni untuk background utama
        self.COLOR_PANEL = "#f8f9fa"       # Abu-abu sangat muda untuk card/frame
        self.COLOR_TEXT = "#000000"        # Hitam murni untuk teks utama (Kontras Maksimal)
        self.COLOR_TEXT_MUTED = "#333333"  # Hitam arang untuk label sekunder
        self.COLOR_ACCENT = "#1a73e8"      # Biru tegas untuk aksen/tombol utama
        self.COLOR_BORDER = "#cccccc"      # Abu-abu untuk border yang jelas

        self.root.configure(bg=self.COLOR_BG)

        # Konfigurasi widget standar melalui TTK Style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Style global elemen dasar
        self.style.configure(".", background=self.COLOR_BG, foreground=self.COLOR_TEXT, fieldbackground=self.COLOR_PANEL)
        self.style.configure("TLabel", font=("Helvetica", 10, "bold"), background=self.COLOR_BG, foreground=self.COLOR_TEXT)
        self.style.configure("TEntry", font=("Helvetica", 10), foreground=self.COLOR_TEXT)

        # Style Tombol Kontras Tinggi
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), background=self.COLOR_ACCENT, foreground="#ffffff", borderwidth=1)
        self.style.map("TButton", background=[("active", "#1557b0")])

        # Style Treeview (Tabel Data) Kontras Tinggi
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=26, background=self.COLOR_BG, foreground=self.COLOR_TEXT, fieldbackground=self.COLOR_BG)
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=self.COLOR_PANEL, foreground=self.COLOR_TEXT, borderwidth=1)
        self.style.map("Treeview", background=[("selected", "#e8f0fe")], foreground=[("selected", "#1a73e8")])

        # State penampung data untuk tampilan visual (bisa berubah saat disortir)
        self.displayed_books = self.sys.inventaris.to_list()

        self._build_ui()
        self.refresh_all_views()

    def _build_ui(self):
        # ----------------------------------------------------------------------
        # HEADER LAYER
        # ----------------------------------------------------------------------
        header_frame = tk.Frame(self.root, bg=self.COLOR_PANEL, height=60, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="SISTEM MANAJEMEN PERPUSTAKAAN DIGITAL", font=("Helvetica", 14, "bold"), bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).pack(side="left", padx=20)

        btn_save = ttk.Button(header_frame, text="💾 Sync State (JSON)", command=self.save_state)
        btn_save.pack(side="right", padx=20, pady=10)

        # ----------------------------------------------------------------------
        # MAIN BODY PANEL SPLIT
        # ----------------------------------------------------------------------
        main_container = tk.Frame(self.root, bg=self.COLOR_BG)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        left_panel = tk.Frame(main_container, bg=self.COLOR_BG)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_panel = tk.Frame(main_container, bg=self.COLOR_BG)
        right_panel.pack(side="right", fill="both", expand=True)

        # ----------------------------------------------------------------------
        # LEFT PANEL: MODUL KONTROL & ENGINE
        # ----------------------------------------------------------------------
        # Frame 1: Kelola Inventaris Buku (SLL)
        inv_frame = tk.LabelFrame(left_panel, text=" [1] Inventaris Buku (Singly Linked List) ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=10)
        inv_frame.pack(fill="x", pady=(0, 10))

        grid_inputs = tk.Frame(inv_frame, bg=self.COLOR_PANEL)
        grid_inputs.pack(fill="x")

        tk.Label(grid_inputs, text="ID (Kosongkan utk Auto):", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_book_id = ttk.Entry(grid_inputs, width=10)
        self.ent_book_id.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(grid_inputs, text="Judul Buku:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", pady=5, padx=(10, 0))
        self.ent_book_title = ttk.Entry(grid_inputs, width=22)
        self.ent_book_title.grid(row=0, column=3, sticky="w", padx=5)

        btn_ops = tk.Frame(inv_frame, bg=self.COLOR_PANEL)
        btn_ops.pack(fill="x", pady=(10, 0))
        ttk.Button(btn_ops, text="Tambah Buku", command=self.add_book).pack(side="left", padx=2)
        ttk.Button(btn_ops, text="Hapus Buku (by ID)", command=self.delete_book).pack(side="left", padx=2)

        # Frame 2: Sirkulasi Transaksi (Queue FIFO)
        queue_frame = tk.LabelFrame(left_panel, text=" [2 & 3] Sirkulasi Transaksi (Queue FIFO) ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=10)
        queue_frame.pack(fill="x", pady=(0, 10))

        grid_q = tk.Frame(queue_frame, bg=self.COLOR_PANEL)
        grid_q.pack(fill="x")
        tk.Label(grid_q, text="Nama Peminjam:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, font=("Helvetica", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_borrower = ttk.Entry(grid_q, width=15)
        self.ent_borrower.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(grid_q, text="Target ID Buku:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, font=("Helvetica", 9, "bold")).grid(row=0, column=2, sticky="w", pady=5, padx=(10, 0))
        self.ent_q_book_id = ttk.Entry(grid_q, width=10)
        self.ent_q_book_id.grid(row=0, column=3, sticky="w", padx=5)

        tk.Label(queue_frame, text="ID Transaksi untuk Hapus Spesifik / Batal:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT_MUTED, font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(10, 2))
        self.ent_cancel_tx_id = ttk.Entry(queue_frame, width=15)
        self.ent_cancel_tx_id.pack(anchor="w", pady=2)

        btn_q_ops = tk.Frame(queue_frame, bg=self.COLOR_PANEL)
        btn_q_ops.pack(fill="x", pady=(10, 0))
        ttk.Button(btn_q_ops, text="Enqueue Antrean", command=self.enqueue_tx).pack(side="left", padx=2)
        ttk.Button(btn_q_ops, text="Process FIFO (Front)", command=self.dequeue_tx).pack(side="left", padx=2)
        ttk.Button(btn_q_ops, text="Hapus via ID", command=self.cancel_tx_by_id).pack(side="left", padx=2)

        # Frame 3: Searching & Sorting Engine (Modul Utama Display Respon)
        engine_frame = tk.LabelFrame(left_panel, text=" [4 & 5] Algoritma Pemrosesan (Search & Sort) ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=10)
        engine_frame.pack(fill="both", expand=True)

        tk.Label(engine_frame, text="Query Cari / Kata Kunci:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, font=("Helvetica", 9, "bold")).pack(anchor="w")
        self.ent_search_query = ttk.Entry(engine_frame)
        self.ent_search_query.pack(fill="x", pady=5)

        btn_eng = tk.Frame(engine_frame, bg=self.COLOR_PANEL)
        btn_eng.pack(fill="x", pady=5)
        ttk.Button(btn_eng, text="Linear Search (Judul)", command=self.exec_linear_search).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(btn_eng, text="Binary Search (ID)", command=self.exec_binary_search).pack(side="left", fill="x", expand=True, padx=2)

        # Tombol Sort Utama yang akan mengubah susunan display tabel secara reaktif
        ttk.Button(btn_eng, text="⚡ Quick Sort (Urutkan ID)", command=self.exec_quick_sort).pack(side="left", fill="x", expand=True, padx=2)
        ttk.Button(btn_eng, text="🔄 Reset Tampilan", command=self.reset_display).pack(side="left", fill="x", expand=True, padx=2)

        # ----------------------------------------------------------------------
        # RIGHT PANEL: LIVE HIGH-CONTRAST DATAVIEW TABLES
        # ----------------------------------------------------------------------
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Data Inventaris Table (Merespon Aksi Sort & Search secara langsung)
        self.tab_inv = tk.Frame(self.notebook, bg=self.COLOR_BG)
        self.notebook.add(self.tab_inv, text=" Data Inventaris Buku ")

        self.tree_inv = ttk.Treeview(self.tab_inv, columns=("ID", "Judul"), show="headings")
        self.tree_inv.heading("ID", text="Book ID ↕")
        self.tree_inv.heading("Judul", text="Judul Buku / Literatur")
        self.tree_inv.column("ID", width=120, anchor="center")
        self.tree_inv.pack(fill="both", expand=True)

        # Tab 2: Live Queue Table
        self.tab_queue = tk.Frame(self.notebook, bg=self.COLOR_BG)
        self.notebook.add(self.tab_queue, text=" Manifest Antrean (FIFO) ")

        self.tree_queue = ttk.Treeview(self.tab_queue, columns=("Tx ID", "Peminjam", "ID Buku"), show="headings")
        self.tree_queue.heading("Tx ID", text="Tx ID")
        self.tree_queue.heading("Peminjam", text="Nama Anggota")
        self.tree_queue.heading("ID Buku", text="ID Buku Target")
        self.tree_queue.column("Tx ID", width=90, anchor="center")
        self.tree_queue.pack(fill="both", expand=True)

        # Tab 3: Log Riwayat Aktivitas (DLL)
        self.tab_logs = tk.Frame(self.notebook, bg=self.COLOR_BG)
        self.notebook.add(self.tab_logs, text=" [7] Audit Log (DLL) ")

        self.txt_logs = tk.Text(self.tab_logs, bg=self.COLOR_BG, fg=self.COLOR_TEXT, wrap="word", font=("Courier", 10), bd=1, relief="solid")
        self.txt_logs.pack(fill="both", expand=True)

        # Bottom Area: BST Visualizer
        tree_op_frame = tk.LabelFrame(right_panel, text=" [6] Operasi Non-Linear Index ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=5)
        tree_op_frame.pack(fill="x", side="bottom", pady=(10, 0))
        ttk.Button(tree_op_frame, text="Generate & Print Structure Tree ke Terminal STDOUT", command=self.trigger_bst_visualizer).pack(fill="x", pady=5)

    # ----------------------------------------------------------------------
    # RENDERING & INTERACTION LOGIC
    # ----------------------------------------------------------------------
    def refresh_all_views(self):
        """Memetakan data aktual ke dalam komponen grafis."""
        # Render Tabel Inventaris berdasarkan susunan state internal 'displayed_books'
        for i in self.tree_inv.get_children():
            self.tree_inv.delete(i)
        for item in self.displayed_books:
            self.tree_inv.insert("", "end", values=(item["id"], item["title"]))

        # Render Tabel Antrean
        for i in self.tree_queue.get_children():
            self.tree_queue.delete(i)
        for q in self.sys.antrean_peminjaman.to_list():
            self.tree_queue.insert("", "end", values=(q.get("tx_id", "-"), q["peminjam"], q["book_id"]))

        # Render Logs
        self.txt_logs.delete("1.0", tk.END)
        for log in self.sys.riwayat_aktivitas.to_list():
            self.txt_logs.insert(tk.END, f"[LOG] {log}\n")
        self.txt_logs.see(tk.END)

    def reset_display(self):
        """Mengembalikan urutan display ke urutan input asli memori (SLL)."""
        self.displayed_books = self.sys.inventaris.to_list()
        self.refresh_all_views()

    def add_book(self):
        try:
            id_input = self.ent_book_id.get().strip()
            title = self.ent_book_title.get().strip()
            if not title: raise ValueError("Judul kosong")

            b_id = int(id_input) if id_input else (max([b["id"] for b in self.sys.inventaris.to_list()] + [0]) + 1)

            # Validasi ID Duplikat
            if any(book["id"] == b_id for book in self.sys.inventaris.to_list()):
                messagebox.showerror("Duplicate Error", f"Buku dengan ID {b_id} sudah ada!")
                return

            book = {"id": b_id, "title": title}
            self.sys.inventaris.append(book)
            self.sys.bst_index.insert(b_id, book)
            self.sys.riwayat_aktivitas.append(f"Tambah buku: {title} (ID: {b_id})")

            self.ent_book_id.delete(0, tk.END)
            self.ent_book_title.delete(0, tk.END)

            # Kembalikan display ke state aslinya dan muat data baru
            self.displayed_books = self.sys.inventaris.to_list()
            self.refresh_all_views()
            self.sys.save_state()
        except ValueError as e:
            messagebox.showerror("Error", f"Verifikasi input Anda: {e}")

    def delete_book(self):
        try:
            b_id = int(self.ent_book_id.get().strip())
            if self.sys.inventaris.delete(b_id):
                self.sys.riwayat_aktivitas.append(f"Hapus buku ID: {b_id}")
                messagebox.showinfo("Success", f"Buku ID {b_id} berhasil dihapus.")
                self.displayed_books = self.sys.inventaris.to_list()
                self.refresh_all_views()
                self.sys.save_state()
            else:
                messagebox.showwarning("Not Found", "ID Buku tidak ditemukan.")
            self.ent_book_id.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Gunakan angka murni untuk mencari ID yang akan dihapus.")

    def enqueue_tx(self):
        try:
            nama = self.ent_borrower.get().strip()
            b_id = int(self.ent_q_book_id.get().strip())
            if not nama: raise ValueError()

            tx_id = max([q["tx_id"] for q in self.sys.antrean_peminjaman.to_list() if "tx_id" in q] + [1000]) + 1
            self.sys.antrean_peminjaman.enqueue({"tx_id": tx_id, "peminjam": nama, "book_id": b_id})
            self.sys.riwayat_aktivitas.append(f"Enqueue Antrean #{tx_id}: {nama}")

            self.ent_borrower.delete(0, tk.END)
            self.ent_q_book_id.delete(0, tk.END)
            self.refresh_all_views()
            self.sys.save_state()
        except ValueError:
            messagebox.showerror("Error", "Lengkapi Nama Anggota dan pastikan ID Buku diisi dengan Angka.")

    def dequeue_tx(self):
        proses = self.sys.antrean_peminjaman.dequeue()
        if proses:
            self.sys.riwayat_aktivitas.append(f"FIFO memproses transaksi #{proses.get('tx_id')}")
            self.refresh_all_views()
            self.sys.save_state()
        else:
            messagebox.showwarning("Empty", "Antrean kosong.")

    def cancel_tx_by_id(self):
        try:
            target = int(self.ent_cancel_tx_id.get().strip())
            old_items = self.sys.antrean_peminjaman.to_list()

            from src.structures.queue import Queue
            self.sys.antrean_peminjaman = Queue()
            found = False

            for item in old_items:
                if item.get("tx_id") == target:
                    found = True
                    self.sys.riwayat_aktivitas.append(f"Membatalkan Transaksi Antrean #{target}")
                    continue
                self.sys.antrean_peminjaman.enqueue(item)

            if found:
                messagebox.showinfo("Success", f"Antrean #{target} berhasil dihapus.")
                self.ent_cancel_tx_id.delete(0, tk.END)
            else:
                messagebox.showwarning("Error", "Tx ID tidak ditemukan.")
                for item in old_items: self.sys.antrean_peminjaman.enqueue(item)

            self.refresh_all_views()
            self.sys.save_state()
        except ValueError:
            messagebox.showerror("Error", "Gunakan ID angka.")

    # ----------------------------------------------------------------------
    # STRATEGI RESPONSIVE ALGORITMA (SEARCH & SORT DISPLAY)
    # ----------------------------------------------------------------------
    def exec_quick_sort(self):
        """URUTKAN LIVE DISPLAY: Memanggil Quick Sort O(n log n) dan langsung merubah susunan Treeview."""
        if not self.displayed_books:
            messagebox.showwarning("Notice", "Tidak ada data buku di view saat ini untuk diurutkan.")
            return

        # Mengeksekusi algoritma built-from-scratch quick_sort pada data penampung view
        self.displayed_books = quick_sort(self.displayed_books, 'id')

        # Segera refresh UI Treeview agar posisi data bergeser urut secara visual
        self.refresh_all_views()
        self.sys.riwayat_aktivitas.append("Mengurutkan visualisasi data tabel menggunakan Quick Sort Engine.")

    def exec_linear_search(self):
        """MEM-FILTER LIVE DISPLAY: Mencari data teks dan langsung memangkas isi Treeview."""
        q = self.ent_search_query.get().strip()
        if not q:
            self.reset_display()
            return
        # Lakukan linear search dari pool data master asli SLL
        self.displayed_books = linear_search(self.sys.inventaris.to_list(), q, 'title')
        self.refresh_all_views()

    def exec_binary_search(self):
        """MENCARI INDEKS SPESIFIK: Memanfaatkan Binary Search untuk menandai baris."""
        try:
            target = int(self.ent_search_query.get().strip())
            # Syarat Binary Search: Data wajib terurut terlebih dahulu
            sorted_master = quick_sort(self.sys.inventaris.to_list(), 'id')
            res = binary_search(sorted_master, target, 'id')

            if res:
                # Set display hanya memuat item tunggal yang ditemukan agar reaktif
                self.displayed_books = [res]
                self.refresh_all_views()
            else:
                messagebox.showinfo("Result", "ID tidak ditemukan di seluruh struktur memori.")
        except ValueError:
            messagebox.showerror("Error", "Binary search membutuhkan parameter input berupa Angka.")

    def trigger_bst_visualizer(self):
        """
        EKSPLORASI TINGKAT LANJUT: Floating Window BST Visualizer.
        Membuka window pop-up baru dan menggambar struktur hirarki pohon 
        secara grafis menggunakan Tkinter Canvas secara interaktif.
        """
        # Ambil root node dari BST backend
        root_node = self.sys.bst_index.root

        if not root_node:
            messagebox.showwarning("BST Empty", "Struktur indeks pohon kosong. Tambahkan beberapa buku terlebih dahulu!")
            return

        # 1. Inisialisasi Floating Window (Toplevel)
        bst_window = tk.Toplevel(self.root)
        bst_window.title("Struktur Indeks Non-Linear (Binary Search Tree)")
        bst_window.geometry("800x600")
        bst_window.configure(bg="#ffffff")

        # Angkat window agar berada di paling depan (Floating Mode)
        bst_window.transient(self.root)
        bst_window.grab_set()

        # 2. Tambahkan Label Header Komponen Kontras Tinggi
        tk.Label(
                bst_window, 
                text="Visualisasi Hirarki Binary Search Tree (Index Buku)", 
                font=("Helvetica", 12, "bold"), 
                bg="#ffffff", 
                fg="#000000"
                ).pack(pady=10)

        # 3. Tambahkan Area Kanvas dengan Scrollbar jika Tree Membesar
        canvas_frame = tk.Frame(bst_window, bg="#ffffff")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(canvas_frame, bg="#f8f9fa", bd=1, relief="solid")
        canvas.pack(fill="both", expand=True)

        # 4. Fungsi Rekursif untuk Menggambar Node dan Garis Penghubung
        def draw_node(node, x, y, x_offset, level):
            if not node:
                return

            radius = 18
            vertical_spacing = 70  # Jarak vertikal antar level pohon

            # Menggambar cabang ke kiri jika ada child kiri
            if node.left:
                canvas.create_line(x, y, x - x_offset, y + vertical_spacing, fill="#000000", width=2)
                draw_node(node.left, x - x_offset, y + vertical_spacing, x_offset / 1.8, level + 1)

            # Menggambar cabang ke kanan jika ada child kanan
            if node.right:
                canvas.create_line(x, y, x + x_offset, y + vertical_spacing, fill="#000000", width=2)
                draw_node(node.right, x + x_offset, y + vertical_spacing, x_offset / 1.8, level + 1)

            # Menggambar lingkaran Node (High Contrast Light Mode)
            canvas.create_oval(
                    x - radius, y - radius, x + radius, y + radius, 
                    fill="#e8f0fe", outline="#1a73e8", width=3
                    )

            # Menuliskan ID Buku (Key) di dalam lingkaran
            canvas.create_text(
                    x, y, text=str(node.key), 
                    font=("Helvetica", 9, "bold"), fill="#000000"
                    )

            # Menuliskan Judul Buku tepat di bawah lingkaran node sebagai metadata
            canvas.create_text(
                    x, y + radius + 10, text=node.value.get('title', ''), 
                    font=("Helvetica", 8), fill="#333333"
                    )

        # 5. Eksekusi Penggambaran Pohon dimulai dari koordinat tengah atas kanvas
        # Parameter: root_node, start_x, start_y, initial_x_offset, level
        bst_window.update() # Update dimensi window untuk presisi koordinat
        start_x = 400
        start_y = 40
        initial_x_offset = 180

        draw_node(root_node, start_x, start_y, initial_x_offset, 1)

        # 6. Tombol Tutup Window Floating
        ttk.Button(bst_window, text="Tutup Visualizer", command=bst_window.destroy).pack(pady=10)

    def save_state(self):
        self.sys.save_state()
        messagebox.showinfo("Persistence Saved", "State berhasil diekspor.")

    def run(self):
        self.root.mainloop()
