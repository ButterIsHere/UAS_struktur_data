#!/usr/bin/env python3
# ==============================================================================
# RUN ENGINE ARCHITECTURE
# Entry point untuk memilih mode Console (Wajib) atau GUI (Bonus Eksplorasi).
# ==============================================================================

import sys
from src.ui.console import LibrarySystem

def main():
    app = LibrarySystem()
    
    # Jalankan argumen '--gui' untuk mode window, default mode terminal CLI
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        try:
            from src.ui.gui import LibraryGUI
            gui_app = LibraryGUI(app)
            gui_app.run()
        except ImportError:
            print("Tkinter belum terinstal sempurna di Arch Anda. Jalankan: sudo pacman -S python-tkinter")
    else:
        app.run()

if __name__ == "__main__":
    main()
