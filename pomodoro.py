# crear temporizador pomodoro con 25 min de trabajo, 5 min de descanso corto y 15 min de descanso largo

import tkinter as tk 
import time 
import pygame 
import threading
from tkinter import ttk 
from datetime import datetime, timedelta

class temporizador_pomodoro:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro")
        self.root.geometry("500x500")
        self.root.configure(bg='black')
        self.root.resizable(False, False)

    def run(self):
        self.root.mainloop()
