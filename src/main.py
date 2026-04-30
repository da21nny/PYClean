import tkinter as tk
from tkinter import messagebox, ttk

# importar funciones desde los módulos separados
from organizador import crear_frame_organizador
from gestor_almacenamiento import crear_frame_gestor
from backup_automatico import crear_frame_backup
from eliminar_duplicados import crear_frame_duplicados
import sorpresa  # agregado
from limpieza import crear_frame_limpieza

# Variables de estilo
FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_DESC = ("Segoe UI", 10)
BG_APP = "#F0F2F5"
BG_CARD = "#FFFFFF"

# función para crear la interfaz principal
def crear_interfaz():
    root = tk.Tk()
    root.title("🗂️ PyClean - Gestor de Archivos")
    root.geometry("900x550")
    root.resizable(False, False)
    root.configure(bg=BG_APP)

    # Header
    header = tk.Frame(root, bg="#2C3E50", height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(header, text="PyClean", font=("Segoe UI", 20, "bold"), bg="#2C3E50", fg="white").pack(side="left", padx=20)
    tk.Label(header, text="Mantén tu sistema organizado y limpio", font=("Segoe UI", 11), bg="#2C3E50", fg="#BDC3C7").pack(side="left", pady=25)

    main_container = tk.Frame(root, bg=BG_APP)
    main_container.pack(fill="both", expand=True, padx=20, pady=20)

    frame_principal = tk.Frame(main_container, bg=BG_APP)
    frame_principal.pack(fill="both", expand=True)

    # Grid config
    for i in range(3): frame_principal.grid_columnconfigure(i, weight=1)
    for i in range(2): frame_principal.grid_rowconfigure(i, weight=1)

    def cambiar_vista(crear_frame_func):
        frame_principal.pack_forget()
        f_nuevo = tk.Frame(main_container, bg=BG_APP)
        f_nuevo.pack(fill="both", expand=True)

        def volver():
            f_nuevo.destroy()
            frame_principal.pack(fill="both", expand=True)

        ui = crear_frame_func(f_nuevo, on_close=volver)
        ui.pack(fill="both", expand=True)

    # Mapeo de herramientas a tarjetas
    herramientas = [
        {"row": 0, "col": 0, "icono": "📁", "color": "#27AE60", "titulo": "Organizador", "desc": "Organiza archivos en carpetas\nsegún su extensión.", "cmd": lambda: cambiar_vista(crear_frame_organizador)},
        {"row": 0, "col": 1, "icono": "🔍", "color": "#2980B9", "titulo": "Duplicados", "desc": "Encuentra y gestiona\narchivos duplicados.", "cmd": lambda: cambiar_vista(crear_frame_duplicados)},
        {"row": 0, "col": 2, "icono": "🧹", "color": "#8E44AD", "titulo": "Limpieza Basura", "desc": "Elimina archivos temporales\ny libera espacio.", "cmd": lambda: cambiar_vista(crear_frame_limpieza)},
        {"row": 1, "col": 0, "icono": "⚙️", "color": "#F39C12", "titulo": "Copia de Seguridad", "desc": "Crea backups seguros\nde tus carpetas.", "cmd": lambda: cambiar_vista(crear_frame_backup)},
        {"row": 1, "col": 1, "icono": "🔧", "color": "#D35400", "titulo": "Gestor Espacio", "desc": "Encuentra archivos grandes\n(> 512MB).", "cmd": lambda: cambiar_vista(crear_frame_gestor)},
        {"row": 1, "col": 2, "icono": "💽", "color": "#7F8C8D", "titulo": "Escanear Drivers", "desc": "Analiza controladores.\n(Proyecto a futuro)", "cmd": lambda: cambiar_vista(sorpresa.crear_frame_sorpresa)},
    ]

    for h in herramientas:
        crear_tarjeta(frame_principal, h)

    footer = tk.Frame(root, bg=BG_APP)
    footer.pack(side="bottom", fill="x", pady=10)
    tk.Label(footer, text="Desarrollado por Los Penguin 1 💻", font=("Segoe UI", 9), bg=BG_APP, fg="#7F8C8D").pack()

    root.mainloop()

def crear_tarjeta(parent, data):
    marco = tk.Frame(parent, bg=BG_APP)
    marco.grid(row=data["row"], column=data["col"], padx=10, pady=10, sticky="nsew")

    tarjeta = tk.Frame(marco, bg=BG_CARD, highlightbackground="#D5D8DC", highlightthickness=1)
    tarjeta.pack(fill="both", expand=True)

    tk.Label(tarjeta, text=data["icono"], font=("Segoe UI", 32), bg=BG_CARD, fg=data["color"]).pack(pady=(15, 5))
    tk.Label(tarjeta, text=data["titulo"], font=FONT_TITLE, bg=BG_CARD, fg="#2C3E50").pack()
    tk.Label(tarjeta, text=data["desc"], font=FONT_DESC, bg=BG_CARD, fg="#7F8C8D", justify="center").pack(pady=(5, 15))

    btn = tk.Button(tarjeta, text="Abrir Herramienta", font=("Segoe UI", 10, "bold"), 
                    bg=data["color"], fg="white", relief="flat", cursor="hand2", command=data["cmd"])
    btn.pack(side="bottom", fill="x", ipady=8)

    def on_enter(e): btn.config(bg="#34495E")
    def on_leave(e): btn.config(bg=data["color"])
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

#ejecutar la interfaz principal
if __name__ == "__main__":
    crear_interfaz()
