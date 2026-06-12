import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import csv

root = tk.Tk()
root.title("Testing Suite App")
root.geometry("900x600")

dane_time = []
dane_value = []

def wczytaj_plik():
    sciezka = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not sciezka:
        return
    dane_time.clear()
    dane_value.clear()
    for row in tabela.get_children():
        tabela.delete(row)
    with open(sciezka, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        for wiersz in reader:
            t = float(wiersz['time'])
            v = float(wiersz['value'])
            dane_time.append(t)
            dane_value.append(v)
            tabela.insert('', 'end', values=(round(t, 3), round(v, 3)))
    rysuj_wykres()

def rysuj_wykres():
    ax.clear()
    ax.scatter(dane_time, dane_value, s=10, color='steelblue', label='Dane')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    if log_var.get():
        ax.set_yscale('log')
        ax.set_title('Dane (skala logarytmiczna)')
    else:
        ax.set_yscale('linear')
        ax.set_title('Dane (skala liniowa)')
    ax.legend()
    canvas.draw()

def oblicz_regresje():
    if not dane_time:
        return
    x = np.array(dane_time)
    y = np.array(dane_value)
    a, b = np.polyfit(x, y, 1)
    label_a.config(text=f"{a:.4f}")
    label_b.config(text=f"{b:.4f}")
    ax.clear()
    ax.scatter(x, y, s=10, color='steelblue', label='Dane')
    ax.plot(x, a * x + b, color='red', linewidth=2, label=f'Regresja: y = {a:.2f}x + {b:.2f}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Regresja liniowa')
    ax.legend()
    if log_var.get():
        ax.set_yscale('log')
    canvas.draw()

def przelacz_skale():
    rysuj_wykres()

lewa = tk.Frame(root)
lewa.pack(side='left', fill='both', expand=True, padx=10, pady=10)

przyciski = tk.Frame(lewa)
przyciski.pack(side='top', fill='x')

btn_load = tk.Button(przyciski, text="Load Data", command=wczytaj_plik, width=12)
btn_load.pack(side='left', padx=5)

btn_plot = tk.Button(przyciski, text="Plot", command=rysuj_wykres, width=12)
btn_plot.pack(side='left', padx=5)

btn_reg = tk.Button(przyciski, text="Calculate Regression", command=oblicz_regresje, width=20)
btn_reg.pack(side='left', padx=5)

log_var = tk.BooleanVar()
chk_log = tk.Checkbutton(lewa, text="Log Y?", variable=log_var, command=przelacz_skale)
chk_log.pack(side='top', anchor='w', padx=5)

ramka_ab = tk.Frame(lewa)
ramka_ab.pack(side='top', anchor='w', padx=5, pady=3)

tk.Label(ramka_ab, text="a:").pack(side='left')
label_a = tk.Label(ramka_ab, text="0", width=10, relief='sunken')
label_a.pack(side='left', padx=5)

tk.Label(ramka_ab, text="b:").pack(side='left')
label_b = tk.Label(ramka_ab, text="0", width=10, relief='sunken')
label_b.pack(side='left', padx=5)

fig, ax = plt.subplots(figsize=(6, 4))
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
canvas = FigureCanvasTkAgg(fig, master=lewa)
canvas.get_tk_widget().pack(fill='both', expand=True)

prawa = tk.Frame(root, width=200)
prawa.pack(side='right', fill='y', padx=10, pady=10)

tk.Label(prawa, text="Data").pack()

scroll = tk.Scrollbar(prawa)
scroll.pack(side='right', fill='y')

tabela = ttk.Treeview(prawa, columns=('time', 'value'), show='headings', yscrollcommand=scroll.set, height=30)
tabela.heading('time', text='time')
tabela.heading('value', text='value')
tabela.column('time', width=80)
tabela.column('value', width=80)
tabela.pack(side='left', fill='y')

scroll.config(command=tabela.yview)

root.mainloop()