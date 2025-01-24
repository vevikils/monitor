#Importamos las librerías necesarias

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from datetime import datetime

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor del Sistema")
        self.root.geometry("1200x600")
        self.root.configure(bg="#2e2e2e")

    
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Figura de Matplotlib
        self.fig = Figure(figsize=(10, 5), dpi=100, facecolor='#2e2e2e')
        self.cpu_ax = self.fig.add_subplot(131, facecolor='#2e2e2e')
        self.mem_ax = self.fig.add_subplot(132, facecolor='#2e2e2e')
        self.disk_ax = self.fig.add_subplot(133, facecolor='#2e2e2e')

        # Canvas de Matplotlib en Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Intervalo de actualización automática en milisegundos
        self.update_interval = 500
        self.auto_update = True
        self.start_auto_update()

    def start_auto_update(self):
        if self.auto_update:
            self.update_stats()
            self.root.after(self.update_interval, self.start_auto_update)

    def update_stats(self):
        # Obtener estadísticas del sistema
        cpu_usage = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Limpiar gráficos anteriores
        self.cpu_ax.cla()
        self.mem_ax.cla()
        self.disk_ax.cla()

        # Configuración de estilos
        style = ttk.Style()
        style.configure("TLabel", background="#2e2e2e", foreground="white", font=("Arial", 12))
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TButton", background="#4e4e4e", foreground="white", font=("Arial", 10))
        
        cpu_color = "#1f77b4"
        mem_color = "#2ca02c"
        disk_color = "#d62728"


        # Función para crear un degradado horizontal
        def gradient_barh(ax, label, value, color):
            bars = ax.barh([label], [value], color=color, edgecolor='white')
            for bar in bars:
                x0, y0 = bar.get_xy()
                w = bar.get_width()
                h = bar.get_height()
                grad = np.linspace(0.3, 1, 256)
                grad = np.vstack((grad, grad))
                ax.imshow(grad, extent=[x0, x0 + w, y0, y0 + h], aspect='auto', cmap=plt.get_cmap('Blues'))

        # Gráfico de uso de CPU
        gradient_barh(self.cpu_ax, '', cpu_usage, cpu_color)
        self.cpu_ax.set_xlim(0, 100)
        self.cpu_ax.set_title('Uso de CPU (%)', fontsize=14, color="white")
        self.cpu_ax.tick_params(axis='x', colors='white')
        self.cpu_ax.tick_params(axis='y', colors='white')
        self.cpu_ax.spines['bottom'].set_color('white')
        self.cpu_ax.spines['top'].set_color('white')
        self.cpu_ax.spines['right'].set_color('white')
        self.cpu_ax.spines['left'].set_color('white')
        self.cpu_ax.bar_label(self.cpu_ax.containers[0], fmt='%.2f%%', label_type='center', color='white')

        # Gráfico de uso de Memoria
        gradient_barh(self.mem_ax, '', mem.percent, mem_color)
        self.mem_ax.set_xlim(0, 100)
        self.mem_ax.set_title('Uso de Memoria (%)', fontsize=14, color="white")
        self.mem_ax.tick_params(axis='x', colors='white')
        self.mem_ax.tick_params(axis='y', colors='white')
        self.mem_ax.spines['bottom'].set_color('white')
        self.mem_ax.spines['top'].set_color('white')
        self.mem_ax.spines['right'].set_color('white')
        self.mem_ax.spines['left'].set_color('white')
        self.mem_ax.bar_label(self.mem_ax.containers[0], fmt='%.2f%%', label_type='center', color='white')

        # Gráfico de uso de Disco
        gradient_barh(self.disk_ax, '', disk.percent, disk_color)
        self.disk_ax.set_xlim(0, 100)
        self.disk_ax.set_title('Uso de Disco (%)', fontsize=14, color="white")
        self.disk_ax.tick_params(axis='x', colors='white')
        self.disk_ax.tick_params(axis='y', colors='white')
        self.disk_ax.spines['bottom'].set_color('white')
        self.disk_ax.spines['top'].set_color('white')
        self.disk_ax.spines['right'].set_color('white')
        self.disk_ax.spines['left'].set_color('white')
        self.disk_ax.bar_label(self.disk_ax.containers[0], fmt='%.2f%%', label_type='center', color='white')

        # Redibujar el canvas
        self.canvas.draw()

 # Registrar las métricas en un archivo de texto
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{datetime.now()} - CPU: {cpu_usage}% - Memoria: {mem.percent}% - Disco: {disk.percent}%\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
