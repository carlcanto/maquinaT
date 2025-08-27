import tkinter as tk
from tkinter import messagebox, ttk

CELL_WIDTH = 40
TAPE_LENGTH = 30

class TuringMachineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Máquina de Turing - Paridad de 1's")
        self.root.configure(bg="#580da2")  # Fondo pastel lila
        
        style = ttk.Style()
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=6, relief='flat', background="#473f78")
        style.map('TButton', background=[('active', '#b084cc')])
        
        self.tape = ['□'] * TAPE_LENGTH
        self.head_position = TAPE_LENGTH // 2
        self.state = 'PAR'
        self.running = False

        # Entrada de cadena
        frame_input = tk.Frame(root, bg="#f8f1ff")
        frame_input.pack(pady=10)
        tk.Label(frame_input, text="💬 Ingrese cadena binaria:", font=("Segoe UI", 11), bg="#f8f1ff").pack(side=tk.LEFT)
        self.entry = tk.Entry(frame_input, font=("Segoe UI", 11), width=25)
        self.entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_input, text="📥 Cargar", command=self.cargar_cinta).pack(side=tk.LEFT)

        # Cinta
        self.canvas = tk.Canvas(root, width=CELL_WIDTH * TAPE_LENGTH, height=90, bg="#ffffff", bd=0, highlightthickness=0)
        self.canvas.pack(pady=15)

        # Controles
        frame_controls = tk.Frame(root, bg="#f8f1ff")
        frame_controls.pack()
        self.btn_paso = ttk.Button(frame_controls, text="⏭ Paso a paso", command=self.paso)
        self.btn_paso.pack(side=tk.LEFT, padx=5)
        self.btn_ejecutar = ttk.Button(frame_controls, text="▶ Ejecutar", command=self.ejecutar_automatico)
        self.btn_ejecutar.pack(side=tk.LEFT, padx=5)
        self.btn_reiniciar = ttk.Button(frame_controls, text="🔄 Reiniciar", command=self.reiniciar)
        self.btn_reiniciar.pack(side=tk.LEFT, padx=5)

        # Estado
        self.estado_label = tk.Label(root, text="📍 Estado: PAR", font=("Segoe UI", 12), bg="#f8f1ff", fg="#080865")
        self.estado_label.pack(pady=5)

        self.resultado_label = tk.Label(root, text="", font=("Segoe UI", 12), bg="#f8f1ff", fg="#10ac84")
        self.resultado_label.pack()

        self.dibujar_cinta()

    def cargar_cinta(self):
        entrada = self.entry.get()
        if not all(c in '01' for c in entrada):
            messagebox.showerror("Error", "Solo se permiten 0 y 1")
            return
        self.reiniciar()
        start = self.head_position
        for i, bit in enumerate(entrada):
            self.tape[start + i] = bit
        self.dibujar_cinta()

    def dibujar_cinta(self):
        self.canvas.delete("all")
        for i, symbol in enumerate(self.tape):
            x = i * CELL_WIDTH
            color = "#2b56ba" if i == self.head_position else "#ffffff"
            border = "#3333bd" if i == self.head_position else "#dcdcdc"
            self.canvas.create_rectangle(x+2, 30, x + CELL_WIDTH - 2, 70, fill=color, outline=border, width=2)
            self.canvas.create_text(x + CELL_WIDTH // 2, 50, text=symbol, font=("Segoe UI", 14, "bold"), fill="#222")

        # Cabezal
        x_head = self.head_position * CELL_WIDTH + CELL_WIDTH // 2
        self.canvas.create_text(x_head, 15, text="⬇", font=("Arial", 16), fill="#ce933b")

    def paso(self):
        if self.state == 'FINAL':
            self.resultado_label.config(text="✅ Resultado: " + ''.join(self.tape).strip('□'))
            return

        symbol = self.tape[self.head_position]

        if self.state == 'PAR':
            if symbol == '1':
                self.head_position += 1
                self.state = 'IMPAR'
            elif symbol == '0':
                self.head_position += 1
            elif symbol == '□':
                self.tape[self.head_position] = '0'
                self.state = 'FINAL'

        elif self.state == 'IMPAR':
            if symbol == '1':
                self.head_position += 1
                self.state = 'PAR'
            elif symbol == '0':
                self.head_position += 1
            elif symbol == '□':
                self.tape[self.head_position] = '1'
                self.state = 'FINAL'

        self.estado_label.config(text="📍 Estado: " + self.state)
        self.dibujar_cinta()

    def ejecutar_automatico(self):
        self.btn_paso.config(state='disabled')
        self.btn_ejecutar.config(state='disabled')
        self.btn_reiniciar.config(state='disabled')
        self.running = True
        self.ejecutar_paso()

    def ejecutar_paso(self):
        if self.state == 'FINAL':
            self.resultado_label.config(text="✅ Resultado: " + ''.join(self.tape).strip('□'))
            self.running = False
            self.btn_paso.config(state='normal')
            self.btn_ejecutar.config(state='normal')
            self.btn_reiniciar.config(state='normal')
            return

        self.paso()
        self.root.after(500, self.ejecutar_paso)

    def reiniciar(self):
        self.tape = ['□'] * TAPE_LENGTH
        self.head_position = TAPE_LENGTH // 2
        self.state = 'PAR'
        self.resultado_label.config(text="")
        self.estado_label.config(text="📍 Estado: PAR")
        self.running = False
        self.btn_paso.config(state='normal')
        self.btn_ejecutar.config(state='normal')
        self.btn_reiniciar.config(state='normal')
        self.dibujar_cinta()


# Ejecutar interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = TuringMachineGUI(root)
    root.mainloop()
