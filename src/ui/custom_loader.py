"""
Componente de loader personalizado con animación SVG
"""
import customtkinter as ctk
import tkinter as tk
import time
import math
import threading

class LoaderAnimation(ctk.CTkCanvas):
    def __init__(self, *args, size: int = 100, **kwargs):
        super().__init__(*args, width=size, height=size, **kwargs)
        self.size = size
        self.configure(bg=kwargs.get('bg', '#2A2A2A'), highlightthickness=0)
        
        # Crear gradientes
        self._create_gradients()
        
        # Crear círculos
        self.circle1 = self.create_circle(
            self.size/2, self.size/2, 40,
            width=8, outline="gradient1"
        )
        self.circle2 = self.create_circle(
            self.size/2, self.size/2, 30,
            width=8, outline="gradient2"
        )
        
        # Iniciar animación
        self._angle = 0
        self._dash_offset1 = 251.3274
        self._dash_offset2 = 0
        self.animate()
        
    def _create_gradients(self):
        # Gradiente 1
        gradient1_colors = [
            (0, "#4f8ef7"),
            (0.5, "#a663cc"),
            (1, "#f74f6f")
        ]
        self._create_gradient("gradient1", gradient1_colors)
        
        # Gradiente 2
        gradient2_colors = [
            (0, "#f7b34f"),
            (0.5, "#5ef7a5"),
            (1, "#4f8ef7")
        ]
        self._create_gradient("gradient2", gradient2_colors)
    
    def _create_gradient(self, name, colors):
        # Crear suficientes colores intermedios para una transición suave
        steps = 100
        gradient = []
        for i in range(steps):
            t = i / (steps - 1)
            for j in range(len(colors) - 1):
                if t <= colors[j+1][0]:
                    t1, c1 = colors[j]
                    t2, c2 = colors[j+1]
                    factor = (t - t1) / (t2 - t1)
                    
                    # Interpolar colores
                    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
                    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
                    r = int(r1 + factor * (r2 - r1))
                    g = int(g1 + factor * (g2 - g1))
                    b = int(b1 + factor * (b2 - b1))
                    
                    gradient.append(f"#{r:02x}{g:02x}{b:02x}")
                    break
        setattr(self, f"_{name}", gradient)
    
    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(
            x-r, y-r, x+r, y+r,
            **kwargs
        )
    
    def animate(self):
        if not hasattr(self, "_running"):
            self._running = True
            self._animate_thread = threading.Thread(target=self._animate_loop, daemon=True)
            self._animate_thread.start()
    
    def _animate_loop(self):
        while self._running:
            # Rotar gradientes
            self._angle = (self._angle + 2) % 360
            angle_rad = math.radians(self._angle)
            
            # Actualizar gradientes
            for i, circle in enumerate([self.circle1, self.circle2]):
                gradient = getattr(self, f"_gradient{i+1}")
                color_idx = int((self._angle / 360) * len(gradient))
                self.itemconfig(
                    circle,
                    outline=gradient[color_idx % len(gradient)]
                )
            
            # Animar dashoffset
            t = (1 + math.sin(angle_rad)) / 2
            self._dash_offset1 = 251.3274 * (1 - t)
            self._dash_offset2 = 188.4956 * t
            
            self.itemconfig(
                self.circle1,
                dash=(251.3274, 251.3274),
                dashoffset=self._dash_offset1
            )
            self.itemconfig(
                self.circle2,
                dash=(188.4956, 188.4956),
                dashoffset=self._dash_offset2
            )
            
            time.sleep(0.016)  # ~60 FPS
    
    def stop(self):
        self._running = False
        if hasattr(self, "_animate_thread"):
            self._animate_thread.join()

class AnimatedText(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invertbox = ctk.CTkFrame(
            self,
            width=48,
            height=48,
            corner_radius=10,
            fg_color="gray30",
            bg_color="transparent"
        )
        self.invertbox.place(x=0, y=0)
        self._animate()
    
    def _animate(self):
        if not hasattr(self, "_pos"):
            self._pos = 0
            self._direction = 1
        
        # Mover el cuadro
        max_x = self.winfo_width() - 48
        self._pos += self._direction * 2
        
        if self._pos >= max_x:
            self._pos = max_x
            self._direction = -1
        elif self._pos <= 0:
            self._pos = 0
            self._direction = 1
        
        self.invertbox.place(x=self._pos)
        self.after(16, self._animate)  # ~60 FPS
