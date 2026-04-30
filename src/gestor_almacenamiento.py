import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

#función para crear el frame del gestor de almacenamiento
def crear_frame_gestor(parent, on_close=None):
    frame = tk.Frame(parent, bg="#F0F2F5")
    archivos_encontrados = []

    # Definir carpetas esenciales a escanear
    usuario = Path.home()
    carpetas_esenciales = [
        usuario / 'Documents',
        usuario / 'Downloads',
        usuario / 'Music',
        usuario / 'Videos',
        usuario / 'Desktop'
    ]

    title = tk.Label(frame, text="🔧 Gestor de Almacenamiento", font=("Segoe UI", 16, "bold"), bg="#F0F2F5", fg="#2C3E50")
    title.pack(anchor="w", padx=20, pady=(20, 5))

    frame_botones = tk.Frame(frame, bg="#F0F2F5")
    frame_botones.pack(side="bottom", fill="x", padx=20, pady=10)

    progreso = ttk.Progressbar(frame, orient="horizontal", mode="determinate")
    progreso.pack(fill="x", padx=20, pady=5)

    lbl_estado = tk.Label(frame, text="Esperando para escanear...", font=("Segoe UI", 11), bg="#F0F2F5", fg="#333333")
    lbl_estado.pack(padx=20)

    columnas = ("Archivo", "Tamaño", "Ruta completa")
    tree = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
    for col in columnas:
        tree.heading(col, text=col)
    tree.column("Archivo", width=200)
    tree.column("Tamaño", width=80)
    tree.column("Ruta completa", width=340)

    tree_frame = tk.Frame(frame, bg="#F0F2F5")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    stop_event = threading.Event()
    scan_thread = None
    SIZE_LIMIT = 512 * 1024 * 1024  # 512 MB

    #=== FUNCIÓN PRINCIPAL ===
    def buscar_archivos_grandes():
        nonlocal archivos_encontrados
        archivos_encontrados.clear()
        for item in tree.get_children():
            tree.delete(item)

        lbl_estado.config(text="Escaneando carpetas esenciales...")
        stop_event.clear()

        total_archivos = 0
        for carpeta in carpetas_esenciales:
            if carpeta.exists():
                for _, _, archivos in os.walk(carpeta):
                    if stop_event.is_set():
                        lbl_estado.config(text="Escaneo cancelado.")
                        return
                    total_archivos += len(archivos)

        progreso["value"] = 0
        progreso["maximum"] = max(total_archivos, 1)
        procesados = 0

        for carpeta in carpetas_esenciales:
            if carpeta.exists():
                for ruta, _, archivos in os.walk(carpeta):
                    if stop_event.is_set():
                        lbl_estado.config(text="Escaneo cancelado.")
                        return
                    for archivo in archivos:
                        if stop_event.is_set():
                            lbl_estado.config(text="Escaneo cancelado.")
                            return
                        ruta_completa = os.path.join(ruta, archivo)
                        try:
                            size = os.path.getsize(ruta_completa)
                            if size > SIZE_LIMIT:
                                archivos_encontrados.append((ruta_completa, size))
                                tree.insert("", "end", values=(archivo, f"{size/1048576:.2f} MB", ruta_completa))
                        except Exception:
                            pass

                        procesados += 1
                        try:
                            progreso["value"] = procesados
                            frame.update_idletasks()
                        except tk.TclError:
                            return

        if stop_event.is_set():
            lbl_estado.config(text="Escaneo cancelado.")
            return

        if archivos_encontrados:
            lbl_estado.config(text=f"Escaneo completado: {len(archivos_encontrados)} archivos grandes encontrados.")
            messagebox.showinfo("Completado", f"Se encontraron {len(archivos_encontrados)} archivos mayores a 512 MB.")
        else:
            lbl_estado.config(text="No se encontraron archivos grandes.")
            messagebox.showinfo("Sin resultados", "No se encontraron archivos mayores a 512 MB.")

        btn_cancelar.config(state="disabled")

    #=== ELIMINAR ARCHIVOS SELECCIONADOS ===
    def eliminar_seleccionados():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "No seleccionaste ningún archivo para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar eliminación", "¿Deseas eliminar los archivos seleccionados?")
        if not confirm:
            return

        eliminados = 0
        espacio_liberado = 0
        for item in seleccion:
            ruta = tree.item(item, "values")[2]
            try:
                espacio_liberado += os.path.getsize(ruta)
                os.remove(ruta)
                tree.delete(item)
                eliminados += 1
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar:\n{ruta}\n{e}")

        espacio_mb = espacio_liberado / 1048576
        messagebox.showinfo("Eliminación completada",
                            f"Se eliminaron {eliminados} archivos.\nEspacio liberado: {espacio_mb:.2f} MB.")
        lbl_estado.config(text=f"Eliminados {eliminados} archivos | Liberados {espacio_mb:.2f} MB")

    #=== INICIAR Y CANCELAR ESCANEO ===
    def iniciar_escaneo():
        nonlocal scan_thread
        stop_event.clear()
        btn_cancelar.config(state="normal")
        scan_thread = threading.Thread(target=buscar_archivos_grandes)
        scan_thread.daemon = True
        scan_thread.start()

    def cancelar_escaneo():
        stop_event.set()
        btn_cancelar.config(state="disabled")
        lbl_estado.config(text="Cancelando escaneo...")

    def cerrar_o_volver():
        stop_event.set()
        if callable(on_close):
            on_close()
        else:
            parent.winfo_toplevel().destroy()

    def crear_btn(p, txt, col, cmd, st="normal"):
        b = tk.Button(p, text=txt, command=cmd, bg=col, fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", state=st)
        return b

    btn_salir = crear_btn(frame_botones, "↩ Volver" if callable(on_close) else "Salir", "#34495E", cerrar_o_volver)
    btn_eliminar = crear_btn(frame_botones, "🗑️ Eliminar seleccionados", "#E74C3C", eliminar_seleccionados)
    btn_cancelar = crear_btn(frame_botones, "✖ Cancelar", "#E74C3C", cancelar_escaneo)

    btn_salir.pack(side="right", padx=(5, 0))
    btn_eliminar.pack(side="right", padx=(5, 5))
    btn_cancelar.pack(side="right", padx=(0, 5))

    #llamar función para comenzar el escaneo
    iniciar_escaneo()

    return frame