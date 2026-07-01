# =============================================================================
# MODULE: GUI INTERFACE UPGRADE (EMBEDDED AUTO-UPDATE VISUALIZER)
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from src.algorithms.searching import linear_search, binary_search
from src.algorithms.sorting import quick_sort

class LibraryGUI:
    def __init__(self, system_backend):
        self.sys = system_backend

        self.root = tk.Tk()
        self.root.title("Digital Library Ecosystem - High Contrast Light Mode")
        self.root.geometry("1150x750")

        self.COLOR_BG = "#ffffff"          
        self.COLOR_PANEL = "#f8f9fa"       
        self.COLOR_TEXT = "#000000"        
        self.COLOR_TEXT_MUTED = "#333333"  
        self.COLOR_ACCENT = "#1a73e8"      

        self.root.configure(bg=self.COLOR_BG)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=self.COLOR_BG, foreground=self.COLOR_TEXT, fieldbackground=self.COLOR_PANEL)
        self.style.configure("TLabel", font=("Helvetica", 10, "bold"), background=self.COLOR_BG, foreground=self.COLOR_TEXT)
        self.style.configure("TEntry", font=("Helvetica", 10), foreground=self.COLOR_TEXT)
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), background=self.COLOR_ACCENT, foreground="#ffffff", borderwidth=1)
        self.style.map("TButton", background=[("active", "#1557b0")])
        self.style.configure("Treeview", font=("Helvetica", 10), rowheight=26, background=self.COLOR_BG, foreground=self.COLOR_TEXT, fieldbackground=self.COLOR_BG)
        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background=self.COLOR_PANEL, foreground=self.COLOR_TEXT, borderwidth=1)
        self.style.map("Treeview", background=[("selected", "#e8f0fe")], foreground=[("selected", "#1a73e8")])

        self.displayed_books = self.sys.inventaris.to_list()

        self._build_ui()
        self.refresh_all_views()

    def _build_ui(self):
        # Header Top Panel
        header_frame = tk.Frame(self.root, bg=self.COLOR_PANEL, height=60, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="SISTEM MANAJEMEN PERPUSTAKAAN DIGITAL", font=("Helvetica", 14, "bold"), bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).pack(side="left", padx=20)
        ttk.Button(header_frame, text="💾 Sync State (JSON)", command=self.save_state).pack(side="right", padx=20, pady=10)

        # Main Container Splits
        main_container = tk.Frame(self.root, bg=self.COLOR_BG)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        left_panel = tk.Frame(main_container, bg=self.COLOR_BG)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_panel = tk.Frame(main_container, bg=self.COLOR_BG)
        right_panel.pack(side="right", fill="both", expand=True)

        # Modul [1]: Inventaris Buku (SLL)
        inv_frame = tk.LabelFrame(left_panel, text=" [1] Inventaris Buku (Singly Linked List) ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=8)
        inv_frame.pack(fill="x", pady=(0, 8))

        grid_inputs = tk.Frame(inv_frame, bg=self.COLOR_PANEL)
        grid_inputs.pack(fill="x")
        
        tk.Label(grid_inputs, text="ID (Auto):", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_book_id = ttk.Entry(grid_inputs, width=8)
        self.ent_book_id.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(grid_inputs, text="Judul Buku:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).grid(row=0, column=2, sticky="w", pady=5, padx=(10, 0))
        self.ent_book_title = ttk.Entry(grid_inputs, width=22)
        self.ent_book_title.grid(row=0, column=3, sticky="w", padx=5)

        # Checkbox Genre
        tk.Label(inv_frame, text="Pilih Genre:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).pack(anchor="w", pady=(5, 2))
        genre_frame = tk.Frame(inv_frame, bg=self.COLOR_PANEL)
        genre_frame.pack(fill="x", pady=2)

        self.genres_list = ["Sci-Fi", "Comic", "Novel", "Textbook", "History"]
        self.genre_vars = {}
        for g in self.genres_list:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(genre_frame, text=g, variable=var, bg=self.COLOR_PANEL, fg=self.COLOR_TEXT, activebackground=self.COLOR_PANEL)
            cb.pack(side="left", padx=4)
            self.genre_vars[g] = var

        btn_ops = tk.Frame(inv_frame, bg=self.COLOR_PANEL)
        btn_ops.pack(fill="x", pady=(5, 0))
        ttk.Button(btn_ops, text="Tambah Buku", command=self.add_book).pack(side="left", padx=2)
        ttk.Button(btn_ops, text="Hapus Buku (by ID)", command=self.delete_book).pack(side="left", padx=2)

        # Modul [2 & 3]: Queue
        queue_frame = tk.LabelFrame(left_panel, text=" [2 & 3] Sirkulasi Transaksi (Queue FIFO) ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=8)
        queue_frame.pack(fill="x", pady=(0, 8))

        grid_q = tk.Frame(queue_frame, bg=self.COLOR_PANEL)
        grid_q.pack(fill="x")
        tk.Label(grid_q, text="Peminjam:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_borrower = ttk.Entry(grid_q, width=12)
        self.ent_borrower.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(grid_q, text="ID Buku Target:", bg=self.COLOR_PANEL, fg=self.COLOR_TEXT).grid(row=0, column=2, sticky="w", pady=5, padx=(10, 0))
        self.ent_q_book_id = ttk.Entry(grid_q, width=8)
        self.ent_q_book_id.grid(row=0, column=3, sticky="w", padx=5)

        btn_q_ops = tk.Frame(queue_frame, bg=self.COLOR_PANEL)
        btn_q_ops.pack(fill="x", pady=(5, 0))
        ttk.Button(btn_q_ops, text="Enqueue", command=self.enqueue_tx).pack(side="left", padx=2)
        ttk.Button(btn_q_ops, text="Process FIFO", command=self.dequeue_tx).pack(side="left", padx=2)

        # Modul [4 & 5]: Search & Sort
        engine_frame = tk.LabelFrame(left_panel, text=" [4 & 5] Search & Sort Engine ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=10, pady=8)
        engine_frame.pack(fill="x", pady=(0, 8))

        self.ent_search_query = ttk.Entry(engine_frame)
        self.ent_search_query.pack(fill="x", pady=2)

        btn_eng = tk.Frame(engine_frame, bg=self.COLOR_PANEL)
        btn_eng.pack(fill="x", pady=4)
        ttk.Button(btn_eng, text="Linear (Judul)", command=self.exec_linear_search).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(btn_eng, text="Binary (ID)", command=self.exec_binary_search).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(btn_eng, text="⚡ Quick Sort", command=self.exec_quick_sort).pack(side="left", fill="x", expand=True, padx=1)
        ttk.Button(btn_eng, text="🔄 Reset", command=self.reset_display).pack(side="left", fill="x", expand=True, padx=1)



        # Modul [6]: EMBEDDED REAL-TIME TREE VISUALIZER
        self.tree_panel = tk.LabelFrame(left_panel, text=" [6] Library Hierarchy Index Visualizer (Auto Update & Scrollable) ", fg=self.COLOR_TEXT, bg=self.COLOR_PANEL, font=("Helvetica", 10, "bold"), padx=5, pady=5)
        self.tree_panel.pack(fill="both", expand=True)

        # Buat container frame untuk menampung canvas dan scrollbar
        canvas_container = tk.Frame(self.tree_panel, bg="#f8f9fa")
        canvas_container.pack(fill="both", expand=True)

        # Buat Scrollbar
        hbar = tk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        vbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buat Canvas dengan konfigurasi scrollregion awal
        self.canvas = tk.Canvas(canvas_container, bg="#f8f9fa", bd=1, relief="solid",
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=tk.LEFT, fill="both", expand=True)

        hbar.config(command=self.canvas.xview)
        vbar.config(command=self.canvas.yview)

        # FITUR DRAG-TO-SCROLL: Daftarkan event mouse klik kiri untuk menggeser canvas
        self.canvas.bind("<Button-1>", lambda event: self.canvas.scan_mark(event.x, event.y))
        self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))



        # --- RIGHT PANEL (Notebook View) ---
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True)

        self.tab_inv = tk.Frame(self.notebook, bg=self.COLOR_BG)
        self.notebook.add(self.tab_inv, text=" Data Inventaris Buku ")
        self.tree_inv = ttk.Treeview(self.tab_inv, columns=("ID", "Judul", "Genre"), show="headings")
        self.tree_inv.heading("ID", text="Book ID ↕", anchor="center")
        self.tree_inv.heading("Judul", text="Judul Buku / Literatur", anchor="w")
        self.tree_inv.heading("Genre", text="Genre", anchor="w")
        self.tree_inv.column("ID", width=70, stretch=False, anchor="center")
        self.tree_inv.column("Judul", width=220, anchor="w")
        self.tree_inv.column("Genre", width=160, anchor="w")
        self.tree_inv.pack(fill="both", expand=True)

        self.tab_queue = tk.Frame(self.notebook, bg=self.COLOR_BG)
        self.notebook.add(self.tab_queue, text=" Manifest Antrean ")
        self.tree_queue = ttk.Treeview(self.tab_queue, columns=("Tx ID", "Peminjam", "ID Buku"), show="headings")
        self.tree_queue.heading("Tx ID", text="Tx ID")
        self.tree_queue.heading("Peminjam", text="Nama Anggota")
        self.tree_queue.heading("ID Buku", text="ID Buku Target")
        self.tree_queue.column("Tx ID", width=80, anchor="center")
        self.tree_queue.pack(fill="both", expand=True)

        self.tab_logs = tk.Frame(self.notebook, bg=self.COLOR_BG)
        self.notebook.add(self.tab_logs, text=" [7] Audit Log (DLL) ")
        self.txt_logs = tk.Text(self.tab_logs, bg=self.COLOR_BG, fg=self.COLOR_TEXT, wrap="word", font=("Courier", 10))
        self.txt_logs.pack(fill="both", expand=True)

    def refresh_all_views(self):
        # 1. Update List Data Tabel
        for i in self.tree_inv.get_children():
            self.tree_inv.delete(i)
        for item in self.displayed_books:
            genres_str = ", ".join(item.get("genres", []))
            self.tree_inv.insert("", "end", values=(item["id"], item["title"], genres_str))

        # 2. Update List Antrean Queue
        for i in self.tree_queue.get_children():
            self.tree_queue.delete(i)
        for q in self.sys.antrean_peminjaman.to_list():
            self.tree_queue.insert("", "end", values=(q.get("tx_id", "-"), q["peminjam"], q["book_id"]))

        # 3. Update Audit Logs
        self.txt_logs.delete("1.0", tk.END)
        for log in self.sys.riwayat_aktivitas.to_list():
            self.txt_logs.insert(tk.END, f"[LOG] {log}\n")
        self.txt_logs.see(tk.END)

        # 4. AUTO RE-RENDER TREE GRAPHICS
        self.render_embedded_tree()

    def render_embedded_tree(self):
        self.canvas.delete("all")
        master_books = self.sys.inventaris.to_list()
        
        genre_map = {}
        no_genre_books = []
        for book in master_books:
            genres = book.get("genres", [])
            if not genres:
                no_genre_books.append(book)
            else:
                for g in genres:
                    if g not in genre_map: genre_map[g] = []
                    genre_map[g].append(book)
        if no_genre_books:
            genre_map["Uncategorized"] = no_genre_books

        # Koordinat Root Awal (Library Level 0)
        root_x = 240
        root_y = 25
        radius = 16

        # Draw Level 0: Library
        self.canvas.create_oval(root_x - 30, root_y - radius, root_x + 30, root_y + radius, fill="#1a73e8", outline="#1557b0", width=2)
        self.canvas.create_text(root_x, root_y, text="LIBRARY", font=("Helvetica", 9, "bold"), fill="#ffffff")

        if not genre_map:
            return

        genres_list = list(genre_map.keys())
        num_genres = len(genres_list)
        
        # Atur lebar jangkauan horizontal canvas kiri bawah
        spacing_x_g = 420 / max((num_genres - 1), 1) if num_genres > 1 else 0
        start_x_g = 40 if num_genres > 1 else 240
        
        g_y = 100       # Level 1 Tinggi Koordinat Y
        b_y_start = 160 # Level 2 Buku Koordinat Y awal

        for i, genre in enumerate(genres_list):
            g_x = start_x_g + (i * spacing_x_g) if num_genres > 1 else root_x
            
            # Line Level 0 -> Level 1
            self.canvas.create_line(root_x, root_y + radius, g_x, g_y - 12, fill="#b4b4b4", width=1)
            
            # Draw Level 1: Genre Box
            self.canvas.create_rectangle(g_x - 35, g_y - 12, g_x + 35, g_y + 12, fill="#e8f0fe", outline="#1a73e8", width=1)
            self.canvas.create_text(g_x, g_y, text=genre, font=("Helvetica", 8, "bold"), fill="#1a73e8")
            
            # Draw Level 2: Books under specific Genre (Stack Vertikal)
            for j, book in enumerate(genre_map[genre]):
                b_x = g_x
                b_y = b_y_start + (j * 32)
                
                # Line Level 1 -> Level 2
                if j == 0:
                    self.canvas.create_line(g_x, g_y + 12, b_x, b_y - 10, fill="#555555", width=1, dash=(2, 2))
                else:
                    self.canvas.create_line(b_x, b_y_start + ((j-1) * 32) + 10, b_x, b_y - 10, fill="#555555", width=1, dash=(2, 2))
                
                # Draw Level 2: Book Rectangles
                self.canvas.create_rectangle(b_x - 35, b_y - 10, b_x + 35, b_y + 10, fill="#ffffff", outline="#333333", width=1)
                
                display_title = book['title']
                if len(display_title) > 8: display_title = display_title[:7] + ".."
                self.canvas.create_text(b_x, b_y, text=f"ID:{book['id']} {display_title}", font=("Helvetica", 7), fill="#000000")

    def reset_display(self):
        self.displayed_books = self.sys.inventaris.to_list()
        self.refresh_all_views()

    def add_book(self):
        try:
            id_input = self.ent_book_id.get().strip()
            title = self.ent_book_title.get().strip()
            if not title: raise ValueError("Judul tidak boleh kosong.")
            
            selected_genres = [g for g, v in self.genre_vars.items() if v.get()]
            b_id = int(id_input) if id_input else (max([b["id"] for b in self.sys.inventaris.to_list()] + [0]) + 1)
            
            if any(book["id"] == b_id for book in self.sys.inventaris.to_list()):
                messagebox.showerror("Duplicate Error", f"ID {b_id} sudah terdaftar!")
                return

            book = {"id": b_id, "title": title, "genres": selected_genres}
            self.sys.inventaris.append(book)
            self.sys.bst_index.insert(b_id, book)
            self.sys.riwayat_aktivitas.append(f"Tambah buku: {title} [ID: {b_id}]")
            
            self.ent_book_id.delete(0, tk.END)
            self.ent_book_title.delete(0, tk.END)
            for v in self.genre_vars.values(): v.set(False)
            
            self.displayed_books = self.sys.inventaris.to_list()
            self.refresh_all_views() # Memicu update tabel dan auto-update visualizer tree
            self.sys.save_state()
        except ValueError as e:
            messagebox.showerror("Validation Error", f"Periksa input data: {e}")

    def delete_book(self):
        try:
            b_id = int(self.ent_book_id.get().strip())
            if self.sys.inventaris.delete(b_id):
                self.sys.riwayat_aktivitas.append(f"Hapus buku ID: {b_id}")
                messagebox.showinfo("Success", f"Buku ID {b_id} berhasil dihapus.")
                self.displayed_books = self.sys.inventaris.to_list()
                self.refresh_all_views() # Memicu auto-update visualizer tree
                self.sys.save_state()
            else:
                messagebox.showwarning("Not Found", f"Buku ID {b_id} tidak ditemukan.")
            self.ent_book_id.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Gunakan ID Angka.")

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
            messagebox.showerror("Error", "Lengkapi input Antrean dengan benar.")

    def dequeue_tx(self):
        proses = self.sys.antrean_peminjaman.dequeue()
        if proses:
            self.sys.riwayat_aktivitas.append(f"FIFO memproses transaksi #{proses.get('tx_id')}")
            messagebox.showinfo("Processed", f"Transaksi #{proses.get('tx_id')} sukses diproses.")
            self.refresh_all_views()
            self.sys.save_state()
        else:
            messagebox.showwarning("Empty", "Daftar antrean kosong.")

    def exec_quick_sort(self):
        if not self.displayed_books: return
        self.displayed_books = quick_sort(self.displayed_books, 'id')
        self.refresh_all_views()

    def exec_linear_search(self):
        q = self.ent_search_query.get().strip()
        if not q:
            self.reset_display()
            return
        self.displayed_books = linear_search(self.sys.inventaris.to_list(), q, 'title')
        self.refresh_all_views()

    def exec_binary_search(self):
        try:
            q = self.ent_search_query.get().strip()
            if not q:
                self.reset_display()
                return
            target = int(q)
            sorted_master = quick_sort(self.sys.inventaris.to_list(), 'id')
            res = binary_search(sorted_master, target, 'id')
            if res:
                self.displayed_books = [res]
                self.refresh_all_views()
            else:
                messagebox.showinfo("Result", "Buku tidak ditemukan.")
        except ValueError:
            messagebox.showerror("Error", "Gunakan ID Angka.")

    def save_state(self):
        self.sys.save_state()
        messagebox.showinfo("Persistence Saved", "State berhasil disinkronisasi.")

    def run(self):
        self.root.mainloop()
