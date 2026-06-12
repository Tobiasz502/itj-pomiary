import nidaqmx
import time
import threading

class AkwizycjaDanych:
    def __init__(self):
        # Bufor na próbki i stan programu
        self.bufor = []
        self.czy_dziala = False

    def start(self):
        """Włącza akwizycję w tle, żeby nie zawiesić komputera."""
        self.czy_dziala = True
        threading.Thread(target=self._petla, daemon=True).start()

    def stop(self):
        """Zatrzymuje pobieranie danych."""
        self.czy_dziala = False

    def _petla(self):
        """Główny silnik (kręci się cały czas w tle)."""
        try:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan("myDAQ2/ai0")
                
                while self.czy_dziala:
                    sample = task.read()      # Czytamy napięcie
                    self.bufor.append(sample) # Wrzucamy do pamięci
                    time.sleep(0.1)           # Czekamy 100ms
                    
        except Exception as e:
            print(f"Błąd sprzętu: {e}")
            self.czy_dziala = False

    def get_samples(self):
        """Zwraca zebrane próbki i czyści bufor."""
        dane = self.bufor.copy()
        self.bufor.clear()
        return dane

# === KOD TESTOWY (uruchomi się tylko jak odpalisz ten plik w konsoli) ===
if __name__ == "__main__":
    print("Uruchamiam akwizycję z myDAQ2 na 5 sekund...")
    modul = AkwizycjaDanych()
    modul.start()
    
    time.sleep(5.0) # Czekamy 5 sekund
    
    modul.stop()
    wyniki = modul.get_samples()
    print(f"Pobrano {len(wyniki)} próbek. Wyniki: {wyniki}")