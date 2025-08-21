#!/usr/bin/env python3
"""
Conversor de Sistemas Numéricos
Aplicación profesional para conversión entre sistemas numéricos.

Autor: [Tu Nombre]
Versión: 1.0.0
Fecha: 2024
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Configuración de la aplicación
APP_NAME = "Conversor de Sistemas Numéricos"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "800x600"
MIN_WINDOW_SIZE = (600, 450)


class ConversorApp:
    """Clase principal de la aplicación"""

    def __init__(self):
        """Inicializar la aplicación"""
        self.root = tk.Tk()
        self.setup_window()
        self.create_basic_layout()

    def setup_window(self):
        """Configurar la ventana principal"""
        # Configuraciones básicas
        self.root.title(APP_NAME)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)

        # Centrar ventana en pantalla
        self.center_window()

        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configurar icono (placeholder por ahora)
        try:
            # Aquí agregamos el icono después
            pass
        except:
            pass

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_basic_layout(self):
        """Crear el layout básico de la aplicación"""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar peso de las columnas y filas
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Título temporal
        title_label = ttk.Label(
            main_frame,
            text="🔢 Conversor de Sistemas Numéricos",
            font=("Arial", 24, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 30))

        # Mensaje temporal
        temp_label = ttk.Label(
            main_frame,
            text="Aplicación en desarrollo...\nSiguiente paso: Sistema de colores y tema",
            font=("Arial", 12),
            justify=tk.CENTER
        )
        temp_label.grid(row=1, column=0, pady=20)

        # Info de versión
        version_label = ttk.Label(
            main_frame,
            text=f"Versión {APP_VERSION}",
            font=("Arial", 10),
            foreground="gray"
        )
        version_label.grid(row=2, column=0, pady=(20, 0))

    def on_closing(self):
        """Manejar el cierre de la aplicación"""
        print("Cerrando aplicación...")
        self.root.destroy()

    def run(self):
        """Ejecutar la aplicación"""
        print(f"Iniciando {APP_NAME} v{APP_VERSION}")
        self.root.mainloop()


def main():
    """Función principal"""
    try:
        app = ConversorApp()
        app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()