import tkinter as tk
from tkinter import ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt

# colores de ventana
BG_COLOR = "#80292d"
BTN_COLOR = "#000000"
FG_COLOR = "#000000"

# diccionario de funciones NO MODIFICAR
diccionario = {
    'np': np,
    'pi': np.pi,
    'e': np.e,
    'sin': np.sin,
    'cos': np.cos,
    'tan': np.tan,
    'log': np.log,
    'exp': np.exp,
    'sqrt': np.sqrt
}

# definimos la homescreen
def main_interface():
    root = tk.Tk()
    root.title("Calculadora de Calculo Integral")
    root.geometry("400x500")
    root.configure(bg=BG_COLOR)
    icono = PhotoImage(file='icon.png')
    root.iconphoto(False, icono)
    root.tk.call('wm', 'iconphoto', root._w, icono)

    def create_button(text, command):
        style = ttk.Style()
        style.configure("Rounded.TButton", foreground=FG_COLOR, background=BTN_COLOR, font=("Arial", 12, "bold"), padding=10, relief="flat")
        return ttk.Button(root, text=text, style="Rounded.TButton", command=command)

    tk.Label(root, text="Calculadora de Calculo Integral", font=("Arial", 16, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=20)

    buttons = [
        ("Areas bajo la curva", area_bajo_curva),
        ("Area entre curvas", area_entre_curvas),
        ("Areas totales acotadas", areas_totales_acotadas),
        ("Volumen de solidos (discos)", volumen_discos),
        ("Volumen de solidos (arandelas)", volumen_arandelas),
    ]

    for text, func in buttons:
        btn = create_button(text, func)
        btn.pack(pady=10)

    create_button("Salir", root.quit).pack(pady=20, anchor="se")

    root.mainloop()

# funcion de area bajo la curva
def area_bajo_curva():
    area_window = tk.Toplevel()
    area_window.title("Area bajo la curva")
    area_window.geometry("800x900")
    area_window.configure(bg=BG_COLOR)

    tk.Label(area_window, text="Funcion (en terminos de x):", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion_entry = tk.Entry(area_window)
    funcion_entry.pack()

    tk.Label(area_window, text="Limite inferior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    a_entry = tk.Entry(area_window)
    a_entry.pack()

    tk.Label(area_window, text="Limite superior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    b_entry = tk.Entry(area_window)
    b_entry.pack()

    tk.Label(area_window, text="Numero de Rectangulos:", bg=BG_COLOR, fg=FG_COLOR).pack()
    c_entry = tk.Entry(area_window)
    c_entry.pack()
    

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=area_window)
    canvas.get_tk_widget().pack()
    
    def calcular_area():
        funcion = funcion_entry.get()
        a = float(a_entry.get())
        b = float(b_entry.get())
        n = int(c_entry.get())

        f = lambda x: eval(funcion)
        x = np.linspace(a, b, n)
        dx = (b - a) / n
        area = np.sum(f(x) * dx)

        ax.clear()
        ax.plot(x, f(x), color="blue")
        ax.bar(x, f(x), width=dx, color="skyblue", alpha=0.5)

        def animate(i):
            ax.plot(x[:i], f(x[:i]), color="blue", alpha=0.5)
            ax.bar(x[:i], f(x[:i]), width=dx, color="skyblue", alpha=0.5)

        ani = FuncAnimation(fig, animate, frames=n, repeat=False)
        canvas.draw()
        tk.Label(area_window, text=f"area aproximada: {area:.2f}", bg=BG_COLOR, fg=FG_COLOR).pack()

    ttk.Button(area_window, text="Calcular", command=calcular_area, style="Rounded.TButton").pack()
    ttk.Button(area_window, text="Regresar", command=area_window.destroy, style="Rounded.TButton").pack()

#funcion de area entre curvas 
def area_entre_curvas():
    area_curva_window = tk.Toplevel()
    area_curva_window.title("area entre curvas")
    area_curva_window.geometry("800x900")
    area_curva_window.configure(bg=BG_COLOR)

    tk.Label(area_curva_window, text="Funcion superior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion1_entry = tk.Entry(area_curva_window)
    funcion1_entry.pack()

    tk.Label(area_curva_window, text="Funcion inferior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion2_entry = tk.Entry(area_curva_window)
    funcion2_entry.pack()

    tk.Label(area_curva_window, text="Limite inferior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    a_entry = tk.Entry(area_curva_window)
    a_entry.pack()

    tk.Label(area_curva_window, text="Limite superior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    b_entry = tk.Entry(area_curva_window)
    b_entry.pack()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=area_curva_window)
    canvas.get_tk_widget().pack()

    def calcular_area_entre_curvas():
        funcion1_str = funcion1_entry.get()
        funcion2_str = funcion2_entry.get()
        
      
        try:
            a = eval(a_entry.get(), {"__builtins__": None}, diccionario) 
            b = eval(b_entry.get(), {"__builtins__": None}, diccionario)  
        except Exception as e:
            tk.Label(area_curva_window, text=f"Error en los limites: {e}", bg=BG_COLOR, fg=FG_COLOR).pack()
            return

        n = 100

        f1 = lambda x: eval(funcion1_str, {"x": x, "__builtins__": None}, diccionario)
        f2 = lambda x: eval(funcion2_str, {"x": x, "__builtins__": None}, diccionario)
        
        x_vals = np.linspace(a, b, n)
        dx = (b - a) / n
        area = np.sum((f1(x_vals) - f2(x_vals)) * dx)

        ax.clear()
        ax.plot(x_vals, f1(x_vals), color="blue")
        ax.plot(x_vals, f2(x_vals), color="red")

        def animate(i):
            ax.fill_between(x_vals[:i], f1(x_vals[:i]), f2(x_vals[:i]), color="purple", alpha=0.3)

        ani = FuncAnimation(fig, animate, frames=n, repeat=False)
        canvas.draw()
        tk.Label(area_curva_window, text=f"area entre curvas: {area:.2f}", bg=BG_COLOR, fg=FG_COLOR).pack()


    ttk.Button(area_curva_window, text="Calcular", command=calcular_area_entre_curvas, style="Rounded.TButton").pack()
    ttk.Button(area_curva_window, text="Regresar", command=area_curva_window.destroy, style="Rounded.TButton").pack()

#funcion de areas totales acodatas
def areas_totales_acotadas():
    acotadas_window = tk.Toplevel()
    acotadas_window.title("areas totales acotadas")
    acotadas_window.geometry("800x900")
    acotadas_window.configure(bg=BG_COLOR)

    tk.Label(acotadas_window, text="Funcion:", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion_entry = tk.Entry(acotadas_window)
    funcion_entry.pack()

    tk.Label(acotadas_window, text="Limite inferior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    a_entry = tk.Entry(acotadas_window)
    a_entry.pack()

    tk.Label(acotadas_window, text="Limite superior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    b_entry = tk.Entry(acotadas_window)
    b_entry.pack()

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=acotadas_window)
    canvas.get_tk_widget().pack()

    def calcular_area_total():
        funcion = funcion_entry.get()
        a = float(a_entry.get())
        b = float(b_entry.get())
        n = 100

        f = lambda x: abs(eval(funcion))
        x = np.linspace(a, b, n)
        dx = (b - a) / n
        area_total = np.sum(f(x) * dx)

        ax.clear()
        ax.plot(x, f(x), color="green")

        def animate(i):
            ax.plot(x[:i], f(x[:i]), color="green", alpha=0.5)
            ax.fill_between(x[:i], 0, f(x[:i]), color="green", alpha=0.3)

        ani = FuncAnimation(fig, animate, frames=n, repeat=False)
        canvas.draw()
        tk.Label(acotadas_window, text=f"area total acotada: {area_total:.2f}", bg=BG_COLOR, fg=FG_COLOR).pack()

    ttk.Button(acotadas_window, text="Calcular", command=calcular_area_total, style="Rounded.TButton").pack()
    ttk.Button(acotadas_window, text="Regresar", command=acotadas_window.destroy, style="Rounded.TButton").pack()


# funcion de volumen de solidos por metodo de discos
def volumen_discos():
    discos_window = tk.Toplevel()
    discos_window.title("Volumen de Solidos de Revolucion (metodo de discos)")
    discos_window.geometry("800x900")
    discos_window.configure(bg=BG_COLOR)

    tk.Label(discos_window, text="Funcion:", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion_entry = tk.Entry(discos_window)
    funcion_entry.pack()

    tk.Label(discos_window, text="Limite inferior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    a_entry = tk.Entry(discos_window)
    a_entry.pack()

    tk.Label(discos_window, text="Limite superior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    b_entry = tk.Entry(discos_window)
    b_entry.pack()

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    canvas = FigureCanvasTkAgg(fig, master=discos_window)
    canvas.get_tk_widget().pack()

    def calcular_volumen_discos():
        funcion = funcion_entry.get()
        a = float(a_entry.get())
        b = float(b_entry.get())
        n = 100

     
        f = lambda x: eval(funcion, {"np": np, "x": x}, diccionario)

        x = np.linspace(a, b, n)
        dx = (b - a) / n
        volume = np.sum(np.pi * f(x) ** 2 * dx)

        ax.clear()
        ax.plot(x, f(x), color="blue")

        def animate(i):
            r = f(x[:i])
            theta = np.linspace(0, 2 * np.pi, 30)
            X = np.outer(r, np.cos(theta))
            Y = np.outer(r, np.sin(theta))
            Z = np.outer(x[:i], np.ones_like(theta))
            ax.plot_surface(X, Y, Z, color="skyblue", alpha=0.3)

        ani = FuncAnimation(fig, animate, frames=n, repeat=False)
        canvas.draw()
        tk.Label(discos_window, text=f"Volumen aproximado: {volume:.2f}", bg=BG_COLOR, fg=FG_COLOR).pack()

    ttk.Button(discos_window, text="Calcular", command=calcular_volumen_discos, style="Rounded.TButton").pack()
    ttk.Button(discos_window, text="Regresar", command=discos_window.destroy, style="Rounded.TButton").pack()

# funcion de volumen de solidos por metodo de arandelas
def volumen_arandelas():
    arandelas_window = tk.Toplevel()
    arandelas_window.title("Volumen de Solidos de Revolucion (Metodo de Arandelas)")
    arandelas_window.geometry("800x900")
    arandelas_window.configure(bg=BG_COLOR)

    tk.Label(arandelas_window, text="Funcion exterior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion1_entry = tk.Entry(arandelas_window)
    funcion1_entry.pack()

    tk.Label(arandelas_window, text="Funcion interior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    funcion2_entry = tk.Entry(arandelas_window)
    funcion2_entry.pack()

    tk.Label(arandelas_window, text="Limite inferior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    a_entry = tk.Entry(arandelas_window)
    a_entry.pack()

    tk.Label(arandelas_window, text="Limite superior:", bg=BG_COLOR, fg=FG_COLOR).pack()
    b_entry = tk.Entry(arandelas_window)
    b_entry.pack()

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    canvas = FigureCanvasTkAgg(fig, master=arandelas_window)
    canvas.get_tk_widget().pack()

    def calcular_volumen_arandelas():
        funcion1 = funcion1_entry.get()
        funcion2 = funcion2_entry.get()
        try:
            a = eval(a_entry.get(), {"__builtins__": None}, diccionario)  
            b = eval(b_entry.get(), {"__builtins__": None}, diccionario)  
        except Exception as e:
            tk.Label(area_curva_window, text=f"Error en los límites: {e}", bg=BG_COLOR, fg=FG_COLOR).pack()
            return
        n = 1000

        f1 = lambda x: eval(funcion1, {"x": x, "__builtins__": None}, diccionario)
        f2 = lambda x: eval(funcion2, {"x": x, "__builtins__": None}, diccionario)
        x = np.linspace(a, b, n)
        dx = (b - a) / n
        volume = np.sum(np.pi * (f1(x) ** 2 - f2(x) ** 2) * dx)

        ax.clear()
        ax.plot(x, f1(x), color="blue")
        ax.plot(x, f2(x), color="red")

        def animate(i):
            r_outer = f1(x[:i])
            r_inner = f2(x[:i])
            theta = np.linspace(0, 2 * np.pi, 30)
            X_outer = np.outer(r_outer, np.cos(theta))
            Y_outer = np.outer(r_outer, np.sin(theta))
            X_inner = np.outer(r_inner, np.cos(theta))
            Y_inner = np.outer(r_inner, np.sin(theta))
            Z = np.outer(x[:i], np.ones_like(theta))
            ax.plot_surface(X_outer, Y_outer, Z, color="skyblue", alpha=0.3)
            ax.plot_surface(X_inner, Y_inner, Z, color="white", alpha=0.5)

        ani = FuncAnimation(fig, animate, frames=n, repeat=False)
        canvas.draw()
        tk.Label(arandelas_window, text=f"Volumen aproximado: {volume:.2f}", bg=BG_COLOR, fg=FG_COLOR).pack()

    ttk.Button(arandelas_window, text="Calcular", command=calcular_volumen_arandelas, style="Rounded.TButton").pack()
    ttk.Button(arandelas_window, text="Regresar", command=arandelas_window.destroy, style="Rounded.TButton").pack()




main_interface()


