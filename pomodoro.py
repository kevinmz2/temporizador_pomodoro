import tkinter as tk
import threading
import time

class temporizador_pomodoro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Temporizador Pomodoro")
        self.root.geometry("400x400")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Variables del temporizador
        self.work_time = 25 * 60  
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        
        # Estado del temporizador
        self.is_running = False
        self.current_time = self.work_time
        self.timer_thread = None
        self.session_count = 0
        self.current_phase = "Trabajo"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título principal
        title_label = tk.Label(
            self.root,
            text="TEMPORIZADOR",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="black"
        )
        title_label.pack(pady=20)
        
        # Contador de sesiones
        self.session_label = tk.Label(
            self.root,
            text=f"Sesión: {self.session_count}/4",
            font=("Arial", 12),
            fg="white",
            bg="black"
        )
        self.session_label.pack()
        
        # Fase actual
        self.phase_label = tk.Label(
            self.root,
            text=self.current_phase,
            font=("Arial", 14, "bold"),
            fg="white",
            bg="black"
        )
        self.phase_label.pack(pady=10)
        
        # Display del tiempo
        self.time_display = tk.Label(
            self.root,
            text=self.format_time(self.current_time),
            font=("Arial", 48, "bold"),
            fg="white",
            bg="black"
        )
        self.time_display.pack(pady=30)
        
        # Botones principales
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=20)
        
        self.start_pause_btn = tk.Button(
            button_frame,
            text="INICIAR",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="black",
            command=self.toggle_timer,
            width=10,
            height=2
        )
        self.start_pause_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = tk.Button(
            button_frame,
            text="RESET",
            font=("Arial", 12, "bold"),
            bg="gray30",
            fg="white",
            command=self.reset_timer,
            width=10,
            height=2
        )
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        self.skip_btn = tk.Button(
            button_frame,
            text="SALTAR",
            font=("Arial", 12, "bold"),
            bg="gray30",
            fg="white",
            command=self.skip_phase,
            width=10,
            height=2
        )
        self.skip_btn.pack(side=tk.LEFT, padx=10)
        

        # minutos configuracion
        config_frame = tk.Frame(self.root, bg="black")
        config_frame.pack(pady=20)
        
        tk.Label(config_frame, text="Configuración (minutos):", 
                font=("Arial", 10), fg="white", bg="black").pack()
        
        controls_frame = tk.Frame(config_frame, bg="black")
        controls_frame.pack(pady=10)
        
        # campos de configurar
        tk.Label(controls_frame, text="Trabajo:", fg="white", bg="black").grid(row=0, column=0, padx=5)
        self.work_var = tk.StringVar(value="25")
        tk.Entry(controls_frame, textvariable=self.work_var, width=5, justify='center').grid(row=0, column=1, padx=5)
        
        tk.Label(controls_frame, text="D.Corto:", fg="white", bg="black").grid(row=0, column=2, padx=5)
        self.short_var = tk.StringVar(value="5")
        tk.Entry(controls_frame, textvariable=self.short_var, width=5, justify='center').grid(row=0, column=3, padx=5)
        
        tk.Label(controls_frame, text="D.Largo:", fg="white", bg="black").grid(row=1, column=0, padx=5)
        self.long_var = tk.StringVar(value="15")
        tk.Entry(controls_frame, textvariable=self.long_var, width=5, justify='center').grid(row=1, column=1, padx=5)
        
        tk.Button(controls_frame, text="Aplicar", font=("Arial", 9), bg="gray30", 
                 fg="white", command=self.apply_config).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
    
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.pause_timer()
    
    def start_timer(self):
        self.is_running = True
        self.start_pause_btn.config(text="PAUSAR")
        
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
    
    def pause_timer(self):
        self.is_running = False
        self.start_pause_btn.config(text="CONTINUAR")
    
    def reset_timer(self):
        self.is_running = False
        self.start_pause_btn.config(text="INICIAR")
        self.current_phase = "Trabajo"
        self.current_time = self.work_time
        self.session_count = 0
        self.update_display()
    
    def skip_phase(self):
        if self.is_running:
            self.current_time = 0
    
    def apply_config(self):
        try:
            self.work_time = int(self.work_var.get()) * 60
            self.short_break = int(self.short_var.get()) * 60
            self.long_break = int(self.long_var.get()) * 60
            
            if not self.is_running:
                if self.current_phase == "Trabajo":
                    self.current_time = self.work_time
                elif self.current_phase == "Descanso Corto":
                    self.current_time = self.short_break
                else:
                    self.current_time = self.long_break
                self.update_display()
        except ValueError:
            pass
    
    def next_phase(self):
        if self.current_phase == "Trabajo":
            self.session_count += 1
            
            if self.session_count >= 4:
                self.current_phase = "Descanso Largo"
                self.current_time = self.long_break
                self.session_count = 0
            else:
                self.current_phase = "Descanso Corto"
                self.current_time = self.short_break
        else:
            self.current_phase = "Trabajo"
            self.current_time = self.work_time
        
        self.update_display()
    
    def update_display(self):
        self.time_display.config(text=self.format_time(self.current_time))
        self.phase_label.config(text=self.current_phase)
        self.session_label.config(text=f"Sesión: {self.session_count}/4")
        
        # cambia segun fase
        if self.current_phase == "Trabajo":
            self.phase_label.config(fg="white")
        elif self.current_phase == "Descanso Corto":
            self.phase_label.config(fg="lightgreen")
        else:
            self.phase_label.config(fg="lightblue")
    
    def run_timer(self):
        while self.is_running and self.current_time > 0:
            time.sleep(1)
            if self.is_running:
                self.current_time -= 1
                self.root.after(0, self.update_display)
        
        if self.current_time <= 0 and self.is_running:
            print("Fin") 
            self.root.after(0, self.next_phase)
            
            if self.is_running:
                self.root.after(1000, self.start_timer)
    
    def run(self):
        self.root.mainloop()
