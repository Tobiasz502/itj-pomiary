import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# KROK 1: Wczytanie i przygotowanie danych
# ==========================================

# Wczytujemy dane z pliku CSV do tabeli (tzw. DataFrame)
df = pd.read_csv('energydata_complete.csv')

# Komputer domyślnie widzi datę jako zwykły tekst. 
# Musimy mu powiedzieć, że to format czasu, aby móc wyciągnąć z niego godzinę.
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour

# Ustawiamy ładny, przejrzysty styl dla wszystkich wykresów
sns.set_theme(style="whitegrid")


# ==========================================
# KROK 2: Generowanie i zapisywanie wykresów
# ==========================================

# --- WYKRES 1: Histogram zużycia energii ---
# Pokazuje, jak często występuje dane zużycie prądu w domu.
plt.figure(figsize=(10, 6))
sns.histplot(df['Appliances'], bins=50, color='skyblue')
plt.title('Rozkład zużycia energii przez urządzenia domowe')
plt.xlabel('Zużycie energii [Wh]')
plt.ylabel('Liczba pomiarów')
plt.savefig('wykres1_rozklad.png') # Zapisuje obrazek na dysku
plt.close() # Czyści pamięć przed kolejnym wykresem


# --- WYKRES 2: Średnie zużycie w ciągu dnia ---
# Liczymy średnie zużycie prądu dla każdej godziny (0-23).
srednie_godzinowe = df.groupby('hour')['Appliances'].mean()

plt.figure(figsize=(10, 6))
plt.plot(srednie_godzinowe.index, srednie_godzinowe.values, marker='o', color='orange', linewidth=2)
plt.title('Średnie zużycie energii w zależności od godziny dnia')
plt.xlabel('Godzina w ciągu doby [h]')
plt.ylabel('Średnie zużycie [Wh]')
plt.xticks(range(0, 24)) # Ustawia podziałkę osi X co 1 godzinę
plt.savefig('wykres2_godziny.png')
plt.close()


# --- WYKRES 3: Zależność energii od temperatury ---
# Wykres punktowy sprawdzający, czy temperatura na zewnątrz wpływa na prąd.
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='T_out', y='Appliances', alpha=0.3, color='green')
plt.title('Wpływ temperatury zewnętrznej na zużycie energii')
plt.xlabel('Temperatura na zewnątrz [°C]')
plt.ylabel('Zużycie energii [Wh]')
plt.savefig('wykres3_temperatura.png')
plt.close()


# --- WYKRES 4: Izolacja budynku (Wewnątrz vs Zewnątrz) ---
# Bierzemy tylko pierwsze 288 wierszy (to równowartość 2 dni, bo pomiary są co 10 minut), 
# żeby na wykresie nie było "pajęczyny" i żeby cokolwiek było widać.
male_dane = df.head(288) 

plt.figure(figsize=(12, 6))
plt.plot(male_dane['date'], male_dane['T1'], label='Temp. w kuchni [°C]', color='red')
plt.plot(male_dane['date'], male_dane['T_out'], label='Temp. na zewnątrz [°C]', linestyle='--', color='blue')
plt.title('Porównanie temperatury wewnątrz i na zewnątrz (wycinek 2 dni)')
plt.xlabel('Czas (Dni)')
plt.ylabel('Temperatura [°C]')
plt.legend() # Pokazuje legendę, żeby było wiadomo co jest jakim kolorem
plt.savefig('wykres4_izolacja.png')
plt.close()


# --- WYKRES 5: Mapa powiązań (Korelacja) ---
# Sprawdzamy, jak wybrane parametry wpływają na siebie nawzajem.
# 1.0 oznacza pełne powiązanie, a wartości bliskie 0 to brak powiązania.
plt.figure(figsize=(10, 8))
wybrane_kolumny = ['Appliances', 'T_out', 'RH_1', 'Windspeed']  # oryginalne nazwy z CSV
nazwy_pl = ['Urządzenia', 'Temp. zewn. [°C]', 'Wilgotność [%]', 'Wiatr [m/s]']
corr = df[wybrane_kolumny].corr()
corr.columns = nazwy_pl
corr.index = nazwy_pl
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Mapa korelacji między parametrami')
plt.savefig('wykres5_korelacja.png')
plt.close()

print("Gotowe! Wszystkie 5 wykresów zostało wygenerowanych i zapisanych w tym samym folderze.")