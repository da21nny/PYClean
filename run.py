import sys
import os

# Asegurar que el directorio src está en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.main import crear_interfaz

if __name__ == "__main__":
    crear_interfaz()
