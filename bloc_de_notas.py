import tkinter as tk
from tkinter import filedialog, messagebox
import os

APP = "Bloc de notas"


class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x500")
        self.path = None

        # Área de texto con scroll
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)
        self.scroll = tk.Scrollbar(frame)
        self.scroll.pack(side="right", fill="y")
        self.text = tk.Text(
            frame,
            wrap="word",
            undo=True,
            font=("Consolas", 12),
            padx=8,
            pady=8,
            yscrollcommand=self.scroll.set,
        )
        self.text.pack(side="left", fill="both", expand=True)
        self.scroll.config(command=self.text.yview)

        # Menú mínimo
        menu = tk.Menu(self)
        archivo = tk.Menu(menu, tearoff=0)
        archivo.add_command(label="Nuevo", accelerator="Ctrl+N", command=self.nuevo)
        archivo.add_command(label="Abrir...", accelerator="Ctrl+O", command=self.abrir)
        archivo.add_command(label="Guardar", accelerator="Ctrl+S", command=self.guardar)
        archivo.add_command(
            label="Guardar como...", accelerator="Ctrl+Shift+S", command=self.guardar_como
        )
        menu.add_cascade(label="Archivo", menu=archivo)
        self.config(menu=menu)

        # Atajos
        self.bind("<Control-n>", lambda e: self.nuevo())
        self.bind("<Control-o>", lambda e: self.abrir())
        self.bind("<Control-s>", lambda e: self.guardar())
        self.bind("<Control-S>", lambda e: self.guardar_como())

        self.text.bind("<<Modified>>", self._on_modified)
        self.protocol("WM_DELETE_WINDOW", self.salir)
        self._actualizar_titulo()

    # --- Título ---
    def _on_modified(self, _event=None):
        self._actualizar_titulo()

    def _modificado(self):
        return self.text.edit_modified()

    def _actualizar_titulo(self):
        nombre = os.path.basename(self.path) if self.path else "Sin título"
        marca = "*" if self._modificado() else ""
        self.title(f"{marca}{nombre} - {APP}")

    # --- Confirmar cambios sin guardar ---
    def _confirmar(self):
        """Devuelve True si se puede continuar (guardó o descartó)."""
        if not self._modificado():
            return True
        resp = messagebox.askyesnocancel(APP, "¿Guardar los cambios?")
        if resp is None:
            return False
        if resp:
            return self.guardar()
        return True

    # --- Acciones ---
    def nuevo(self):
        if not self._confirmar():
            return
        self.text.delete("1.0", "end")
        self.path = None
        self.text.edit_modified(False)
        self.text.edit_reset()
        self._actualizar_titulo()

    def abrir(self):
        if not self._confirmar():
            return
        ruta = filedialog.askopenfilename(
            filetypes=[("Texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8", errors="replace") as f:
                contenido = f.read()
        except OSError as e:
            messagebox.showerror(APP, f"No se pudo abrir el archivo:\n{e}")
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", contenido)
        self.path = ruta
        self.text.edit_modified(False)
        self.text.edit_reset()
        self._actualizar_titulo()

    def guardar(self):
        if not self.path:
            return self.guardar_como()
        return self._escribir(self.path)

    def guardar_como(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return False
        return self._escribir(ruta)

    def _escribir(self, ruta):
        try:
            with open(ruta, "w", encoding="utf-8", newline="") as f:
                f.write(self.text.get("1.0", "end-1c"))
        except OSError as e:
            messagebox.showerror(APP, f"No se pudo guardar el archivo:\n{e}")
            return False
        self.path = ruta
        self.text.edit_modified(False)
        self._actualizar_titulo()
        return True

    def salir(self):
        if self._confirmar():
            self.destroy()


if __name__ == "__main__":
    Notepad().mainloop()
