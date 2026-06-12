import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import csv
from modul_akwizycji import AkwizycjaDanych

class AplikacjaPomiarowa:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja Akwizycji Danych (Zadanie 3)")
        
        # Podpinamy nasz silnik z Zadania 2
        self.daq = AkwizycjaDanych()
        
        # Zmienne do kontroli pomiaru
        self.czy_pomiar_trwa = False
        self.czy_tryb_auto = False
        self.czas_do_konca_pomiaru = 0
        self.czas_do_restartu_auto = 0
        
        self.zebrane_dane_pomiaru = []
        self.limit_przekroczony = False
        self.dane_wykresu_y = [] 
        
        self.zbuduj_interfejs()
        self.aktualizuj_gui()

    def zbuduj_interfejs(self):
        """Tworzy wygląd okna (przyciski, pola)."""
        panel = tk.Frame(self.root)
        panel.pack(pady=10)

        tk.Button(panel, text="Start Akwizycji", command=self.daq.start, bg="lightgreen").grid(row=0, column=0, padx=5)
        tk.Button(panel, text="Stop Akwizycji", command=self.daq.stop, bg="salmon").grid(row=0, column=1, padx=5)
        tk.Button(panel, text="Start Pomiaru", command=self.start_pomiaru, bg="lightblue").grid(row=0, column=2, padx=5)
        tk.Button(panel, text="Stop Pomiaru", command=self.stop_pomiaru, bg="salmon").grid(row=0, column=3, padx=5)
        
        self.btn_auto = tk.Button(panel, text="Tryb Auto: WYŁ", command=self.przelacz_auto, bg="lightgray")
        self.btn_auto.grid(row=0, column=4, padx=5)

        ustawienia = tk.Frame(self.root)
        ustawienia.pack(pady=5)
        
        tk.Label(ustawienia, text="Długość pomiaru [s]:").grid(row=0, column=0)
        self.entry_czas = tk.Entry(ustawienia, width=5)
        self.entry_czas.insert(0, "5")
        self.entry_czas.grid(row=0, column=1)

        tk.Label(ustawienia, text="Limit MIN:").grid(row=0, column=2, padx=(10,0))
        self.entry_min = tk.Entry(ustawienia, width=5)
        self.entry_min.insert(0, "2.0")
        self.entry_min.grid(row=0, column=3)

        tk.Label(ustawienia, text="Limit MAX:").grid(row=0, column=4, padx=(10,0))
        self.entry_max = tk.Entry(ustawienia, width=5)
        self.entry_max.insert(0, "8.0")
        self.entry_max.grid(row=0, column=5)

        self.lbl_stan = tk.Label(self.root, text="STAN: Oczekiwanie", font=("Arial", 14, "bold"))
        self.lbl_stan.pack(pady=5)
        
        self.lbl_ocena = tk.Label(self.root, text="Ocena: Brak", font=("Arial", 12))
        self.lbl_ocena.pack(pady=5)

        # Ustawienia wykresu
        self.figura = Figure(figsize=(8, 4), dpi=100)
        self.os = self.figura.add_subplot(111)
        self.os.set_title("Przebieg napięcia [V]")
        self.plot_canvas = FigureCanvasTkAgg(self.figura, self.root)
        self.plot_canvas.get_tk_widget().pack()

    def przelacz_auto(self):
        self.czy_tryb_auto = not self.czy_tryb_auto
        if self.czy_tryb_auto:
            self.btn_auto.config(text="Tryb Auto: WŁ", bg="gold")
        else:
            self.btn_auto.config(text="Tryb Auto: WYŁ", bg="lightgray")

    def start_pomiaru(self):
        if not self.daq.czy_dziala:
            messagebox.showwarning("Błąd", "Kliknij najpierw Start Akwizycji!")
            return
            
        self.czy_pomiar_trwa = True
        self.zebrane_dane_pomiaru = []
        self.limit_przekroczony = False
        self.czas_do_konca_pomiaru = int(self.entry_czas.get()) * 10
        
        self.lbl_stan.config(text="STAN: W trakcie pomiaru...", fg="blue")
        self.lbl_ocena.config(text="Ocena: Sprawdzanie...", bg="white")

    def stop_pomiaru(self):
        if not self.czy_pomiar_trwa:
            return
            
        self.czy_pomiar_trwa = False
        self.zapisz_do_pliku()
        
        if self.limit_przekroczony:
            self.lbl_ocena.config(text="Ocena: NEGATYWNA (Przekroczono limity)", bg="red", fg="white")
        else:
            self.lbl_ocena.config(text="Ocena: POZYTYWNA (W limitach)", bg="green", fg="white")
            
        self.lbl_stan.config(text="STAN: Zakończono pomiar", fg="black")
        
        if self.czy_tryb_auto:
            self.czas_do_restartu_auto = 30 # Czeka 3 sekundy
            self.lbl_stan.config(text="STAN: Przerwa przed kolejnym pomiarem...", fg="orange")

    def zapisz_do_pliku(self):
        nazwa_pliku = datetime.datetime.now().strftime("Pomiar_%Y%m%d_%H%M%S.csv")
        with open(nazwa_pliku, mode='w', newline='') as plik:
            writer = csv.writer(plik)
            writer.writerow(["Probka", "Napięcie [V]"])
            for i, wartosc in enumerate(self.zebrane_dane_pomiaru):
                writer.writerow([i, round(wartosc, 4)])

    def aktualizuj_gui(self):
        """Pętla okienka odświeżająca się co 100ms."""
        if self.daq.czy_dziala:
            # POBIERANIE TYLKO JEDNEJ LISTY DANYCH
            probki_ai = self.daq.get_samples()
            
            if probki_ai:
                # Rysowanie wykresu
                self.dane_wykresu_y.extend(probki_ai)
                if len(self.dane_wykresu_y) > 100:
                    self.dane_wykresu_y = self.dane_wykresu_y[-100:]
                    
                self.os.clear()
                self.os.plot(self.dane_wykresu_y, color='blue')
                self.os.set_ylim([-10, 10]) 
                self.plot_canvas.draw()
                
                # Ocenianie pomiaru, jeśli jest aktywny
                if self.czy_pomiar_trwa:
                    limit_min = float(self.entry_min.get())
                    limit_max = float(self.entry_max.get())
                    self.zebrane_dane_pomiaru.extend(probki_ai)
                    
                    for p in probki_ai:
                        if p < limit_min or p > limit_max:
                            self.limit_przekroczony = True
                            
                    self.czas_do_konca_pomiaru -= len(probki_ai)
                    if self.czas_do_konca_pomiaru <= 0:
                        self.stop_pomiaru()

        # Obsługa trybu Auto
        if not self.czy_pomiar_trwa and self.czy_tryb_auto and self.czas_do_restartu_auto > 0:
            self.czas_do_restartu_auto -= 1
            if self.czas_do_restartu_auto <= 0:
                self.start_pomiaru()

        self.root.after(100, self.aktualizuj_gui)


if __name__ == "__main__":
    okno_glowne = tk.Tk()
    aplikacja = AplikacjaPomiarowa(okno_glowne)
    okno_glowne.mainloop()