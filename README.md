# 📁 Proyecto: PYClean - Gestor de Archivos - Version GUI

Automatiza tareas comunes con Python: Organización de archivos, Copia de Seguridad, Limpieza de archivos basura, Eliminacion de archivos Duplicados, Gestion de Almacenamiento, Escaner de Drivers(Proyecto a futuro).  

Proyecto nos ayudo con la lógica, condicionales, bucles, manejo del sistema de archivos y entorno grafico.

---

## 🧠 Descripción General

Este script permite realizar distintas tareas desde una Interfaz Grafica (TKinter):
1. Organizar archivos por tipo  
2. Crear copias de respaldo (backup)  
3. Buscar archivos duplicados  
4. Gestionar almacenamiento (detectar archivos grandes)
5. Limpieza de Archivos Basura
6. Escaneo de Drivers (Proyecto a futuro)

Cada función es independiente y se ejecuta desde un **menú principal**.

---

## ⚙️ Requisitos

- **Python > 3.11
- Módulos estándar: `os`, `shutil`, `time`, `datetime`, `tkinter`, `filedialog`, `messagebox`, `send2trash`
- Editor recomendado: Visual Studio Code
- Sistema operativo: Solo Windows 10 y posteriores

## 🚀 Ejecución

### Desde la terminal (Recomendado)
1. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el script principal:
   ```bash
   python run.py
   ```

### 📦 Creación de Ejecutable (.exe) (Opcional)
Si deseas generar un archivo ejecutable (.exe) para usarlo de forma independiente:

1. Asegúrate de haber instalado las dependencias (`pyinstaller` está incluido en `requirements.txt`).
2. Ejecuta el siguiente comando desde la raíz del proyecto:
   ```bash
   pyinstaller --onefile --windowed --icon=assets/icono.ico --add-data "assets/bsod.gif;assets" --name "PYClean" src/main.py
   ```
3. El archivo `PYClean.exe` se generará dentro de la carpeta `dist/`.
---
## Desarrolladores
-Edgar Vega
-Ivan Leiva
-Kevin Santiago Gaona
-Cristian Fernandez
-Mariano Gomez
