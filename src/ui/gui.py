# ==============================================================================
# MODULE: GUI INTERFACE UPGRADE (BONUS FEATURE)
# Membuka window grafis berbasis Tkinter (Native di Arch/Wayland via XWayland).
# ==============================================================================

import tkinter as tk
from tkinter import messagebox

class LibraryGUI:
    def __init__(self, system_backend):
        self.sys = system_backend
        self.root = tk.Tk()
        self.root.title("Digital Library Ecosystem - Advanced GUI")
        self.root.geometry("500x400")
        
        tk.Label(self.root, text="Perpustakaan Digital Engine", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        tk.Button(self.root, text="Lihat Representasi Tree (BST)", command=self.show_tree, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Simpan State Aktual (.json)", command=self.save_data, width=30, height=2).pack(pady=10)
        tk.Button(self.root, text="Keluar & Sinkronisasi", command=self.root.quit, width=30, height=2).pack(pady=10)

    def show_tree(self):
        # Jalankan visualisasi teks di terminal stdout sekaligus
        self.sys.bst_index.visualize()
        messagebox.showinfo("Tree Visualizer", "Struktur hirarki BST dicetak pada terminal stdout Anda!")

    def save_data(self):
        self.sys.save_state()
        messagebox.showinfo("Success", "State data berhasil diekspor ke data/library_data.json")

    def run(self):
        self.root.mainloop()
