import customtkinter as ctk
import threading
import time

class ThemeColors:
    PRIMARY = "#7371FC"
    SECONDARY = "#A594F9"
    BACKGROUND = "#2A2A2A"
    SURFACE = "#3A3A3A"
    ERROR = "#FF5252"
    SUCCESS = "#4CAF50"
    TEXT = "#FFFFFF"
    TEXT_SECONDARY = "#B3B3B3"

class BanterLoader(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="transparent", width=72, height=72)
        
        # Crear los 9 cuadros
        self.boxes = []
        for i in range(9):
            box = ctk.CTkFrame(
                self,
                width=20,
                height=20,
                fg_color="#51E4DC",
                corner_radius=6,
                bg_color="transparent",
                border_width=2,
                border_color="#51E4DC"
            )
            # Posicionar en una grid 3x3
            row = i // 3
            col = i % 3
            box.place(x=col * 26, y=row * 26)
            box._rotation = 45  # Rotación inicial de 45 grados
            box._pos = [col * 26, row * 26]  # Posición base
            self.boxes.append(box)
        
        # Iniciar animación
        self._animate()
    
    def _move_box(self, box_idx, time_percent):
        # Patrones de movimiento específicos para cada caja
        patterns = [
            # Caja 1 (superior izquierda)
            [[-26,0], [0,0], [0,0], [26,0], [26,26], [26,26], [26,26], [26,0], [0,0], [-26,0]],
            # Caja 2 (superior centro)
            [[0,0], [26,0], [0,0], [26,0], [26,26], [26,26], [26,26], [26,26], [0,26], [0,26]],
            # Caja 3 (superior derecha)
            [[-26,0], [-26,0], [0,0], [-26,0], [-26,0], [-26,0], [-26,0], [-26,0], [-26,-26], [0,-26]],
            # Caja 4 (centro izquierda)
            [[-26,0], [-26,0], [-26,-26], [0,-26], [0,0], [0,-26], [0,-26], [0,-26], [-26,-26], [-26,0]],
            # Caja 5 (centro)
            [[0,0], [0,0], [0,0], [26,0], [26,0], [26,0], [26,0], [26,0], [26,-26], [0,-26]],
            # Caja 6 (centro derecha)
            [[0,0], [-26,0], [-26,0], [0,0], [0,0], [0,0], [0,0], [0,26], [-26,26], [-26,0]],
            # Caja 7 (inferior izquierda)
            [[26,0], [26,0], [26,0], [0,0], [0,-26], [26,-26], [0,-26], [0,-26], [0,0], [26,0]],
            # Caja 8 (inferior centro)
            [[0,0], [-26,0], [-26,-26], [0,-26], [0,-26], [0,-26], [0,-26], [0,-26], [26,-26], [26,0]],
            # Caja 9 (inferior derecha)
            [[-26,0], [-26,0], [0,0], [-26,0], [0,0], [0,0], [-26,0], [-26,0], [-52,0], [-26,0]]
        ]
        
        # Obtener patrón para esta caja
        moves = patterns[box_idx]
        
        # Encontrar el índice del movimiento actual
        move_idx = int(time_percent * 10)
        if move_idx >= len(moves):
            move_idx = len(moves) - 1
            
        # Obtener el desplazamiento base
        base_x = (box_idx % 3) * 26
        base_y = (box_idx // 3) * 26
        
        # Aplicar el movimiento
        offset = moves[move_idx]
        x = base_x + offset[0]
        y = base_y + offset[1]
        
        return x, y
    
    def _animate(self):
        if not hasattr(self, "_start_time"):
            self._start_time = time.time()
        
        current_time = time.time()
        elapsed = (current_time - self._start_time) % 4  # Ciclo de 4 segundos
        time_percent = elapsed / 4
        
        # Actualizar posición de cada caja
        for i, box in enumerate(self.boxes):
            x, y = self._move_box(i, time_percent)
            box.place(x=x, y=y)
            
            # Rotar 45 grados
            # Calcular rotación y opacidad
            box.configure(
                corner_radius=6
            )
        
        # Continuar animación
        if self.winfo_exists():
            self.after(16, self._animate)  # ~60 FPS

class LoadingScreen(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # Configurar ventana
        self.title("")
        self.geometry("400x300")
        self.resizable(False, False)
        self.configure(fg_color=ThemeColors.BACKGROUND)
        
        # Centrar ventana
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        
        # Quitar barra de título
        self.overrideredirect(True)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True)
        
        # Título
        self.title_label = ctk.CTkLabel(
            main_frame,
            text="Conversor Numérico",
            font=("Inter", 28, "bold"),
            text_color=ThemeColors.PRIMARY
        )
        self.title_label.pack(pady=(0, 20))
        
        # Banter Loader
        self.loader = BanterLoader(main_frame)
        self.loader.pack(pady=20)
        
        # Autor
        self.author_label = ctk.CTkLabel(
            main_frame,
            text="by Jasser Cedeño",
            font=("Inter", 16),
            text_color=ThemeColors.TEXT_SECONDARY
        )
        self.author_label.pack(pady=20)
        
        # Auto-cerrar después de 3 segundos
        self.after(3000, self.destroy)

class NumberConverterApp:
    def __init__(self):
        # Configurar tema global
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.withdraw()
        self.root.title("Conversor Numérico")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.configure(fg_color=ThemeColors.BACKGROUND)
        
        # Variables
        self.current_base = ctk.StringVar(value="decimal")
        self.result_cards = {}
        
        # Mostrar pantalla de carga
        self.splash = LoadingScreen()
        self.root.after(3000, self._finish_splash)
    
    def _finish_splash(self):
        self.splash.destroy()
        
        # Crear interfaz
        self.setup_ui()
        
        # Centrar y mostrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
        self.root.deiconify()
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Panel izquierdo
        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Título
        title = ctk.CTkLabel(
            self.left_panel,
            text="Conversor\nNumérico",
            font=("Inter", 32, "bold"),
            text_color=ThemeColors.TEXT,
            justify="left"
        )
        title.pack(anchor="w", pady=(0, 30))
        
        # Selector de bases
        self.bases_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.bases_frame.pack(fill="x", pady=(0, 20))
        
        self.base_buttons = {}
        bases = [
            ("Decimal", "decimal"),
            ("Binario", "binario"),
            ("Octal", "octal"),
            ("Hexadecimal", "hexadecimal")
        ]
        
        for name, value in bases:
            btn = ctk.CTkButton(
                self.bases_frame,
                text=name,
                command=lambda v=value: self.change_base(v),
                fg_color=ThemeColors.SURFACE if value == self.current_base.get() else "transparent",
                border_width=2 if value != self.current_base.get() else 0,
                hover_color=ThemeColors.PRIMARY,
                font=("Inter", 14)
            )
            btn.pack(fill="x", pady=5)
            self.base_buttons[value] = btn
        
        # Campo de entrada
        input_frame = ctk.CTkFrame(self.left_panel, fg_color=ThemeColors.SURFACE)
        input_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(
            input_frame,
            text="Ingrese un número:",
            font=("Inter", 14),
            text_color=ThemeColors.TEXT_SECONDARY
        ).pack(padx=15, pady=(15, 5))
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Escriba aquí",
            font=("Inter", 18),
            height=40,
            fg_color="transparent",
            text_color=ThemeColors.TEXT,
            border_width=0
        )
        self.input_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Ejemplo actual
        examples = {
            "decimal": "Ej: 255, 128, 64",
            "binario": "Ej: 1010, 1100, 11111111",
            "octal": "Ej: 377, 200, 77",
            "hexadecimal": "Ej: FF, 80, A5"
        }
        
        self.example_label = ctk.CTkLabel(
            input_frame,
            text=examples["decimal"],
            font=("Inter", 12),
            text_color=ThemeColors.TEXT_SECONDARY
        )
        self.example_label.pack(padx=15, pady=(0, 15))
        
        # Botón de conversión
        convert_btn = ctk.CTkButton(
            self.left_panel,
            text="Convertir",
            font=("Inter", 16, "bold"),
            height=45,
            fg_color=ThemeColors.PRIMARY,
            hover_color=ThemeColors.SECONDARY,
            command=self.convert
        )
        convert_btn.pack(fill="x", pady=(0, 20))
        
        # Panel derecho (resultados)
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Título de resultados
        ctk.CTkLabel(
            self.right_panel,
            text="Resultados",
            font=("Inter", 24, "bold"),
            text_color=ThemeColors.TEXT
        ).pack(anchor="w", pady=(0, 20))
        
        # Grid de resultados
        results_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        results_frame.pack(fill="both", expand=True)
        results_frame.grid_columnconfigure((0, 1), weight=1)
        results_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Crear tarjetas de resultado
        for i, (name, base) in enumerate(bases):
            if base != self.current_base.get():
                card = AnimatedCard(
                    results_frame,
                    title=name
                )
                card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
                self.result_cards[base] = card
    
    def change_base(self, base):
        if base == self.current_base.get():
            return
            
        old_base = self.current_base.get()
        self.current_base.set(base)
        self.input_entry.delete(0, "end")
        
        # Actualizar botones
        for value, btn in self.base_buttons.items():
            is_current = value == base
            btn.configure(
                fg_color=ThemeColors.SURFACE if is_current else "transparent",
                border_width=0 if is_current else 2
            )
        
        # Actualizar ejemplos
        examples = {
            "decimal": "Ej: 255, 128, 64",
            "binario": "Ej: 1010, 1100, 11111111",
            "octal": "Ej: 377, 200, 77",
            "hexadecimal": "Ej: FF, 80, A5"
        }
        self.example_label.configure(text=examples[base])
        
        # Reorganizar tarjetas de resultado
        for result_base, card in self.result_cards.items():
            card.grid_remove()
        
        self.result_cards.clear()
        
        bases = [
            ("Decimal", "decimal"),
            ("Binario", "binario"),
            ("Octal", "octal"),
            ("Hexadecimal", "hexadecimal")
        ]
        
        results_frame = self.right_panel.winfo_children()[1]  # El frame después del título
        i = 0
        for name, value in bases:
            if value != base:
                card = AnimatedCard(
                    results_frame,
                    title=name
                )
                card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
                self.result_cards[value] = card
                i += 1
    
    def convert(self):
        value = self.input_entry.get().strip()
        if not value:
            return
            
        try:
            # Primero convertir a decimal
            if self.current_base.get() == "decimal":
                decimal = int(value)
            elif self.current_base.get() == "binario":
                decimal = int(value, 2)
            elif self.current_base.get() == "octal":
                decimal = int(value, 8)
            else:  # hexadecimal
                decimal = int(value, 16)
                
            # Convertir a todas las bases
            conversions = {
                "decimal": str(decimal),
                "binario": bin(decimal)[2:],
                "octal": oct(decimal)[2:],
                "hexadecimal": hex(decimal)[2:].upper()
            }
            
            # Mostrar resultados con animación
            current = self.current_base.get()
            
            def animate_results():
                for base, card in self.result_cards.items():
                    card.set_value(conversions[base])
                    time.sleep(0.1)  # Pequeño retraso entre cada resultado
            
            # Ejecutar animación en un hilo separado
            threading.Thread(target=animate_results, daemon=True).start()
            
        except ValueError:
            pass  # Ignorar errores de validación por ahora
    
    def run(self):
        self.root.mainloop()

class AnimatedCard(ctk.CTkFrame):
    def __init__(self, *args, title: str = "", show_initial: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estado inicial
        self.visible = show_initial
        if not show_initial:
            self.grid_remove()
        
        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=("Inter", 16, "bold"),
            text_color=ThemeColors.TEXT
        )
        self.title.pack(pady=(15, 5))
        
        self.value = ctk.CTkLabel(
            self,
            text="",
            font=("Inter", 24),
            text_color=ThemeColors.TEXT
        )
        self.value.pack(pady=(5, 15))
        
        self.configure(
            fg_color=ThemeColors.SURFACE,
            corner_radius=15
        )
    
    def set_value(self, value: str):
        self.value.configure(text=value)
        
    def clear(self):
        self.value.configure(text="")
        
    def show(self):
        if not self.visible:
            self.visible = True
            self.grid()
            
    def hide(self):
        if self.visible:
            self.visible = False
            self.grid_remove()

if __name__ == "__main__":
    app = NumberConverterApp()
    app.run()
